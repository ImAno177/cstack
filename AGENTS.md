# cstack

The repository root is the installable plugin. Keep grouped skills, hooks, manifests, scripts, and docs at the root; do not recreate `source/`, `plugins/`, or `general/` layers.

Use the explicitly named skill first. Use `skills/agent/skills-router/SKILL.md` only when several installed skills plausibly apply. Never auto-route `tdd`.

Skills listed in `.cstack/upstreams.json` are managed copies. Update them with `python scripts/sync_upstream_skills.py --write`; do not hand-edit them. The sync job runs on schedule and manual dispatch.

Validate a stack change from the repository root:

```powershell
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

Keep hooks fail-open, preserve trust-boundary validation, and do not add code comments unless a tool, compiler, license, public contract, or non-obvious external constraint requires one.
