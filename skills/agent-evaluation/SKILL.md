---
name: agent-evaluation
description: Evaluate an agent workflow across representative repeated tasks using outcome, trajectory, reliability, cost, latency, and cleanup evidence. Use when comparing models, skills, hooks, prompts, or agent configurations; not for a single code test.
---

# Agent evaluation

Evaluate the whole agent and harness, not only its final message.

## Design

- Freeze the model/version, host, tools, prompts, skill set, repository state, permissions, and environment before comparing runs.
- Use representative short, multi-step, long-horizon, recovery, and handoff tasks. Keep the task set fixed while comparing configurations.
- Repeat each task enough to expose variance: use at least three runs, and use five or more when comparing a small difference.
- Define the evaluator and stopping rule before the agent runs. Do not let the candidate change the task set, evaluator, or evidence threshold.
- Compare a baseline against one changed variable at a time when the question is causal. Use an arena only when independent alternatives are the object of the experiment.
- For tool orchestration, compare sequential direct calls with the candidate mode on the same task stream. Freeze concurrency, rate limits, retry policy, and output reduction so the mode is the variable being measured.

## Measure

- Record final correctness, trajectory correctness, tool/argument errors, retries, loops, timeouts, cleanup, latency, tokens, and cost.
- Inspect the actual artifact or state independently of the agent's final answer. Include false-completion and partial-completion rates.
- Report per-task results and aggregate results, including pass@1, repeated-run completion, variance, and failure categories. Do not hide a protected regression behind one average.
- Separate model, harness, environment, task, and verifier failures before changing prompts or skills.
- Treat a self-reported reflection, clean exit, or retrieved memory as a hypothesis; promote it only after an external artifact-based check.
- Count token, tool-call, wall-clock, and storage cost alongside quality. Reject a nominal gain that exceeds the declared budget or hides a protected-task regression.
- Split latency into model, queue, and tool critical-path time. Record cancellation, partial-result, and retry behavior; a shorter wall-clock run is not a gain if it loses evidence or correctness.

## Handoff

- State the verdict, sample size, configuration, evidence, uncertainty, and the next change to test.
- Keep the evaluator outside the agent's write scope and preserve traces or artifacts needed to reproduce a failure.
