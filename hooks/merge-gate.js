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
  return text.includes(dir) || verdictRef.test(text);
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
  const m = String(text).match(new RegExp(`${flag}["']?(?:\\s+|=|:)\\s*["']?([0-9a-fA-F]{40})\\b`));
  return m ? m[1].toLowerCase() : null;
}

function shellReason(cmd) {
  const merge = cmd.match(ghMerge);
  if (merge && !/(^|\s)(--help|-h)(\s|$)/.test(merge[1])) {
    return check(shaIn(merge[1], '--match-head-commit'), 'merging');
  }
  const api = cmd.match(apiMerge);
  if (api) return check(shaIn(cmd, '\\bsha'), 'merging through the API');
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
