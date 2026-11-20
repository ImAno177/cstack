const fs = require('fs');
const os = require('os');
const path = require('path');
const { pluginRoot, run, sessionState, writeJson } = require('./lib');

const every = Math.max(2, parseInt(process.env.CSTACK_REMIND_EVERY || '8', 10) || 8);
const pinLimit = 2000;

function read(file) {
  try {
    return fs.readFileSync(file, 'utf8').trim();
  } catch (e) {
    return '';
  }
}

function pins(input) {
  const project = process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();
  const parts = [
    read(path.join(os.homedir(), '.claude', 'pinned-rules.md')),
    read(path.join(project, '.claude', 'pinned-rules.md'))
  ].filter(Boolean);
  const text = parts.join('\n').slice(0, pinLimit);
  return text ? `Pinned rules the user asked to keep for this work:\n${text}` : '';
}

function rules() {
  return read(path.join(pluginRoot, 'hooks', 'standing-rules.md'));
}

const header = 'Reminder from the cstack hook. It restates rules you already have and adds none.';

run('standing-rules', (input) => {
  const event = input.hook_event_name;
  const pinned = pins(input);

  if (event === 'SessionStart') {
    const source = input.source || 'startup';
    if (source === 'compact') return { context: [header, rules(), pinned].filter(Boolean).join('\n\n') };
    return pinned ? { context: pinned } : null;
  }

  if (event === 'SubagentStart') return pinned ? { context: pinned } : null;

  if (event === 'UserPromptSubmit') {
    const { file, state } = sessionState(input, 'prompts');
    const prompts = (state.prompts || 0) + 1;
    writeJson(file, { ...state, prompts });
    if (prompts % every !== 0) return null;
    return { context: [header, rules(), pinned].filter(Boolean).join('\n\n') };
  }
  return null;
});
