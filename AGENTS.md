# Contributor guidance

This file is for people and agents changing this repository. The skills in `skills/` are the product that users load; this file does not govern how users work.

## Before you change anything

- Read [README.md](README.md) for the layout and [docs/releasing.md](docs/releasing.md) for the release checklist.
- Check `git status` and keep unrelated changes out of your commits. Stage paths explicitly.

## Validate before a pull request

Run the same checks as `.github/workflows/validate-cstack.yml`:

```sh
python scripts/validate_plugin.py --root .
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
python scripts/sync_upstream_skills.py --check
```

Also run `python -m py_compile` on the benchmark scripts and `python benchmarks/reproduction/run_codex_ab.py --help`, as the workflow does. The Python dependency is `pyyaml`.

## Upstream-synced skills are not hand-edited

Skills listed in `.cstack/upstreams.json` are copied from their upstream repositories by the sync workflow. Edit them upstream. A local edit is overwritten by the next sync and fails `sync_upstream_skills.py --check`.

## Keep the hosts in sync

- Declare the version in `plugin.json`, `.codex-plugin/plugin.json`, `.grok-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`. `validate_plugin.py` rejects a mismatch.
- Regenerate `.grok-plugin/plugin-index.json` with `python scripts/generate_grok_plugin_index.py` after any change to a skill description or to a skill's name.
- `agents/` holds Claude Code subagents only. Codex and Grok manifests do not reference it, and the validators do not scan it.
- Claude Code reads the version from `.claude-plugin/plugin.json`. Users receive skill changes only after that version changes.

## Skill rules enforced by the validators

- Every `SKILL.md` has `name` and `description` frontmatter. Skill names are lowercase kebab-case and unique.
- Entrypoints stay within `max_entry_lines` in `.cstack/skill-policy.json`.
- Skills in an `overlap_groups` entry name each other in their descriptions.
- Skill files must not contain the host-specific markers listed in the policy.
- Internal links must resolve.

Write descriptions that say when to use the skill, and when not to, in concrete terms.

## Changes that need a changelog entry

Update [CHANGELOG.md](CHANGELOG.md) for user-visible skill behaviour, manifests, agents, validators, or CI. Describe the change in one line per item.
