const fs = require("fs");
const path = require("path");

const bootstrap = [
  "CSTACK ROUTING ACTIVE",
  "Use one directly matching installed skill when the task has a clear owner.",
  "Read skills-router only when selection is ambiguous or crosses capabilities.",
  "For non-trivial engineering with no narrower owner, use default-mode.",
  "Use supporting skills only for a required additional output; verify the real result.",
].join("\n");

try {
  const routerPath = path.join(__dirname, "..", "skills", "skills-router", "SKILL.md");
  if (!fs.existsSync(routerPath)) {
    throw new Error(`missing skill router: ${routerPath}`);
  }
  let context = bootstrap;
  if (process.env.CSTACK_ROUTER_MODE === "full") {
    const fullRouter = fs.readFileSync(routerPath, "utf8").replace(/^---[\s\S]*?---\s*/, "");
    context = `CSTACK SKILL ROUTER ACTIVE\n\n${fullRouter}`;
  }
  if (process.env.PLUGIN_DATA) {
    process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: context } }));
  } else {
    process.stdout.write(context);
  }
} catch (error) {
  process.stderr.write(`cstack session hook: ${error.message}\n`);
  process.exitCode = 0;
}
