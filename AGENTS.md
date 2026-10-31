# cstack

The repository root is the installable plugin. Keep skills, hooks, manifests, scripts, and docs at the root; do not recreate `source/`, `plugins/`, or `general/` layers.

Use the explicitly named skill first. Use `skills/skills-router/SKILL.md` only when several installed skills plausibly apply.

## Work rules

- Read only the instructions and files relevant to the task. Do not scan the whole repository for a small change.
- State the outcome and scope, then execute the smallest complete change. Use a plan only for work that is multi-file, long-running, or risky.
- Inspect `git status` first and preserve unrelated user changes. Do not reset, checkout, or overwrite them.
- Search for the existing target, callers, exports, and configuration before creating a file or parallel implementation. Update the existing path when it owns the behavior.
- Reuse existing code and commands. Do not add a one-off helper, abstraction, fallback, compatibility layer, or scratch file for a single use. If a temporary artifact is necessary, keep it outside the repository and remove it before handoff.
- If a command fails because of permissions or sandbox policy, read the error and use a known writable path. Do not retry random paths or claim a workaround worked without rerunning the real command.
- Do not ask for approval for reversible work already covered by the request. Ask only when the scope or an irreversible external action is genuinely unclear.

## Tests and handoff

- Do not add tests by default. Add or change a test when behavior, a public contract, a bug fix, a parser, a branch, security, or a data-writing path needs regression coverage. Tests verify the implementation; they do not define a workaround.
- Prefer the smallest existing check that proves the real artifact. Do not treat compilation or a green test as proof of user-visible behavior, side effects, cleanup, or security. Inspect the resulting artifact or effect.
- Do not change or delete a test just to make it pass. Report checks that were skipped and why.
- Remove debug output, generated files, temporary fixtures, and one-off scripts before handoff unless the repository explicitly owns them.

Skills listed in `.cstack/upstreams.json` are managed copies. Update them with `python scripts/sync_upstream_skills.py --write`; do not hand-edit them. The sync job runs on schedule and manual dispatch.

Validate a stack change from the repository root:

```powershell
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

Keep hooks fail-open, preserve trust-boundary validation, and do not add code comments unless a tool, compiler, license, public contract, or non-obvious external constraint requires one.
