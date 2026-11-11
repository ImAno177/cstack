---
name: agent-evaluation
description: Evaluate an agent workflow across representative repeated tasks using outcome, trajectory, reliability, cost, latency, and cleanup evidence. Use when comparing models, skills, hooks, prompts, or agent configurations; not for a single code test. To compare independent alternatives use `arena`; to promote learnings across episodes use `continual-learning`.
---

# Agent evaluation

Evaluate the whole agent and harness, not only its final message.

## Design

- Freeze the model/version, host, tools, prompts, skill set, repository state, permissions, and environment before comparing runs.
- Use representative short, multi-step, long-horizon, recovery, and handoff tasks. Keep the task set fixed while comparing configurations.
- Repeat each task at least three times; use five or more when comparing a small difference.
- Define the evaluator and stopping rule before the agent runs. Keep the candidate from changing the task set, evaluator, or evidence threshold.
- Compare a baseline against one changed variable at a time for causal questions. Use `arena` only when independent alternatives are the object of the experiment.
- For tool orchestration, compare sequential direct calls with the candidate mode on the same task stream. Freeze concurrency, rate limits, retry policy, and output reduction so the mode is the measured variable.

## Measure

- Record final correctness, trajectory correctness, tool/argument errors, retries, loops, timeouts, cleanup, latency, tokens, and cost.
- Inspect the actual artifact or state independently of the agent's final answer. Include false-completion and partial-completion rates.
- Report per-task and aggregate results: pass@1, repeated-run completion, variance, failure categories. Show any protected regression separately from the average.
- Separate model, harness, environment, task, and verifier failures before changing prompts or skills.
- Treat a self-reported reflection, clean exit, or retrieved memory as a hypothesis; promote it only after an external artifact-based check.
- Count token, tool-call, wall-clock, and storage cost alongside quality. Reject a nominal gain that exceeds the declared budget or hides a protected-task regression.
- Split latency into model, queue, and tool critical-path time. Record cancellation, partial-result, and retry behavior; a shorter run that loses evidence or correctness is not a gain.

## Not for

- A single unit or integration test of code; run that test directly.

## Done when

- The report names verdict, sample size, configuration, per-task table, evidence paths, and uncertainty.
- The evaluator sits outside the agent's write scope, and traces or artifacts needed to reproduce each failure are saved.
- Changing the task set, evaluator, or configuration after seeing results invalidates the comparison; mark it inconclusive and rerun.

## If it fails

- When results are noisy or an evaluator is suspect, add runs or fix the evaluator, then rerun the full comparison. Keep thresholds fixed.
- Stop and report inconclusive when variance still exceeds the effect after doubling runs.

## Example report

```
Verdict: candidate B not better than baseline A (inconclusive)
Config: model <id>, host <host>, 12 tasks x 5 runs, evaluator v1 (frozen)
Per-task: A pass@1 0.72, B 0.75; task t07 regressed 0.8 -> 0.4 (protected)
Cost: A 41k tokens/run, B 58k tokens/run
Evidence: <traces dir>/{A,B}/t07-*.json
Next change to test: B with the t07 hook removed
```
