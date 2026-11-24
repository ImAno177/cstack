# Skill effect benchmark

The routing evals (`docs/routing-evals.md`) check which skill a description selects. This protocol checks whether a skill or rule change makes an agent produce better work. Use it before keeping a new skill, a large rewrite, or a deletion.

## Why paired, repeated runs

- One run is not a measurement. The same harness measured twice on the same tasks moved by about 3 points ([Cortex, arXiv 2610.14216](https://arxiv.org/abs/2610.14216)).
- The same skill helped on one model–harness pair and hurt on another in 37% of SkillsBench tasks ([arXiv 2610.08875](https://arxiv.org/abs/2610.08875)).
- A same-job skill that is also installed takes about one run in five away from the intended skill, and the task still passes. Score the skill's own requirements, not only task success ([arXiv 2610.11647](https://arxiv.org/abs/2610.11647)).
- A skill the agent never opens cannot be credited or blamed. Listed-only skills are rarely opened, so record exposure ([Cortex](https://arxiv.org/abs/2610.14216)).

## Protocol

1. Fix the model, harness version, and task set. Write each task's checks before the first run, including the skill's exclusive requirements (rules a capable model would not follow without the skill).
2. Run every task `k ≥ 3` times in each arm: `baseline` (live harness) and `candidate` (live harness plus or minus the one change). Interleave arms so drift lands on both.
3. Record per run: task pass, each requirement check, tokens, wall time, and which skill files were opened.
4. Compare arms task by task. Keep a change only when it fired in at least one run, raises the mean, and makes no task that never failed start failing. Delete an item only when it fired and removing it lost nothing measurable; keep any item that never fired.
5. Re-run after every model change: a stronger model may already do what a skill teaches.

## Claude Code

`claude plugin eval` (Claude Code v2.1.269 or later) runs this protocol on Claude Code: each case runs three times by default with the plugin and again with no plugin, and the report gives both scores and their difference. Create a suite with `claude plugin eval init` from the repository root; cases live in `evals/`. Every run is a billed model call. cstack does not ship a suite yet, so no Claude Code result is claimed here.

`/skill-doctor` reports what each skill costs in the always-on listing and how often it was invoked. Use it before adding a skill, and to pick skills to mark `disable-model-invocation`.

## Exposure from the hooks

`plugins/cstack/hooks/usage-log.js` records each skill the agent opens (through the Skill tool or a read of its `SKILL.md`) and each skill `plugins/cstack/hooks/model-skill.js` injects. `python scripts/skill_usage_report.py` prints both and the listed skills never opened. ACES scores the same thing as the activation check of its skill-execution metric: did the agent read the expected `SKILL.md` ([arXiv 2608.20614](https://arxiv.org/abs/2608.20614)). A skill the agent never reads has no effect to measure.

## What a result of this size can show

- Score instruction following and goal completion separately. With a relevant skill, goal completion is near its ceiling for most models while the overall score rises by 5.5 to 22 points, mostly from instruction following, and smaller models gain more ([arXiv 2606.17819](https://arxiv.org/abs/2606.17819)).
- A held-out split of 20 to 26 tasks detects a skill effect only when the skill wins about four of every five tasks where the two arms disagree; pooled over 69 tasks, about two of three ([arXiv 2609.12742](https://arxiv.org/abs/2609.12742)). A few-point gain on fewer tasks is inside the agent's own variance.
- Visible skill count costs time and success: lift held for 1 to 20 visible skills while wall time nearly doubled, and with 50 visible skills the with-skill pass rate fell from 0.725 to 0.55 ([arXiv 2608.20614](https://arxiv.org/abs/2608.20614)).
- Context files are followed but raise cost: in one study they increased steps and cost by about 20% without a significant change in task success, and repository overviews did not reduce the steps agents took to reach a relevant file ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988)). Add to `AGENTS.md` only what the repository and the model cannot supply.
- Measure compliance across a long session, not only at the start: compliance drops as the agent writes more code within one session ([arXiv 2605.10039](https://arxiv.org/abs/2605.10039)).

## Runner

`benchmarks/reproduction/run_codex_ab.py` runs paired, repeated arms on Codex for the micrograd fixture. Its arms are no skills versus the whole pack, so it measures the pack, not one change; to test one change, stage two cstack checkouts that differ only in that change and compare their results the same way:

```
python benchmarks/reproduction/run_codex_ab.py --model <model> --runs 3 --output /tmp/cstack-ab-<date>
```

It writes `results.json` with each run's grade, tokens, and `skills_opened` (skills whose `SKILL.md` a shell command read by explicit path; listings and globs do not count), and prints the per-pair deltas. Add a fixture under `benchmarks/reproduction/<task>/` with `TASK.md` and a grader that reads the workspace only after the agent exits.
