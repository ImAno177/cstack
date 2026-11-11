---
name: swarm
description: Fan out N parallel workers across independent coverage slices or identical race attempts, drain them, and return one evidence-backed report. Use for "swarm this", parallel coverage, audits, races, gauntlets, or exploration. Not for competing designs that need a rubric, a judge, and grafting into one artifact; use `arena`.
---

# Swarm

Keep a task list with one entry per phase: Frame, Fan out, Aggregate, Report. Read [subagents](../default-mode/references/subagents.md) before the first spawn.

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm returns.
2. Choose the shape: partition into slices, race N workers on identical briefs, or mix both. For a race or a mix, declare the selection rule before spawning: `first pass`, `rank all`, or `best-of`.
3. Pick the worker model per [models and diversity](../default-mode/references/subagents.md#models-and-diversity). For a model race, name each arm's model up front.
4. Give each writing worker its own output location. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order), and the worker records both in its result.

## Phase B: Fan out

Start up to three workers at a time (the `multi-agent-workflow` cap) and queue the rest; raise the cap only when the user asks or an earlier measured run justified it. Run each in its own worktree or sandbox when it writes. Every brief stands alone: the goal, scope, exact slice or race arm, how to verify, and what to report. Results use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect lists every issue it can prove, not only the first. Go on with N-1 and note it when a worker drops out. No nested fan-out.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief named, and respawn that worker once; after a second miss, record a gap. A gap is not a pass. For coverage, every required slice needs a result. For a race, apply the declared selection rule. Verify the claims you keep against the real artifacts.

## Phase D: Report

One consolidated report: a result table, one line per issue, gaps and dropouts, and the race rule when used. Do not paste raw worker output, and do not hide an uncovered slice behind an aggregate result.

## Example

Predicate: every package under `packages/` has an audit result. Shape: slices on `<model-a>`. Race rule: none.

| Slice | Result | Evidence |
| --- | --- | --- |
| `packages/api` | PASS | `pytest packages/api` printed `31 passed` at `<sha>` |
| `packages/web` | ISSUES | `npm test --prefix packages/web` fails `login.spec.ts`, expected 200, got 500, at `<sha>` |
| `packages/cli` | BLOCKED | gap: worker timed out twice; not a pass |
