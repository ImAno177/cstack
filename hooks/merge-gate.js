const fs = require('fs');
const path = require('path');
const { dataDir, run, readJson, shellCommand } = require('./lib');

const verdictDir = path.join(dataDir, 'verdicts');
const verdictPattern = /[\\/]verdicts([\\/]|$)/i;

function touchesVerdicts(input) {
  const ti = input.tool_input || {};
  const target = String(ti.file_path || ti.path || ti.notebook_path || '');
  if (target && verdictPattern.test(target) && path.resolve(target).startsWith(path.resolve(verdictDir))) return true;
  const patch = String(ti.patch || ti.input || '');
  if (patch && patch.includes(verdictDir.replace(/\\/g, '/'))) return true;
  const cmd = shellCommand(input).replace(/\\/g, '/');
  return cmd !== '' && cmd.includes(verdictDir.replace(/\\/g, '/'));
}

function mergeCheck(cmd) {
  const segments = cmd.split(/\r?\n|&&|\|\||;|\||&/);
  const base = (x) => x.toLowerCase().replace(/^["']|["']$/g, '').replace(/\.(exe|cmd|bat)$/, '');
  for (const seg of segments) {
    const t = seg.trim().split(/\s+/).filter(Boolean);
    const i = t.findIndex((x, k) => base(x) === 'gh' && t[k + 1] === 'pr' && t[k + 2] === 'merge');
    if (i < 0) continue;
    const args = t.slice(i + 3);
    if (args.includes('--help') || args.includes('-h')) continue;
    let sha = '';
    for (let k = 0; k < args.length; k++) {
      if (args[k] === '--match-head-commit') sha = args[k + 1] || '';
      else if (args[k].startsWith('--match-head-commit=')) sha = args[k].slice('--match-head-commit='.length);
    }
    sha = sha.replace(/^["']|["']$/g, '');
    if (!/^[0-9a-f]{40}$/.test(sha)) {
      return 'merge with --match-head-commit and the full 40-character SHA the verifier checked, written literally in the command.';
    }
    const record = readJson(path.join(verdictDir, sha + '.json'), null);
    if (!record) {
      return `no verifier verdict is recorded for ${sha}. Start a verifier subagent on this exact head; its report must name the SHA and end with a VERDICT line. A verdict covers one commit.`;
    }
    if (record.verdict !== 'PASS' && record.verdict !== 'PASS+NOTES') {
      return `the recorded verifier verdict for ${sha} is ${record.verdict || 'unreadable'}. Fix the problems, push, and verify the new head.`;
    }
  }
  return null;
}

run('merge-gate', (input) => {
  if (touchesVerdicts(input)) {
    return { block: 'verdict records are written only by the verdict hook from a verifier report. Run a verifier instead of editing them.' };
  }
  const cmd = shellCommand(input);
  if (!cmd) return null;
  const reason = mergeCheck(cmd);
  return reason ? { block: reason } : null;
});
