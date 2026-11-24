# cstack

A skill marketplace for coding agents. One repository holds three plugins; install only the ones you need. Claude Code, Codex, Grok Build, Cursor, and any agent that reads [Agent Skills](https://github.com/vercel-labs/skills) can load them.

| Plugin | Install id | What it holds | Skills (listed / total) |
| --- | --- | --- | --- |
| `cstack` | `cstack@cstack` | Engineering workflow: `default-mode` and its task playbooks, test-first fixes, change review and audits, commit and PR conventions, user-started workflows (`/cstack:arena`, `/cstack:swarm`, `/cstack:interrogate`, …), the principles, the verifier, researcher, and implementer subagents, and the enforcement hooks. | 27 / 70 |
| `cstack-harness` | `cstack-harness@cstack` | Building and running agents: harness design, long-run context, completion checks, multi-agent work, tool orchestration, evaluation, prompt and skill audits. | 9 / 9 |
| `cstack-research` | `cstack-research@cstack` | Research and ML: literature reviews with verified citations, scientific figures and slides, Kaggle benchmarks, LoRA fine-tuning, quantization. | 6 / 6 |

"Listed" skills have their description in the model's context on every turn, and the model picks them on its own. The other skills run only when you type them (`/cstack:<name>`) or when a listed skill, usually `default-mode`, links to them. Of the 27 listed in `cstack`, six are the `if-u-are-<model>` skills; each applies to one model only.

## Layout

```text
.cstack/catalog.json        the one source for plugin names, descriptions, and version
plugins/<plugin>/           one installable plugin
  skills/<name>/SKILL.md    one skill per folder, with optional references/ and scripts/
  agents/                   Claude Code subagents (cstack only)
  hooks/                    hooks.json and its Node.js scripts (cstack only)
  .claude-plugin/ .codex-plugin/ .grok-plugin/ .cursor-plugin/   generated host manifests
.claude-plugin/ .agents/plugins/ .grok-plugin/ .cursor-plugin/   generated marketplaces
skills.sh.json              generated skill paths for `npx skills`
AGENTS.md                   cross-project instructions you can import (not loaded by any plugin)
scripts/ tests/ benchmarks/ docs/   repository tooling, not installed
```

Everything an installed plugin needs lives inside its `plugins/<name>/` folder, because hosts copy only that folder. [docs/architecture.md](docs/architecture.md) explains the split and the research behind it.

## Install

Claude Code:

```sh
claude plugin marketplace add ImAno177/cstack
claude plugin install cstack@cstack
claude plugin install cstack-harness@cstack
claude plugin install cstack-research@cstack
```

Skills load as `/cstack:<skill>`, and subagents as `cstack:verifier`, `cstack:researcher`, and `cstack:implementer`. Plugins do not load instruction files, so `AGENTS.md` is not applied by installing. To use it everywhere, add `@~/.claude/plugins/marketplaces/cstack/AGENTS.md` to `~/.claude/CLAUDE.md`.

Codex:

```sh
codex plugin marketplace add ImAno177/cstack --ref main
codex plugin add cstack@cstack
```

Grok Build and Grok Bot:

```sh
grok plugin marketplace add ImAno177/cstack
grok plugin install cstack --trust
```

Grok Build also reads the Claude Code marketplace above.

Cursor: import the repository as a team marketplace (Dashboard, Plugins, Team Marketplaces, Import from Repo); it reads `.cursor-plugin/marketplace.json`. Cursor loads the skills but not the Claude Code hooks.

Other agents (Gemini CLI, OpenCode, GitHub Copilot, and others the `skills` CLI supports) read `skills.sh.json`:

```sh
npx skills add ImAno177/cstack
npx skills add ImAno177/cstack --skill tdd change-review
```

These commands describe the intended integration. Check that skills are discovered on your client before you report a host as supported.

## Skills that moved out

cstack used to copy third-party skills into this repository. Their owners publish them, so install them from the source and get updates directly:

```sh
npx skills add cloudflare/skills
npx skills add huggingface/skills
npx skills add Kaggle/kaggle-cli
npx skills add googlecolab/google-colab-cli
```

Cloudflare and Hugging Face also publish Claude Code, Codex, and Cursor marketplaces in those repositories.

## Hooks

The `cstack` plugin ships `plugins/cstack/hooks/hooks.json`. The hooks back the most important rules with code, because instructions in a prompt fade as a session grows and can be dropped by compaction. Every block message says what to do next.

| Hook | What it does |
| --- | --- |
| `model-skill` | Injects the `if-u-are-<model>` skill for the model the host reports. |
| `standing-rules` | Re-injects `hooks/standing-rules.md` after compaction and every 8 prompts (`CSTACK_REMIND_EVERY`), plus pinned rules from `.claude/pinned-rules.md` and `~/.claude/pinned-rules.md` (see `pin-rule`). |
| `check-gate` | Blocks a stop once when code changed and no test, build, or run of it followed. |
| `merge-gate` | Blocks `gh pr merge` and API or MCP merges unless they name the full head SHA and a verifier recorded `PASS` or `PASS+NOTES` for it. |
| `verdict-record` | Records the final `VERDICT:` line of a `cstack:verifier` report against the SHA on its `Head:` line. |
| `usage-log` | Logs which skills were injected and opened; `python scripts/skill_usage_report.py` summarizes the log. |

`CSTACK_HOOKS=off` turns every hook off, and `CSTACK_HOOKS_DISABLE=check-gate,merge-gate` turns off named ones. The hooks need Node.js. Claude Code runs all of them. Codex runs plugin hooks only after you review and trust them in `/hooks`. Grok Build honors only their blocking decisions. Hooks are a guardrail at the tool layer, not a sandbox.

## Develop

```sh
python scripts/build_manifests.py      # regenerate every host manifest from .cstack/catalog.json
python scripts/validate_plugin.py      # catalog, manifests, skill and agent frontmatter, hook paths
python scripts/validate_skill_stack.py # links, entry size, overlap groups, listing budget per plugin
python -m unittest discover -s tests -p 'test_*.py'
```

CI runs the same commands. [CONTRIBUTING.md](CONTRIBUTING.md) has the rules for adding a skill or a plugin, [docs/releasing.md](docs/releasing.md) the release steps, and [docs/routing-evals.md](docs/routing-evals.md) and [docs/skill-effect-benchmark.md](docs/skill-effect-benchmark.md) how to measure a change.

## License

[MIT](LICENSE). Adapted skills keep their upstream notices; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).
