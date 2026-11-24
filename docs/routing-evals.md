# Routing evals

`evals/routing/` checks whether Claude Code picks the right cstack skill for a realistic request. Each case is a folder that `claude plugin eval` reads ([Test plugins with evals](https://code.claude.com/docs/en/plugin-evals)):

- `prompt.md`: the request as a user would type it, with run settings. Every case loads all three plugins, allows `Read`, `Glob`, `Grep`, and `Skill`, and runs up to 10 turns.
- `graders/routes.md`: a `tool_used` grader on the `Skill` tool. A positive case passes when the expected skill is called at least once. A `negative` case passes when no cstack skill other than `if-u-are-*` is called.
- `case.yaml` and `scaffold.sh`: build the sample repository in `evals/fixtures/shop-repo.sh` (a small Flask shop with history and a feature branch) before the run. In an empty workspace the agent searched, found nothing, and stopped before choosing a skill.

Tags:

| Tag | Cases | Use |
| --- | --- | --- |
| `train` | one per listed skill | Read these failures when you change a description. |
| `test` | one per listed skill, phrased differently | Do not tune against these; they show whether a change generalizes. |
| `via-default-mode` | 4 | Requests for `arena`, `swarm`, `interrogate`, and `figure-it-out`, which are user-started and reached through `default-mode`. |
| `negative` | 8 | Near-miss requests that should trigger no cstack skill. |

`validate_skill_stack.py` fails when a listed skill has no `train` or no `test` case.

## Run

From the repository root:

```sh
claude plugin eval . --eval-dir evals --scaffold --ablation none --model haiku --runs 3 -j 8 --threshold 0 --trust-plugin
```

- `--scaffold` runs each case's `scaffold.sh`, which builds the sample repository; read it before you trust it.
- `--ablation none` skips the no-plugin arm, because a routing grader on `Skill` is only an indicator in a two-arm run.
- Add `--tag test` to run one tag, `--case 'tdd-*'` to run one skill, and `--max-cost-usd` to cap spending.
- Results go to `evals/results/`, which is ignored by Git.

Every run is a real, billed model call. Measured costs per run on 2026-11-24: about $0.006 with Haiku, $0.10 with Sonnet, and $0.34 with Opus.

## Reading a result

A miss is either no skill call or a wrong one. Keep the run's trace (`--keep-temp`) and read which `Skill` calls it made before you change a description. Three runs per case still move by one or two between identical runs, so compare whole tags, not single cases, and confirm a change on the `test` tag.
