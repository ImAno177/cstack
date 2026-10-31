# cstack

Portable General skills for ChatGPT, Codex, Grok Build, and Grok Bot.

## Layout

`source/general` is the canonical source. `plugins/general` is the generated package.

```text
source/general/skills/          skill sources
source/general/hooks/           shared hook
source/general/.codex-plugin/   Codex manifest
source/general/.grok-plugin/    Grok manifest
plugins/general/                installable package
.agents/plugins/                Codex marketplace
.grok-plugin/                   Grok marketplace and plugin index
```

## Build and validate

```powershell
python scripts/build_general_plugin.py --source-root source/general --destination plugins/general --policy .general/skill-policy.json
python scripts/validate_plugin.py --root plugins/general
python scripts/validate_skill_stack.py --source-root source/general --plugin-root plugins/general --policy .general/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

## Install

Codex:

```powershell
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add general@general
```

Grok Build:

```powershell
grok plugin marketplace add ImAno177/cstack
grok plugin install general --trust
```

Grok Bot uses the same marketplace and skills. Refresh the plugin after a new release.

## CI

`.github/workflows/build-general-plugin.yml` builds the package, validates the skills, and regenerates `.grok-plugin/plugin-index.json`.

The workflow commits generated files on pushes to `main`.
