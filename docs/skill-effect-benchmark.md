# Skill effect benchmark

The routing benchmark (`docs/routing-benchmark.md`) checks which skill a description selects. This protocol checks whether a skill or rule change makes an agent produce better work. Use it before keeping a new skill, a large rewrite, or a deletion.

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

## Runner

`benchmarks/reproduction/run_codex_ab.py` runs paired, repeated arms on Codex for the micrograd fixture. Its arms are no skills versus the whole pack, so it measures the pack, not one change; to test one change, stage two cstack checkouts that differ only in that change and compare their results the same way:

```
python benchmarks/reproduction/run_codex_ab.py --model <model> --runs 3 --output /tmp/cstack-ab-<date>
```

It writes `results.json` with each run's grade, tokens, and `skills_opened` (skills whose `SKILL.md` a shell command read by explicit path; listings and globs do not count), and prints the per-pair deltas. Add a fixture under `benchmarks/reproduction/<task>/` with `TASK.md` and a grader that reads the workspace only after the agent exits.
