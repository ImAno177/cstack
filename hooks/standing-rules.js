const fs = require('fs');
const os = require('os');
const path = require('path');
const { pluginRoot, run, sessionState, writeJson } = require('./lib');

const requested = Number(process.env.CSTACK_REMIND_EVERY);
const every = Number.isInteger(requested) && requested >= 2 ? requested : 8;
const pinLimit = 2000;

function capped(text, file) {
  if (text.length <= pinLimit) return text;
  const cut = text.lastIndexOf('\n', pinLimit);
  const kept = text.slice(0, cut > 0 ? cut : 0);
  return `${kept}\n(${text.length - kept.length} more characters in ${file} were not loaded; keep the file under ${pinLimit} characters.)`;
}

function read(file) {
  try {
    return fs.readFileSync(file, 'utf8').trim();
  } catch (e) {
    return '';
  }
}

function pins(input) {
  const project = process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();
  const files = [path.join(project, '.claude', 'pinned-rules.md'), path.join(os.homedir(), '.claude', 'pinned-rules.md')];
  const parts = files.map((f) => [f, read(f)]).filter(([, t]) => t).map(([f, t]) => capped(t, f));
  return parts.length ? `Pinned rules the user asked to keep for this work:\n${parts.join('\n')}` : '';
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
