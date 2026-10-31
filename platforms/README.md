# Platform adapters

The portable plugin package is `plugins/general`. Platform adapters publish or reference that package without changing its skills.

ChatGPT and Codex use `plugin.json` and `skills/`. Grok Build and Grok Bot use `.grok-plugin/marketplace.json`, `plugins/general/.grok-plugin/plugin.json`, and the same generated `skills/` directory. Future adapters can add their marketplace metadata here while keeping one generated skill payload.
