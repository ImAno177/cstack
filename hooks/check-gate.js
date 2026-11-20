const fs = require('fs');
const path = require('path');
const { dataDir, run, shellCommand } = require('./lib');

const codeExt = /\.(c|cc|cpp|cs|cjs|cts|dart|ex|exs|go|gradle|h|hpp|java|js|jsx|kt|kts|lua|m|mjs|mts|php|ps1|py|rb|rs|scala|sh|svelte|swift|ts|tsx|vue|zig)$/i;

const checkCommand = new RegExp(
  [
    '\\b(pytest|unittest|tox|nox|mypy|pyright|ruff|py_compile|compileall)\\b',
    '\\b(jest|vitest|mocha|ava|playwright|cypress|eslint|biome|tsc)\\b',
    '\\b(npm|pnpm|yarn|bun)\\s+(test|t|run\\s+\\S+|build|lint|typecheck|check)\\b',
    '\\bnode\\s+--test\\b',
    '\\bdeno\\s+(test|check|lint)\\b',
    '\\bgo\\s+(test|build|vet)\\b',
    '\\bcargo\\s+(test|build|check|clippy|nextest)\\b',
    '\\b(gradlew?|mvnw?|ctest|bazel|buck2?|xcodebuild|phpunit|rspec|rake)\\b',
    '\\bmake\\b(?![^\\n]*\\s(-n|--dry-run|--just-print)\\b)',
    '\\bcmake\\s+--build\\b',
    '\\b(dotnet|swift)\\s+(test|build)\\b',
    '\\bvalidate[_-]\\w+\\.(py|js|mjs|ts|sh|ps1)\\b'
  ].join('|'),
  'i'
);

const interpreter = /\b(python3?|py|node|bun|deno\s+run|ruby|go\s+run|bash|sh|pwsh|powershell|php|perl|rscript|dotnet\s+run|java)\b/i;

function project(input) {
  return process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();
}

function inProject(file, input) {
  const root = path.resolve(project(input));
  const rel = path.relative(root, path.resolve(root, file));
  return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel);
}

function editedFiles(input) {
  const ti = input.tool_input || {};
  const files = [];
  for (const key of ['file_path', 'path', 'notebook_path']) if (ti[key]) files.push(String(ti[key]));
  const patch = String(ti.patch || ti.input || (input.tool_name === 'apply_patch' ? ti.command || '' : ''));
  for (const m of patch.matchAll(/^\*\*\* (?:Add|Update) File: (.+)$/gm)) files.push(m[1].trim());
  return files.filter((f) => codeExt.test(f) && inProject(f, input));
}

const readers = /^(git|cat|less|more|head|tail|type|echo|printf|rg|grep|findstr|select-string|find|ls|dir|sed|awk|wc|diff|code|vim?|nano|open|start)$/i;

function exercises(cmd, files) {
  const unquoted = cmd.replace(/"[^"]*"|'[^']*'/g, '""');
  const segments = unquoted.split(/\r?\n|&&|\|\||;|\|/);
  const ran = segments.some((seg) => {
    const first = (seg.trim().split(/\s+/)[0] || '').replace(/^.*[\\/]/, '').replace(/\.exe$/i, '');
    return first && !readers.test(first) && checkCommand.test(seg);
  });
  if (ran) return true;
  return files.some((f) => {
    const name = path.basename(f);
    const at = cmd.indexOf(name);
    return at > 0 && interpreter.test(cmd.slice(0, at)) && !/^\s*(git|cat|less|head|tail|type|echo|rg|grep)\b/i.test(cmd);
  });
}

function logFile(input) {
  const key = `${input.session_id || 'nosession'}-${input.agent_id || 'main'}`.replace(/[^A-Za-z0-9_-]/g, '_').slice(0, 160);
  return path.join(dataDir, 'sessions', `${key}.checks.jsonl`);
}

function append(file, record) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify(record) + '\n');
}

function events(file) {
  try {
    return fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).map((l) => {
      try {
        return JSON.parse(l);
      } catch (e) {
        return {};
      }
    });
  } catch (e) {
    return [];
  }
}

function status(list) {
  let lastEdit = -1;
  list.forEach((e, i) => {
    if (e.t === 'edit') lastEdit = i;
  });
  if (lastEdit < 0) return null;
  const after = list.slice(lastEdit + 1);
  if (after.some((e) => e.t === 'blocked')) return null;
  const checks = after.filter((e) => e.t === 'check');
  const last = checks[checks.length - 1];
  if (last && last.ok) return null;
  let start = lastEdit;
  for (let i = lastEdit; i >= 0; i--) {
    if (list[i].t === 'check' && list[i].ok) break;
    start = i;
  }
  const files = [...new Set(list.slice(start, lastEdit + 1).filter((e) => e.t === 'edit').flatMap((e) => e.files))];
  return { files, failed: last ? last.cmd : null };
}

run('check-gate', (input) => {
  const event = input.hook_event_name;
  const file = logFile(input);

  if (event === 'PostToolUse' || event === 'PostToolUseFailure') {
    const edited = editedFiles(input);
    if (edited.length) {
      append(file, { t: 'edit', files: edited });
      return null;
    }
    const cmd = shellCommand(input);
    const list = events(file);
    const pending = status(list);
    if (cmd && pending && exercises(cmd, pending.files)) {
      append(file, { t: 'check', ok: event === 'PostToolUse', cmd: cmd.slice(0, 200) });
    }
    return null;
  }

  if (event === 'Stop' || event === 'SubagentStop') {
    if (input.stop_hook_active) return null;
    const pending = status(events(file));
    if (!pending) return null;
    append(file, { t: 'blocked' });
    const names = pending.files.slice(0, 8).map((f) => path.basename(f)).join(', ');
    if (pending.failed) {
      return {
        block:
          `the last check after your edits to ${names} failed: ${pending.failed}. ` +
          `Fix the cause and run it again, or report the failure and what you tried in your reply; this hook will not stop you again for these edits.`
      };
    }
    return {
      block:
        `you changed ${names} and no test, build, type-check, or run of the changed code followed. ` +
        `Run the project's check that exercises this change and report its result. ` +
        `If no check can run here, say which one and why in your reply; this hook will not stop you again for these edits.`
    };
  }
  return null;
});
