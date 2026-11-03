---
name: multi-agent-workflow
description: Coordinate two or more agents for bounded parallel research, review, or implementation with isolated ownership, explicit handoffs, and independent verification. Use when delegating work; stay direct for short, sequential, or shared-state tasks.
---

# Multi-agent workflow

Use multiple agents only when the work splits into independent, bounded questions. Keep short tasks, ordered steps, and edits to one shared resource in the main agent.

## Delegate

- Split by independent question or ownership boundary. Do not send the same question to several agents unless an independent comparison is the goal.
- Prefer read-only research, review, and validation lanes. Give each agent one goal, the allowed paths, the inputs, the expected output, and a done condition.
- Start with at most three concurrent agents and one delegation level. Increase either cap only when measured quality, latency, and cost justify it; never allow unbounded nested delegation.
- Give every worker a time, retry, and output budget. A worker may not spawn another worker unless the parent explicitly grants a bounded budget.
- Start one unit through kickoff, execution, verification, and handoff before fanning out when the delegation shape is new. This catches a bad brief once instead of multiplying it.
- Every brief names the done predicate, allowed paths, forbidden actions, exact evidence, and the result schema. A worker that cannot name its proof is not ready to start.

## Isolate writes

- Never let parallel agents edit the same working tree, branch, file, or mutable state.
- Give each writing agent its own worktree, branch, or output path. Keep the main agent as the merge owner and apply changes sequentially.
- If the host cannot provide real isolation, keep implementation in one agent and delegate read-only work only.

## Reconcile

- Wait for every spawned agent or mark the missing result incomplete. A clean process exit is not evidence that the task succeeded.
- Require each result to state status, scope, changed paths, commands run, evidence, blockers, and next action. Read it, check its paths and claims against the repository, and resolve contradictions before editing.
- For a code-ready change, assign a verifier who did not write it and who checks the current head. A new head needs a new verdict unless the relevant proof is unchanged and that reuse is explicit.
- Trust the artifact and the proof, not a green checklist or a worker's summary. Drop results with missing evidence and record the gap instead of treating silence as success.
- After merging each write, run the smallest real check. Remove worktrees, scratch files, logs, and generated artifacts that the repository does not own.
- Do not put secrets or unnecessary user data in prompts, shared outputs, or handoff files.
