---
name: figure-it-out
description: Design an auditable playbook when no narrower one fits - a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for "figure it out" or work too large for a single default-mode playbook. Not for work one existing playbook covers; use `default-mode`.
---

# Figure it out

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: phases that scale rigor to the task, run the scientific method, and leave a decision trail a human can audit after stepping away.

## Start

Keep a task list whose first item is to read the [principles index](../default-mode/references/principles.md) and the principles it lists for this work (at least `principle-prove-it-works` and `principle-sequence-verifiable-units`). Then add the phases below.

## Phase A: Frame

Ground first, then commit. Start the run only once you can state:

- the definition of done as a falsifiable predicate checked on the real artifact (`principle-prove-it-works`);
- the scope, quantified: rough units and effort, and the blockers grounding surfaced;
- the rigor level, biased high. One-way doors and high blast radius get more; reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs before a long run. Proceed on reversible work without waiting (`principle-never-block-on-human`), and post one checkpoint for a multi-hour run.

## Phase B: Design the workflow

Split the work into atomic, independently landable units, riskiest unknown first. Scaffold and verification come before features (`principle-foundational-thinking`).

- Build the verification harness before the work, with the baseline captured from the pre-change state, so each check reads "old value vs new value".
- Run `architect` (which runs `arena`) for one-way-door design decisions. Skip it for mechanical work whose shape is already settled (`principle-laziness-protocol`).
- Decide what fans out. Parallelize only across seams and give each worker its own worktree or branch (`principle-separate-before-serializing-shared-state`, [subagents](../default-mode/references/subagents.md)). Do not over-fan.
- Write the phase list down. That list is what the human reviews.

Then add the design's steps to the task list between the Phase C and Phase D entries, run each under the Phase C loop, and log each step as it lands rather than saving the trail for the end.

## Phase C: Run the loop

Each unit is an experiment: state the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced and revert it if it did not. Verify each unit before starting the next (`principle-sequence-verifiable-units`).

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system.
- Pair delegated work with a judge. Reset and harden the contract when a worker games the gate. Fix a wrong gate in its own change rather than routing around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Report every negative.

## Phase D: Keep the audit trail

Log the run with `show-me-your-work`. This work is usually ambitious enough to commit the trail so the reviewer can read it in the PR; the trail plus the diff is what lets the human trust the work.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not only the harness. Encode any recurring correction as a gate, lint rule, check, or script (`principle-encode-lessons-in-structure`).

**Reply:** the playbook you designed, the rigor level and why, the decision-trail path, what is verified against the predicate, and what is still open.

## Done when

- The Phase A predicate was run against the real artifact and its output is quoted in the reply.
- The decision trail exists at the path the reply names, with one row per step.
- Every unit has a VERIFIED, NOT VERIFIED, or INCONCLUSIVE verdict; none is blank.

## If it fails

Name the failing unit and whether the hypothesis, the gate, or the environment was wrong. Change one of those before retrying. After two failed retries of a unit, revert it, log it, and take a different method or report the blocker. Keep the predicate fixed; do not weaken it to pass.
