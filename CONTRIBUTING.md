# Contributing to cstack

This file is for people changing this repository. Users install the plugins under `plugins/`; `AGENTS.md` is the cross-project instruction file they can import.

## Before you change anything

- Read [README.md](README.md) for the layout and [docs/architecture.md](docs/architecture.md) for why it is shaped this way.
- Check `git status` and keep unrelated changes out of your commits. Stage paths explicitly.

## Add or change a skill

1. Pick the plugin by audience: `cstack` for engineering workflow, `cstack-harness` for building and running agents, `cstack-research` for research and ML. Put the skill at `plugins/<plugin>/skills/<name>/SKILL.md`; the folder name is the skill name.
2. Decide whether the model should pick the skill on its own. A workflow the user starts on purpose sets `disable-model-invocation: true` and is linked from `default-mode` or another listed skill. Each plugin may list at most `max_listed_skills_per_plugin` skills (`.cstack/skill-policy.json`); when a new skill would exceed it, merge an overlapping skill or make one user-started first.
3. Write the description in the third person: what the skill does, when to use it, and when to use a named sibling instead. At most 1,024 characters. When it overlaps a listed skill, add both to an `overlap_groups` entry.
4. Keep the entrypoint under `max_entry_lines` lines. Move detail to `references/` one level deep and deterministic steps to `scripts/`.
5. Link only to files inside the same plugin. Name a skill from another plugin in text, with its plugin, instead of linking to it.
6. Run `python scripts/build_manifests.py`, because the Grok index lists every skill description.
7. Before you claim the skill helps, run it: see [docs/skill-effect-benchmark.md](docs/skill-effect-benchmark.md).

Do not copy another project's published skills into this repository. Link to them from the README instead. A skill adapted from another project keeps its license notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) or in the skill folder.

## Add a plugin

Add an entry to `.cstack/catalog.json`, create `plugins/<name>/skills/`, and run `python scripts/build_manifests.py`. `validate_plugin.py` fails when the catalog and the `plugins/` folders disagree.

## Validate before a pull request

Run the same checks as `.github/workflows/validate-cstack.yml`:

```sh
python scripts/build_manifests.py --check
python scripts/validate_plugin.py
python scripts/validate_skill_stack.py
python -m unittest discover -s tests -p 'test_*.py'
python -m py_compile benchmarks/reproduction/run_codex_ab.py benchmarks/reproduction/micrograd/grade.py
```

The Python dependency is `pyyaml`; the hook tests need Node.js. Run `claude plugin validate plugins/<plugin>` when Claude Code is installed.

## Rules the validators enforce

- Skill names are lowercase kebab-case, at most 64 characters, unique across all plugins, and equal to their folder name. Every `SKILL.md` sits at `skills/<name>/SKILL.md`.
- Descriptions are non-empty and at most 1,024 characters.
- Each plugin lists no more than the policy's limit of model-invoked skills.
- Skills in an `overlap_groups` entry name each other in their descriptions.
- Internal links resolve and stay inside their plugin.
- Skill files do not contain the host-specific markers listed in the policy.
- Generated manifests match `.cstack/catalog.json`.
- Every hook command in `hooks.json` points at an existing script, and every agent's preloaded skill exists in its plugin.

## Changelog

Update [CHANGELOG.md](CHANGELOG.md) for user-visible skill behavior, manifests, agents, hooks, validators, or CI. One line per change.
