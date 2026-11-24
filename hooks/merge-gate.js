const path = require('path');
const { dataDir, run, readJson, shellCommand } = require('./lib');

const verdictDir = path.join(dataDir, 'verdicts');
const slash = (s) => String(s).replace(/\\/g, '/').toLowerCase();
const verdictRef = /(claude_plugin_data|plugin_data|plugins\/+data\/+cstack[^\s'"]*)[^\s'"]*\/+verdicts\b/i;

function touchesVerdicts(input) {
  const ti = input.tool_input || {};
  const dir = slash(path.resolve(verdictDir));
  const target = ti.file_path || ti.path || ti.notebook_path;
  if (target && slash(path.resolve(String(target))).startsWith(dir + '/')) return true;
  const text = slash([shellCommand(input), ti.patch || '', ti.input || ''].join('\n'));
  if (text.includes(dir) || verdictRef.test(text) || /verdict-record/.test(text)) return true;
  return /verdicts/.test(text) && /plugin_data|plugins\/+data|cstack|datadir/.test(text);
}

const ghMerge = /(?:^|[\s;&|(`"'\/\\])gh(?:\.exe)?["']?\s+pr\s+merge\b([^\n;&|)`]*)/i;
const apiMerge = /(?:\bgh(?:\.exe)?["']?\s+api\b|api\.github\.com)[^\n]*?\/pulls\/\d+\/merge\b([^\n]*)/i;

function check(sha, how) {
  if (!sha) return `${how} without the full 40-character SHA the verifier checked. Use gh pr merge <n> --squash --match-head-commit <sha>.`;
  const record = readJson(path.join(verdictDir, sha + '.json'), null);
  if (!record) {
    return `no verifier verdict is recorded for ${sha}. Start a verifier subagent on this exact head; its report must contain "Head: ${sha}" and end with a VERDICT line. A verdict covers one commit.`;
  }
  if (record.verdict !== 'PASS' && record.verdict !== 'PASS+NOTES') {
    return `the recorded verifier verdict for ${sha} is ${record.verdict || 'unreadable'}. Fix the problems, push, and verify the new head.`;
  }
  return null;
}

function shaIn(text, flag) {
  const values = [...String(text).matchAll(new RegExp(`${flag}(?:\\s+|=|:)\\s*([0-9a-fA-F]{7,64})?`, 'g'))].map((m) =>
    (m[1] || '').toLowerCase()
  );
  if (values.length !== 1) return { sha: null, many: values.length > 1 };
  return { sha: /^[0-9a-f]{40}$/.test(values[0]) ? values[0] : null, many: false };
}

const wrapperBefore = /(?:\s-c|\s-command|\s-encodedcommand|\s-e)\s*$/i;

function normalize(cmd) {
  let out = '';
  let last = 0;
  for (const m of cmd.matchAll(/"([^"]*)"|'([^']*)'/g)) {
    const content = m[1] !== undefined ? m[1] : m[2];
    const before = cmd.slice(last, m.index);
    out += before;
    if (/(^|[\\/])gh(\.exe)?$/i.test(content.trim())) out += 'gh';
    else if (/^(--?[\w-]+|[0-9a-fA-F]{7,64}|\d+)$/.test(content.trim())) out += content.trim();
    else if (wrapperBefore.test(out)) out += ` ${normalize(content)} `;
    else out += '""';
    last = m.index + m[0].length;
  }
  return out + cmd.slice(last);
}

const dataOnlyCommands = new Set(['git', 'echo', 'printf', 'cat', 'tee', 'gh']);

function withoutHeredocBodies(cmd) {
  return cmd.replace(/<<-?\s*(['"]?)(\w+)\1([^\n]*)\n[\s\S]*?\n\s*\2\s*(?=\n|$)/g, '<<$2$3');
}

function onlyDataCommands(cmd) {
  const unquoted = withoutHeredocBodies(cmd).replace(/"(?:[^"\\]|\\.)*"|'[^']*'/g, '""');
  if (/`|\$\(|<\(/.test(unquoted) || /`|\$\(/.test(cmd.replace(/'[^']*'/g, "''"))) return false;
  return unquoted
    .split(/\r?\n|&&|\|\||;|\||&/)
    .map((seg) => (seg.trim().split(/\s+/)[0] || '').replace(/^.*[\\/]/, '').replace(/\.exe$/i, '').toLowerCase())
    .filter(Boolean)
    .every((word) => dataOnlyCommands.has(word));
}

function shellReason(raw) {
  const cmd = normalize(withoutHeredocBodies(raw));
  const literal = raw.replace(/\\(["'])/g, '$1');
  if (!ghMerge.test(cmd) && (ghMerge.test(literal) || apiMerge.test(literal)) && !onlyDataCommands(raw)) {
    const found = shaIn(literal, '(?:--match-head-commit|\\bsha)');
    if (found.many) return 'name the head SHA exactly once, with the SHA the verifier checked.';
    return check(found.sha, 'merging through another program');
  }
  const merge = cmd.match(ghMerge);
  if (merge && !/(^|\s)(--help|-h)(\s|$)/.test(merge[1])) {
    const found = shaIn(merge[1], '--match-head-commit');
    if (found.many) return 'name --match-head-commit exactly once, with the SHA the verifier checked.';
    return check(found.sha, 'merging');
  }
  const api = cmd.match(apiMerge);
  if (api) {
    const found = shaIn(cmd, '\\bsha');
    if (found.many) return 'name the sha parameter exactly once, with the SHA the verifier checked.';
    return check(found.sha, 'merging through the API');
  }
  return null;
}

run('merge-gate', (input) => {
  if (touchesVerdicts(input)) {
    return { block: 'verdict records are written only by the verdict hook from a verifier report. Run a verifier instead of editing them.' };
  }
  const tool = String(input.tool_name || '');
  if (/^mcp__.*merge_?pull_?request/i.test(tool)) {
    const ti = input.tool_input || {};
    const sha = String(ti.sha || ti.expected_head_sha || ti.expectedHeadSha || '').toLowerCase();
    return (r => (r ? { block: r } : null))(check(/^[0-9a-f]{40}$/.test(sha) ? sha : null, 'merging through MCP'));
  }
  const cmd = shellCommand(input);
  if (!cmd) return null;
  const reason = shellReason(cmd);
  return reason ? { block: reason } : null;
});
