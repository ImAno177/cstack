const fs = require('fs');
const os = require('os');
const path = require('path');

const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || process.env.PLUGIN_ROOT || path.resolve(__dirname, '..');
const dataDir =
  process.env.CLAUDE_PLUGIN_DATA ||
  process.env.PLUGIN_DATA ||
  path.join(os.homedir(), '.claude', 'plugins', 'data', 'cstack-cstack');

function disabled(name) {
  if (String(process.env.CSTACK_HOOKS || '').toLowerCase() === 'off') return true;
  const list = String(process.env.CSTACK_HOOKS_DISABLE || '').split(',').map((s) => s.trim());
  return list.includes(name);
}

function run(name, handler) {
  if (disabled(name)) process.exit(0);
  const chunks = [];
  process.stdin.on('data', (c) => chunks.push(c));
  process.stdin.on('end', () => {
    let input;
    try {
      input = JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
    } catch (e) {
      process.exit(0);
    }
    let result;
    try {
      result = handler(input || {});
    } catch (e) {
      process.exit(0);
    }
    if (result && result.block) {
      process.stderr.write(`cstack ${name}: ${result.block}`);
      process.exit(2);
    }
    if (result && result.context) {
      const event = input.hook_event_name || 'SessionStart';
      process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: event, additionalContext: result.context } }));
    }
    process.exit(0);
  });
}

function sessionKey(input) {
  const raw = `${input.session_id || 'nosession'}-${input.agent_id || 'main'}`;
  return raw.replace(/[^A-Za-z0-9_-]/g, '_').slice(0, 160);
}

function readJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    return fallback;
  }
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value));
  fs.renameSync(tmp, file);
}

function sessionState(input, kind) {
  const file = path.join(dataDir, 'sessions', `${sessionKey(input)}.${kind}.json`);
  return { file, state: readJson(file, {}) };
}

function appendLog(name, record) {
  const dir = path.join(dataDir, 'logs');
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(path.join(dir, name), JSON.stringify({ ts: new Date().toISOString(), ...record }) + '\n');
}

function shellCommand(input) {
  const ti = input.tool_input || {};
  return String(ti.command || ti.cmd || '');
}

module.exports = { pluginRoot, dataDir, run, sessionState, writeJson, readJson, appendLog, shellCommand };
