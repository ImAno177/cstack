# cstack

Portable cstack plugin for ChatGPT, Codex, Grok Build, Grok Bot, and Claude Code.

## Layout

The repository root is the canonical, installable plugin.

```text
skills/                         canonical skills, with platform groups where useful
.codex-plugin/                  Codex manifest
.grok-plugin/                   Grok manifest, marketplace, and index
.claude-plugin/                 Claude Code manifest and marketplace
agents/                         Claude Code subagents (pr-reviewer)
.cstack/                        routing policy, upstream manifest, and generated lock
.agents/plugins/                Codex marketplace
```

Portable workflow control lives in `skills/default-mode/`. Its `SKILL.md` is the entrypoint; `playbooks/` contains short, task-shaped operating modes. `skills/agent-harness/` covers model loops and runtime boundaries. Every skill lives at `skills/<name>/SKILL.md`, the one-level layout that Claude Code, Codex, Cursor, Grok, and the Agent Skills ecosystem all scan, and hosts choose skills from their frontmatter descriptions. There is no router skill and no routing hook.

Third-party skills (Cloudflare, Kaggle, Colab, Hugging Face) are copied verbatim from their upstream repositories by the entries in `.cstack/upstreams.json`; edit them upstream, not here. `validate_plugin.py` fails if any `SKILL.md` is nested deeper than `skills/<name>/`.

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

Grok Bot uses the same marketplace and skills. Grok Build also reads Claude Code marketplaces, so the Claude Code commands below work there too. Refresh the plugin after a new release.

Cursor loads cstack as an [Agent Plugin](https://cursor.com/docs/plugins) (root `plugin.json` plus `skills/`). On a Teams or Enterprise plan, import this repository under **Dashboard → Plugins → Team Marketplaces → Import from Repo**. Otherwise clone it into the local plugin folder and reload the window:

```sh
git clone https://github.com/ImAno177/cstack ~/.cursor/plugins/local/cstack
```

Other agents that read Agent Skills (Gemini CLI, OpenCode, GitHub Copilot, and others supported by the [`skills` CLI](https://github.com/vercel-labs/skills)):

```sh
npx skills add ImAno177/cstack
```

Claude Code:

```sh
claude plugin marketplace add ImAno177/cstack
claude plugin install cstack@cstack
```

Skills load as `/cstack:<skill>`. Claude Code reads `CLAUDE.md`, not `AGENTS.md`: the root `CLAUDE.md` imports `AGENTS.md` for sessions in this repository; to use the instructions everywhere, add `@/path/to/cstack/AGENTS.md` to `~/.claude/CLAUDE.md`.

All examples describe the intended host integration; verify installation and native skill discovery on your specific client before reporting support as tested. cstack does not install or require any lifecycle hooks.

## Upstream synchronization

`.github/workflows/sync-upstream-skills.yml` proposes changes as a pull request rather than pushing directly to `main`. Successful syncs record source commit SHAs and vendored content hashes in `.cstack/upstreams.lock.json`. See [release instructions](docs/releasing.md) for the initial bootstrap, review requirements, and GitHub Actions permissions.

## Routing evaluation

Use the [37-case routing benchmark](docs/routing-benchmark.md) to compare task success, selected skills, tokens, and latency. No model performance improvements are claimed without real repeated runs.

## Reproduction benchmark

The [micrograd A/B benchmark](benchmarks/reproduction/micrograd/README.md) launches two isolated Codex CLI trials concurrently (baseline without cstack vs. with cstack), then scores nine hidden black-box checks. Requires a locally authenticated Codex CLI; results have not yet been collected.

## Release and licensing

Contributor workflow, validator details, and skill rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

`.github/workflows/validate-cstack.yml` runs the root validators and checks the generated Grok plugin index. See [changelog](CHANGELOG.md), [release checklist](docs/releasing.md), [MIT license](LICENSE), and [third-party notices](THIRD_PARTY_NOTICES.md). Bundled upstream skill content may have separate licenses.
