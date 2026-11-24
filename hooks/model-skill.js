const fs = require('fs');
const path = require('path');
const { pluginRoot, run, appendLog } = require('./lib');

const table = [
  [/fable-5-2|mythos-5-2/, 'if-u-are-fable-5-2'],
  [/opus-5-5/, 'if-u-are-opus-5-5'],
  [/haiku-5-5/, 'if-u-are-haiku-5-5'],
  [/gpt-6-astra/, 'if-u-are-gpt-6-astra'],
  [/gpt-6\.1-sol/, 'if-u-are-gpt-6-1-sol'],
  [/gpt-5\.6-luna/, 'if-u-are-gpt-5-6-luna']
];

const aliases = { haiku: 'claude-haiku-5-5', opus: 'claude-opus-5-5', fable: 'claude-fable-5-2' };
const preloaded = /^cstack:(verifier|researcher|implementer)$/;

function skillFor(model) {
  const id = String(model || '').toLowerCase().replace(/\[.*\]$/, '');
  const full = aliases[id] || id;
  const hit = table.find(([re]) => re.test(full));
  return hit ? hit[1] : null;
}

function modelFor(input) {
  const event = input.hook_event_name;
  if (event === 'PostModelSwitch') return input.to_model;
  if (event === 'SubagentStart') {
    if (preloaded.test(String(input.agent_type || ''))) return null;
    if (input.model) return input.model;
    if (process.env.CLAUDE_CODE_SUBAGENT_MODEL_FORCE === '1') return process.env.CLAUDE_CODE_SUBAGENT_MODEL;
    return null;
  }
  return input.model;
}

run('model-skill', (input) => {
  const model = modelFor(input);
  const skill = skillFor(model);
  if (!skill) return null;
  const file = path.join(pluginRoot, 'skills', skill, 'SKILL.md');
  if (!fs.existsSync(file)) return null;
  const body = fs.readFileSync(file, 'utf8').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
  const text = `The harness reports your model as ${model}. The cstack skill ${skill} follows; apply it for this session and do not open it again.\n\n${body}`;
  if (text.length > 9500) return null;
  appendLog('skill-usage.jsonl', {
    event: input.hook_event_name,
    session_id: input.session_id,
    agent_id: input.agent_id,
    agent_type: input.agent_type,
    via: 'hook',
    skill,
    model
  });
  return { context: text };
});
