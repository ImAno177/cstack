const { run, appendLog } = require('./lib');

run('usage-log', (input) => {
  const base = {
    event: input.hook_event_name,
    session_id: input.session_id,
    agent_id: input.agent_id,
    agent_type: input.agent_type
  };
  const ti = input.tool_input || {};
  const event = input.hook_event_name;

  if (event === 'SessionStart') appendLog('skill-usage.jsonl', { ...base, source: input.source, model: input.model });
  else if (event === 'PostModelSwitch') appendLog('skill-usage.jsonl', { ...base, source: input.source, model: input.to_model });
  else if (event === 'SubagentStart') appendLog('skill-usage.jsonl', { ...base, model: input.model });
  else if (input.tool_name === 'Skill' && ti.skill) appendLog('skill-usage.jsonl', { ...base, via: 'Skill', skill: String(ti.skill) });
  else if (input.tool_name === 'Read' && ti.file_path) {
    const m = String(ti.file_path).replace(/\\/g, '/').match(/\/skills\/([^/]+)\/SKILL\.md$/i);
    if (m) appendLog('skill-usage.jsonl', { ...base, via: 'Read', skill: m[1] });
  }
  return null;
});
