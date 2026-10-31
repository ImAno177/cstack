const fs = require("fs");
const path = require("path");

try {
  const skill = fs.readFileSync(path.join(__dirname, "..", "skills", "general", "SKILL.md"), "utf8");
  const context = `GENERAL MODE ACTIVE\n\n${skill.replace(/^---[\s\S]*?---\s*/, "")}`;
  if (process.env.PLUGIN_DATA) {
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: context } }));
  } else if (process.env.GROK_PLUGIN_ROOT || process.env.GROK_HOOK_EVENT) {
    process.exitCode = 0;
  } else {
    process.stdout.write(context);
  }
} catch {
  process.exitCode = 0;
}
