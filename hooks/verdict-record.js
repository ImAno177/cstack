const path = require('path');
const { dataDir, run, writeJson } = require('./lib');

function parse(text) {
  const lines = String(text || '').split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (!lines.length) return null;
  const m = lines[lines.length - 1].match(/^VERDICT:\s*(PASS\+NOTES|PASS|FAIL)$/);
  if (!m) return null;
  const sha = String(text).match(/\b[0-9a-f]{40}\b/);
  return { verdict: m[1], sha: sha ? sha[0] : null };
}

run('verdict-record', (input) => {
  const event = input.hook_event_name;
  const handback = input.tool_name === 'SubagentHandback';
  const text = handback ? (input.tool_input || {}).message : input.last_assistant_message;
  const found = parse(text);

  if (event === 'PreToolUse') {
    if (handback && /(^|:)verifier$/.test(String(input.agent_type || '')) && (!found || !found.sha)) {
      return {
        block:
          'a verifier report must name the full 40-character head SHA it checked and end with exactly one line: VERDICT: PASS, VERDICT: PASS+NOTES, or VERDICT: FAIL. Add both and deliver the report again.'
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
