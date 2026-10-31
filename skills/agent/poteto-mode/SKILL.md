---
name: poteto-mode
description: Default workflow for non-trivial engineering changes with multiple files, boundaries, or risk.
---

# Default workflow

The session hook loads this workflow by default. Keep simple answers and one-line edits direct. An explicitly named skill owns the task when one clearly applies.

## Use the loop when it earns its cost

1. Frame non-trivial work. State the user's problem, the smallest complete change, and the evidence that will prove success.
2. Read only what the task needs. Follow the nearest `AGENTS.md` and relevant skill. Inspect callers, configuration, exports, fixtures, and generated artifacts when the change can affect them.
3. Resolve ambiguity with evidence. Use `in-your-own-words` or `sharpen` only when intent remains unclear. Decide and proceed on reversible execution. Pause for a real product choice or irreversible action.
4. Design only changed boundaries. Use `how` for an unfamiliar subsystem. Use `architect` and `principle-model-the-domain` when data or ownership changes. For a novel interaction or contested architecture, compare 2–3 small prototypes. For a multi-file change, keep a short path-and-check plan before editing.
5. Make the smallest complete diff. Remove dead or redundant code before adding structure. Reuse existing code and dependencies. Preserve validation, error handling, security, accessibility, and data-safety boundaries. Write comments only for constraints the code cannot show.
6. Verify in proportion to risk. Use the smallest real check that can catch the failure: validator, typecheck, behavior test, CLI, browser, or runtime. Reproduce the user's exact symptom before fixing a bug. Inspect the final diff and report changed, verified, skipped, and risk.

## Supporting routes

- Several skills plausibly own the request → `skills-router`.
- Prose, docs, README, RFC, PR, or commit message → `technical-writing`, then `unslop` when the output is prose.
- A measured number or benchmark → `benchmark-checklist`.
- A broad, sensitive, or cross-system change → `blast-radius`.
- A recurring agent mistake → `correct`.

Keep procedures in skills and references. Keep global instructions short. Do not create a process artifact unless it helps the next decision or verification.
