---
name: architect
description: Sketch types, signatures, and module structure before code, design it at least twice, then stay in the loop while implementation fills in the sketch. Use for "architect this", "design this", a change that crosses a module or service boundary, or non-trivial work where jumping to code would lock in the wrong shape.
---

# Architect

Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Compare at least two structurally different designs, then fill in code against the chosen sketch.

## Not for

- A change where one existing owner and interface already make the shape obvious.

Keep a task list with one entry per phase: Ground, Sketch, Agree, Implement, Scrap.

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Run `how` over the relevant subsystems and produce the explanation it prescribes; naming a file is not grounding. If the design redefines ownership or layering, also run `why` on the existing shape so the rationale becomes a constraint, not a guess.

Run Phase A for every task except greenfield work with no surrounding system to integrate.

## Phase B: Sketch

Run `arena` with the design-sketch task and the Phase A grounding. Pass [references/runner-prompt.md](references/runner-prompt.md) as each runner's prompt. Pick runners per [subagents](../default-mode/references/subagents.md#models-and-diversity), preferring model diversity for design work.

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks sufficient: whole-shape alternatives, not point fixes inside one shape (`principle-exhaust-design-space`).

Screen every candidate against [references/design-red-flags.md](references/design-red-flags.md). Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repository.

Compare viable candidates on interface depth: prefer the design that hides more complexity behind a smaller public surface. Arena returns one synthesized design; its synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

By default, proceed to implementation with the synthesized design. Stop for sign-off when the user asks, such as "show me before implementing"; otherwise do not stop.

The sketch can ship as its own commit (the "scaffold first" mode of `principle-foundational-thinking`). Planned breakage during fill-in is fine (`principle-outcome-oriented-execution`). For adversarial pressure before implementing, run `interrogate` on the sketch. Treat user pushback on the shape as Phase A evidence: re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

Replace `not implemented` bodies with code. The sketch is the contract. A deviation is a signal to surface, not friction to absorb. When a function needs a parameter the sketch did not anticipate, decide whether the sketch was wrong, a requirement was missed, or the implementation is overreaching, and record the decision in the rationale. Run the repo's typecheck after each fill-in step.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch cannot absorb, throw it out instead of bolting fixes onto it (`principle-redesign-from-first-principles`, `principle-fix-root-causes`). The signal is a pattern, not one instance:

- the same workaround shape repeating across unrelated code;
- unrelated edge cases that each need a special-case branch;
- types that need escape hatches (`any`, casts, optional fields that are always set) to compile;
- a "we need a lock" reflex where the sketch said state was not shared;
- callers that must know the abstraction's internal rules;
- two or more independent Phase D deviations of the same shape.

A few edge cases do not condemn a design; complexity in the data is not complexity in the design. Scrap by this method, or an equivalent that ends with a smaller sketch: re-run `how` over what was built, redesign as if the new constraints were day-one assumptions, make the new sketch smaller than the old one before it grows (`principle-subtract-before-add`), and return to Phase B.

## Outputs

The caller's usage first, then the type sketch derived from it: one file of new types and signatures for small changes, a module map plus type definitions for larger work. The rationale ships alongside, shaped per [references/rationale-template.md](references/rationale-template.md), including the usage sketch and the synthesis decision.

## Done when

- The rationale file has every template section, usage before types, and a Synthesis decision naming at least two structurally distinct candidates.
- No design red flag is left unanswered, and the repo's typecheck passes on the sketch (bodies may throw `not implemented`).

## If it fails

- Candidates differ only in detail: change a structural axis (state owner, boundary) and rerun Phase B once.
- Phase D shows a Phase E pattern: scrap. Do not patch the sketch a third time.

