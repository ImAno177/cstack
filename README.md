# cstack

Portable cstack plugin for ChatGPT, Codex, Grok Build, and Grok Bot.

## Layout

The repository root is the canonical, installable plugin.

```text
skills/                         canonical skills, with platform groups where useful
hooks/                          host-specific hook configs and shared runtime
.codex-plugin/                  Codex manifest
.grok-plugin/                   Grok manifest, marketplace, and index
.cstack/                        routing policy and upstream manifest
.agents/plugins/                Codex marketplace
```

Platform groups include `skills/kaggle/`, `skills/colab/`, `skills/huggingface/`, and `skills/cloudflare/`; portable core skills live directly under `skills/`.

## Build and validate

```powershell
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
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

`.github/workflows/validate-cstack.yml` validates the root plugin and regenerates `.grok-plugin/plugin-index.json`.

`.github/workflows/sync-upstream-skills.yml` refreshes managed skills from their original public repositories on schedule or manual dispatch.
