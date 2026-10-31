# cstack

Portable cstack skills for ChatGPT, Codex, Grok Build, and Grok Bot.

## Layout

`source/cstack` is the canonical source. `plugins/cstack` is the generated package.

```text
source/cstack/skills/           skill sources
source/cstack/hooks/            shared hook
source/cstack/.codex-plugin/    Codex manifest
source/cstack/.grok-plugin/     Grok manifest
plugins/cstack/                 installable package
.agents/plugins/                Codex marketplace
.grok-plugin/                   Grok marketplace and plugin index
```

## Build and validate

```powershell
python scripts/build_cstack_plugin.py --source-root source/cstack --destination plugins/cstack --policy .cstack/skill-policy.json
python scripts/validate_plugin.py --root plugins/cstack
python scripts/validate_skill_stack.py --source-root source/cstack --plugin-root plugins/cstack --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

## Install

Codex:

```powershell
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add cstack@cstack
```

Grok Build:

```powershell
grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

Grok Bot uses the same marketplace and skills. Refresh the plugin after a new release.

## CI

`.github/workflows/build-cstack-plugin.yml` builds the package, validates the skills, and regenerates `.grok-plugin/plugin-index.json`.

The workflow commits generated files on pushes to `main`.
