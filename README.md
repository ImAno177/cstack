# cstack

`cstack` is the repository for the standalone General skills plugin for ChatGPT, Codex, Grok Bot, and compatible agent hosts.

## Data flow

`source/general` is the canonical input. The generated installable payload is `plugins/general`.

```text
source/general/
├── skills/                 canonical skill sources
├── hooks/hooks.json        shared lifecycle hook contract
├── .codex-plugin/          Codex manifest overlay
├── .grok-plugin/           Grok manifest overlay
└── plugin.json             portable plugin metadata
plugins/general/            generated installable package
.agents/plugins/            Codex marketplace catalog
.grok-plugin/               Grok marketplace catalog and generated index
```

The General plugin is rebuilt by GitHub Actions when its source, policy, builder, validator, or package changes. It has no upstream synchronization job; updates are made in this repository and promoted through the generated package.

The academic research set includes PEFT/LoRA/QLoRA, bitsandbytes quantization, TRL, Kaggle CLI, and scientific visualization. Continual learning is a separate special skill with paper notes and an agent-level evaluation protocol.

Test suites and test fixtures are excluded from generated plugin payloads. Testing guidance documents remain available inside the relevant skills.

## Build locally

Build and validate the standalone plugin.

```powershell
python scripts/build_general_plugin.py --source-root source/general --destination plugins/general --policy .general/skill-policy.json
python scripts/validate_plugin.py --root plugins/general
python scripts/validate_skill_stack.py --source-root source/general --plugin-root plugins/general --policy .general/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

## ChatGPT and Codex

Add the repository as a Git-backed marketplace, then install `general` from the plugin directory.

```powershell
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin marketplace upgrade general
```

The ChatGPT desktop app uses the portable `plugin.json`; Codex also reads the generated `.codex-plugin/plugin.json` overlay. The lifecycle hook is declared at `hooks/hooks.json`. A refresh is still required after a new commit because the host controls plugin installation and trust.

## Grok Build and Grok Bot

This repository is a Grok marketplace. Its `.grok-plugin/marketplace.json` is the catalog source of truth and `.grok-plugin/plugin-index.json` is generated from the installable `plugins/general` package. Grok Build receives the host-compatible lifecycle hook; Grok Bot receives the portable skills and does not depend on a lifecycle hook.

Install it with Grok Build:

```powershell
grok plugin marketplace add ImAno177/cstack
grok plugin install general --trust
```

Grok Bot uses the same installed plugin on its bot computer. Refresh the plugin from the Grok plugins/marketplace UI after a new release.

## Automation

The General workflow supports `workflow_dispatch`; ordinary pushes and pull requests to General paths trigger the build automatically.

## Other platforms

The canonical skill payload is the portable `plugins/general/skills` directory. Platform-specific marketplace files can point at that directory without changing the skills themselves. New adapters should live under `platforms/` and must not write into the generated plugin directly.
