# cstack

Portable cstack plugin for ChatGPT, Codex, Grok Build, Grok Bot, and Claude Code.

## Layout

The repository root is the canonical, installable plugin.

```text
skills/                         canonical skills, with platform groups where useful
.codex-plugin/                  Codex manifest
.grok-plugin/                   Grok manifest, marketplace, and index
.claude-plugin/                 Claude Code manifest and marketplace
.cstack/                        routing policy, upstream manifest, and generated lock
.agents/plugins/                Codex marketplace
```

Portable workflow control lives in `skills/default-mode/`. Its `SKILL.md` is the entrypoint; `playbooks/` contains short, task-shaped operating modes. `skills/agent-harness/` covers model loops and runtime boundaries. Skills are discovered through host-native skill metadata. `skills/skills-router/SKILL.md` is available on demand for ambiguous or cross-domain tasks; no routing hook runs automatically.

Platform groups include `skills/kaggle/`, `skills/colab/`, `skills/huggingface/`, and `skills/cloudflare/`; portable core skills live directly under `skills/`. Only entries declared in `.cstack/upstreams.json` are automatically synchronized.

## Build and validate

```sh
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

## Install

Codex:

```sh
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add cstack@cstack
```

Grok Build:

```sh
grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

Grok Bot uses the same marketplace and skills. Refresh the plugin after a new release.

Claude Code:

```sh
claude plugin marketplace add ImAno177/cstack
claude plugin install cstack@cstack
```

Claude Code only scans `skills/<name>/SKILL.md`, so `.claude-plugin/plugin.json` lists each platform group (`skills/kaggle/`, `skills/cloudflare/`, ...) under `skills`; `validate_plugin.py` fails if a skill is unreachable. Skills load as `/cstack:<skill>`. Claude Code reads `CLAUDE.md`, not `AGENTS.md`: the root `CLAUDE.md` imports `AGENTS.md` for sessions in this repository; to use the instructions everywhere, add `@/path/to/cstack/AGENTS.md` to `~/.claude/CLAUDE.md`.

All examples describe the intended host integration; verify installation and native skill discovery on your specific client before reporting support as tested. cstack does not install or require any lifecycle hooks.

## Upstream synchronization

`.github/workflows/sync-upstream-skills.yml` proposes changes as a pull request rather than pushing directly to `main`. Successful syncs record source commit SHAs and vendored content hashes in `.cstack/upstreams.lock.json`. See [release instructions](docs/releasing.md) for the initial bootstrap, review requirements, and GitHub Actions permissions.

## Routing evaluation

Use the [32-case routing benchmark](docs/routing-benchmark.md) to compare task success, selected skills, tokens, and latency. No model performance improvements are claimed without real repeated runs.

## Reproduction benchmark

The [micrograd A/B benchmark](benchmarks/reproduction/micrograd/README.md) launches two isolated Codex CLI trials concurrently (baseline without cstack vs. with cstack), then scores nine hidden black-box checks. Requires a locally authenticated Codex CLI; results have not yet been collected.

## Release and licensing

`.github/workflows/validate-cstack.yml` runs the root validators and checks the generated Grok plugin index. See [changelog](CHANGELOG.md), [release checklist](docs/releasing.md), [MIT license](LICENSE), and [third-party notices](THIRD_PARTY_NOTICES.md). Bundled upstream skill content may have separate licenses.
