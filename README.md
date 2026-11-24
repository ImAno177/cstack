# cstack

Portable cstack plugin for ChatGPT, Codex, Grok Build, Grok Bot, and Claude Code.

## Layout

The repository root is the canonical, installable plugin.

```text
skills/                         canonical skills, with platform groups where useful
.codex-plugin/                  Codex manifest
.grok-plugin/                   Grok manifest, marketplace, and index
.claude-plugin/                 Claude Code manifest and marketplace
agents/                         Claude Code subagents (verifier, researcher, implementer)
hooks/                          enforcement hooks (Claude Code, Codex, Grok Build)
.cstack/                        routing policy, upstream manifest, and generated lock
.agents/plugins/                Codex marketplace
```

Portable workflow control lives in `skills/default-mode/`. Its `SKILL.md` is the entrypoint; `playbooks/` contains short, task-shaped operating modes. `skills/agent-harness/` covers model loops and runtime boundaries. Every skill lives at `skills/<name>/SKILL.md`, the one-level layout that Claude Code, Codex, Cursor, Grok, and the Agent Skills ecosystem all scan, and hosts choose skills from their frontmatter descriptions. There is no router skill and no routing hook.

Resume and diagnosis workflows: `skills/recall/` reconstructs prior work from scoped session and repository records. `default-mode/playbooks/` adds session pickup, safe pause, bounded autonomous runs, metric hillclimbing, live and offline forensics, and visual parity. Each is a task-specific playbook, not a new router. See [the pstack comparison](docs/pstack-audit-2026-11-21.md) for the 58-skill/22-playbook inventory and non-ports.

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

Skills load as `/cstack:<skill>`. Claude Code does not load instruction files from a plugin, so installing cstack does not apply `AGENTS.md`. To use the instructions in every project, add `@~/.claude/plugins/marketplaces/cstack/AGENTS.md` to `~/.claude/CLAUDE.md`. In this repository the root `CLAUDE.md` imports `AGENTS.md`.

cstack lists about 75 skill descriptions. Claude Code gives the listing 1% of the context window and drops the descriptions of the least-used skills when it overflows, which removes the words a request is matched on. Raise the budget in `~/.claude/settings.json` with `"skillListingBudgetFraction": 0.03`, and run `/skill-doctor` to see which skills you never use. Codex has the same limit at 2% (`skills.max_context_tokens`).

Grok Build also reads Claude Code marketplaces, plugins, skills, agents, and instruction files with no extra configuration.

All examples describe the intended host integration; verify installation and native skill discovery on your specific client before reporting support as tested.

## Hooks

Instructions in a prompt are followed probabilistically and fade: prohibitions weaken as a session grows ([arXiv 2604.20911](https://arxiv.org/abs/2604.20911), [arXiv 2605.10039](https://arxiv.org/abs/2605.10039)), and context compaction can drop rules entirely ([arXiv 2606.22528](https://arxiv.org/abs/2606.22528)). `hooks/hooks.json` loads with the plugin and backs the most important rules with code. Each block message says what to do next, because agents recover far more often from a denial that explains itself ([arXiv 2606.25189](https://arxiv.org/abs/2606.25189)).

| Hook | Events | What it does |
| --- | --- | --- |
| `model-skill` | SessionStart, SubagentStart, PostModelSwitch | Injects the `if-u-are-<model>` skill for the model the host reports, so the model does not have to find it. |
| `standing-rules` | SessionStart, SubagentStart, UserPromptSubmit | Re-injects `hooks/standing-rules.md` after every compaction and every 8 prompts (`CSTACK_REMIND_EVERY`, an integer of 2 or more; other values fall back to 8), and pinned rules (up to 2,000 characters per file, cut at a line break with a note) from `.claude/pinned-rules.md` and `~/.claude/pinned-rules.md` (see the `pin-rule` skill). |
| `check-gate` | PostToolUse, PostToolUseFailure, Stop, SubagentStop | Blocks a stop once when code files in the project changed and no test, build, type-check, or interpreter run of the changed file followed, or when the last such check failed. |
| `merge-gate` | PreToolUse | Blocks `gh pr merge` and API or MCP merges unless they name the full head SHA and a verifier recorded `PASS` or `PASS+NOTES` for it; blocks edits to the verdict records. |
| `verdict-record` | PreToolUse, PostToolUse, SubagentStop | Records a verifier's final `VERDICT:` line against the SHA on its `Head:` line. Only agents whose type is in `CSTACK_VERIFIER_AGENTS` (default `verifier`, which matches `cstack:verifier`) count, so an implementer cannot certify its own work. |
| `usage-log` | SessionStart, SubagentStart, PostModelSwitch, PostToolUse | Logs which skills were injected and opened. `python scripts/skill_usage_report.py` summarizes it. |

State and logs live in the plugin data directory (`~/.claude/plugins/data/cstack-cstack/` on Claude Code). Set `CSTACK_HOOKS=off` to turn every hook off, or `CSTACK_HOOKS_DISABLE=check-gate,merge-gate` to turn off named ones. The hooks need Node.js.

Host support differs. Claude Code runs every hook. Codex loads plugin hooks only after you review and trust them in `/hooks`, and has no `PostModelSwitch`. Grok Build reads Claude Code plugin hooks but honors only blocking decisions, so context injection does not reach the model there. Hooks are a guardrail, not a sandbox: a command run from inside a script the agent wrote does not pass through them.

## Upstream synchronization

`.github/workflows/sync-upstream-skills.yml` proposes changes as a pull request rather than pushing directly to `main`. Successful syncs record source commit SHAs and vendored content hashes in `.cstack/upstreams.lock.json`. See [release instructions](docs/releasing.md) for the initial bootstrap, review requirements, and GitHub Actions permissions.

## Routing evaluation

Use the [37-case routing benchmark](docs/routing-benchmark.md) to compare task success, selected skills, tokens, and latency. No model performance improvements are claimed without real repeated runs.

## Reproduction benchmark

The [micrograd A/B benchmark](benchmarks/reproduction/micrograd/README.md) launches two isolated Codex CLI trials concurrently (baseline without cstack vs. with cstack), then scores nine hidden black-box checks. Requires a locally authenticated Codex CLI; results have not yet been collected.

## Release and licensing

Contributor workflow, validator details, and skill rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

`.github/workflows/validate-cstack.yml` runs the root validators and checks the generated Grok plugin index. See [changelog](CHANGELOG.md), [release checklist](docs/releasing.md), [MIT license](LICENSE), and [third-party notices](THIRD_PARTY_NOTICES.md). Bundled upstream skill content may have separate licenses.
