# Platform adapters

The portable plugin package is `plugins/cstack`. Platform adapters publish or reference that package without changing its skills.

ChatGPT and Codex use `plugin.json` and `skills/`. Grok Bot uses `.grok-plugin/marketplace.json` and the same generated skills directory. Future adapters can add their marketplace metadata here while keeping one generated skill payload.
