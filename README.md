# cstack

Portable cstack plugin for ChatGPT, Codex, Grok Build, and Grok Bot.

## Layout

The repository root is the canonical, installable plugin.

```text
skills/                         canonical skills
packs/cloudflare/               optional Cloudflare skill pack (not in core index)
hooks/                          host-specific hook configs and shared runtime
.codex-plugin/                  Codex manifest
.grok-plugin/                   Grok manifest, marketplace, and index
.cstack/                        routing policy and upstream manifest
.agents/plugins/                Codex marketplace
templates/                      portable agent instruction templates
```

## Install (bash)

```bash
# Codex
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add cstack@cstack

# Grok Build
grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

## Install (PowerShell)

```powershell
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add cstack@cstack

grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

Grok Bot uses the same marketplace and skills. Refresh the plugin after a new release.

## Optional packs → Cloudflare

Core stays lean. Cloudflare Workers, Wrangler, Durable Objects, Email, Zero Trust, Turnstile, Agents SDK, sandbox, and web-perf live in `packs/cloudflare`. Enable steps: see `packs/cloudflare/README.md`.

Grok Bot fleet setup: see https://github.com/ImAno177/botx-setup

`grok-build` was skipped: the workflow source is host- and bot-specific and could not be made portable. Use `poteto-mode` for SDD/TDD.

## Build and validate

```powershell
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

## CI

`.github/workflows/validate-cstack.yml` validates the root plugin and regenerates `.grok-plugin/plugin-index.json`.

`.github/workflows/sync-upstream-skills.yml` refreshes managed skills from their original public repositories on schedule or manual dispatch.
