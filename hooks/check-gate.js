const path = require('path');
const { run, sessionState, writeJson, shellCommand } = require('./lib');

const codeExt = /\.(c|cc|cpp|cs|cjs|cts|dart|ex|exs|go|gradle|h|hpp|java|js|jsx|kt|kts|lua|m|mjs|mts|php|ps1|py|rb|rs|scala|sh|svelte|swift|ts|tsx|vue|zig)$/i;

const checkCommand = new RegExp(
  [
    '\\b(pytest|unittest|tox|nox|mypy|pyright|ruff|py_compile|compileall)\\b',
    '\\b(jest|vitest|mocha|ava|playwright|cypress|eslint|biome|tsc)\\b',
    '\\b(npm|pnpm|yarn|bun)\\s+(test|t|run\\s+\\S+|build|lint|typecheck|check)\\b',
    '\\bnode\\s+--test\\b',
    '\\b(deno)\\s+(test|check|lint)\\b',
    '\\bgo\\s+(test|build|vet)\\b',
    '\\bcargo\\s+(test|build|check|clippy|nextest)\\b',
    '\\b(gradlew?|mvnw?|make|ctest|bazel|buck2?|xcodebuild|phpunit|rspec|rake)\\b',
    '\\bcmake\\s+--build\\b',
    '\\b(dotnet|swift)\\s+(test|build)\\b',
    '\\bvalidate[_-]?\\w*'
  ].join('|'),
  'i'
);

function inProject(file, input) {
  const project = process.env.CLAUDE_PROJECT_DIR || input.cwd;
  if (!project || !path.isAbsolute(file)) return true;
  const rel = path.relative(path.resolve(project), path.resolve(file));
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

function exercisesEdit(cmd, files) {
  if (checkCommand.test(cmd)) return true;
  return files.some((f) => {
    const name = path.basename(f);
    return name.length > 3 && cmd.includes(name);
  });
}

run('check-gate', (input) => {
  const event = input.hook_event_name;
  const { file, state } = sessionState(input, 'checks');
  const files = state.files || [];

  if (event === 'PostToolUse' || event === 'PostToolUseFailure') {
    const edited = editedFiles(input);
    if (edited.length) {
      const next = { ...state, seq: (state.seq || 0) + 1, dirty: true, files: [...new Set([...files, ...edited])].slice(-20) };
      writeJson(file, next);
      return null;
    }
    const cmd = shellCommand(input);
    if (cmd && state.dirty && exercisesEdit(cmd, files)) {
      writeJson(file, { ...state, dirty: false, files: [], lastCheck: cmd.slice(0, 200), lastCheckFailed: event === 'PostToolUseFailure' });
    }
    return null;
  }

  if (event === 'Stop' || event === 'SubagentStop') {
    if (input.stop_hook_active) return null;
    if (!state.dirty || state.blockedSeq === state.seq) return null;
    writeJson(file, { ...state, blockedSeq: state.seq });
    const list = files.slice(0, 5).map((f) => path.basename(f)).join(', ');
    return {
      block:
        `you changed ${list} and no test, build, type-check, or run of the changed code followed. ` +
        `Run the project's check that exercises this change and report its result. ` +
        `If no check can run here, say which one and why in your reply; this hook will not stop you again for these edits.`
    };
  }
  return null;
});
