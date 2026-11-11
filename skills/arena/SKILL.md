---
name: arena
description: Run N parallel candidates at the same task against a declared rubric, cross-judge them, pick a base, and graft the strongest parts of the losers into it. Use for "arena this", design bakeoffs, or when one attempt at a non-trivial artifact would lock in the wrong shape. The result is one synthesized artifact. Not for coverage or mechanical races that return a report; use `swarm`.
---

# Arena

Use an arena only when the candidates are competing designs for the same artifact, judged independently against a rubric, and the comparison is worth the extra work. Use `swarm` instead to split work into slices or to race identical attempts under a mechanical rule (first pass, best score); swarm returns a report and never grafts. Keep a task list with one entry per phase: Frame, Fan out, Cross-judge, Pick, Graft, Verify. Read [subagents](../default-mode/references/subagents.md) before the first spawn.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate produces.
2. Derive the rubric: 3-6 concrete, gradeable criteria for success on this task. It is the picker's tool in Phase D; candidates see only the task.
3. Pick the runners: at least two, across model families when the host offers them (see [models and diversity](../default-mode/references/subagents.md#models-and-diversity)). Add runners when the arena covers several design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive. Say which models ran.
4. Give each candidate its own output location, a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/` (`principle-separate-before-serializing-shared-state`).

## Phase B: Fan out

Start all N candidates together. Each brief has the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and rejected. Go on with N-1 and note the dropout when a candidate produces nothing.

## Phase C: Cross-judge

After every candidate finishes, start one read-only judge that produced none of them, from a different model family than yours when the host offers one; otherwise a fresh context, and say so. The judge sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs while you read in Phase D.

## Phase D: Pick a base

Read every candidate end to end. Score each against the rubric criterion by criterion, not on overall feel, and compare with the judge. Agreement confirms the pick. On disagreement, read both rationales before deciding: one of you is biased or the rubric was ambiguous.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API (`principle-laziness-protocol`). Do not select by prose quality, worker confidence, or a clean process exit.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things, not most of it. Fold each graft in by hand so the result stays coherent under one mental model (`principle-redesign-from-first-principles`); do not paste mechanically.

Ship the consensus shape without grafting when the candidates converge on one shape. Reframe and re-run rather than average when they diverge wildly, because Phase A was under-specified.

## Phase F: Verify

Verify the result like any other output (`principle-prove-it-works`): run the real checks on the synthesized artifact itself, not on a candidate. A problem the arena missed means Phase A was wrong (reframe and re-run) or a candidate caught it and you missed the graft (return to Phase E). Do not paper over it; keep the rubric fixed while repairing.

## Outputs

One synthesized artifact, with a short note: the base and why, the judge's verdict or that no judge ran, each graft and its source candidate, what was rejected and why, convergence or dropouts, the models used, and the verification result.

## Example

- **Base**: candidate-2 (`/tmp/arena-retry/candidate-2/`). It scored highest on rubric criteria 1 (single entry point), 3 (no new dependency), and 4 (tests exercise behavior).
- **Judge**: read-only, `<model-b>`, a different family from the main agent; it also chose candidate-2.
- **Grafts**: the backoff table from candidate-1, folded in by hand.
- **Rejected**: candidate-3's plugin layer (fails criterion 3).
- **Dropouts and models**: none; ran on `<model-a>`, `<model-b>`.
- **Verification**: `pytest tests/test_retry.py` on the synthesized artifact printed `12 passed`.
