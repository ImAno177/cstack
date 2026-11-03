const fs = require("fs");
const path = require("path");

try {
  const skill = fs.readFileSync(path.join(__dirname, "..", "skills", "skills-router", "SKILL.md"), "utf8");
  const context = `CSTACK SKILL ROUTER ACTIVE\n\n${skill.replace(/^---[\s\S]*?---\s*/, "")}`;
  if (process.env.PLUGIN_DATA) {
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: context } }));
  } else {
    process.stdout.write(context);
  }
} catch {
  process.exitCode = 0;
}
