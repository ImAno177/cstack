const fs = require("fs");
const path = require("path");

try {
  const root = path.join(__dirname, "..", "skills", "agent");
  const files = ["poteto-mode/SKILL.md", "skills-router/SKILL.md"];
  const context = files.map((file) => fs.readFileSync(path.join(root, file), "utf8").replace(/^---[\s\S]*?---\s*/, "")).join("\n\n---\n\n");
  const activeContext = `CSTACK DEFAULT WORKFLOW ACTIVE\n\n${context}`;
  if (process.env.PLUGIN_DATA) {
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: activeContext } }));
  } else if (process.env.GROK_PLUGIN_ROOT || process.env.GROK_HOOK_EVENT) {
    process.exitCode = 0;
  } else {
    process.stdout.write(activeContext);
  }
} catch {
  process.exitCode = 0;
}
