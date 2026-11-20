const path = require('path');
const { dataDir, run, writeJson } = require('./lib');

const verifierTypes = String(process.env.CSTACK_VERIFIER_AGENTS || 'verifier')
  .split(',')
  .map((s) => s.trim().toLowerCase())
  .filter(Boolean);

function isVerifier(agentType) {
  const type = String(agentType || '').toLowerCase();
  const bare = type.split(':').pop();
  return verifierTypes.includes(type) || verifierTypes.includes(bare);
}

function headSha(text) {
  const labeled = String(text).match(/^\W*head(?:\s+sha)?\W*\s*([0-9a-f]{40})\b/im);
  if (labeled) return labeled[1];
  const all = [...new Set(String(text).match(/\b[0-9a-f]{40}\b/g) || [])];
  return all.length === 1 ? all[0] : null;
}

function parse(text) {
  const lines = String(text || '').split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (!lines.length) return null;
  const m = lines[lines.length - 1].match(/^VERDICT:\s*(PASS\+NOTES|PASS|FAIL)$/);
  if (!m) return null;
  return { verdict: m[1], sha: headSha(text) };
}

run('verdict-record', (input) => {
  const event = input.hook_event_name;
  const handback = input.tool_name === 'SubagentHandback';
  if (!isVerifier(input.agent_type)) return null;
  const text = handback ? (input.tool_input || {}).message : input.last_assistant_message;
  const found = parse(text);

  if (event === 'PreToolUse') {
    if (handback && (!found || !found.sha)) {
      return {
        block:
          'a verifier report must contain a line "Head: <full 40-character SHA you checked>" and end with exactly one line: VERDICT: PASS, VERDICT: PASS+NOTES, or VERDICT: FAIL. Add both and deliver the report again.'
      };
    }
    return null;
  }

  if (!found || !found.sha || !input.agent_id) return null;
  writeJson(path.join(dataDir, 'verdicts', found.sha + '.json'), {
    verdict: found.verdict,
    ts: new Date().toISOString(),
    session_id: input.session_id,
    agent_id: input.agent_id,
    agent_type: input.agent_type,
    source: handback ? 'SubagentHandback' : event
  });
  return null;
});
