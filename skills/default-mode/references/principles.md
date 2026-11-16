# Principles

The 24 principle skills are the reasons behind cstack's playbooks. Each is a short skill named `principle-<title>`, with the title in kebab case. When text says "the **fix-root-causes** principle", it means `principle-fix-root-causes`. Only `principle-prove-it-works` and `principle-fix-root-causes` are listed for automatic invocation; the other 22 are kept out of the always-on skill listing, so open them by path: `../../principle-<title>/SKILL.md` from this file. Read a principle's own `SKILL.md` before you apply it, and in your reply name each principle that changed a decision and the choice it changed.

## Contents

- Before writing code
- While building
- Debugging and measuring
- Delegation and long runs
- Finishing
- When principles pull against each other

## Before writing code

| Principle | Apply when |
| --- | --- |
| [`principle-foundational-thinking`](../../principle-foundational-thinking/SKILL.md) | Choosing core types and data structures, or sequencing scaffold before features |
| [`principle-model-the-domain`](../../principle-model-the-domain/SKILL.md) | Stateful logic, or code that branches a lot or repeats a shape assumption |
| [`principle-type-system-discipline`](../../principle-type-system-discipline/SKILL.md) | Designing types or signatures in a statically typed language |
| [`principle-boundary-discipline`](../../principle-boundary-discipline/SKILL.md) | Placing validation, error handling, or framework adapters |
| [`principle-experience-first`](../../principle-experience-first/SKILL.md) | Product, UX, or feature-scope tradeoffs |
| [`principle-exhaust-design-space`](../../principle-exhaust-design-space/SKILL.md) | A novel interaction or architecture decision with no useful precedent |
| [`principle-redesign-from-first-principles`](../../principle-redesign-from-first-principles/SKILL.md) | Integrating a new requirement into an existing design |

## While building

| Principle | Apply when |
| --- | --- |
| [`principle-subtract-before-add`](../../principle-subtract-before-add/SKILL.md) | Sequencing an addition, refactor, or rewrite |
| [`principle-laziness-protocol`](../../principle-laziness-protocol/SKILL.md) | Sizing a diff, or tempted to add abstractions or layers |
| [`principle-minimize-reader-load`](../../principle-minimize-reader-load/SKILL.md) | Code that is hard to trace |
| [`principle-migrate-callers-then-delete-legacy-apis`](../../principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | A new internal API while old callers still exist |
| [`principle-outcome-oriented-execution`](../../principle-outcome-oriented-execution/SKILL.md) | A planned rewrite or migration with explicit phase boundaries |
| [`principle-make-operations-idempotent`](../../principle-make-operations-idempotent/SKILL.md) | Commands, lifecycle steps, or loops that must survive crashes and retries |
| [`principle-separate-before-serializing-shared-state`](../../principle-separate-before-serializing-shared-state/SKILL.md) | Concurrent actors that might write the same file, branch, key, or state |
| [`principle-sequence-verifiable-units`](../../principle-sequence-verifiable-units/SKILL.md) | Multi-step work, and how you stack commits and PRs |
| [`principle-build-the-lever`](../../principle-build-the-lever/SKILL.md) | Non-trivial edits, migrations, analyses, or checks a tool could do or prove |

## Debugging and measuring

| Principle | Apply when |
| --- | --- |
| `principle-fix-root-causes` | Debugging any symptom |
| [`principle-attack-the-premise`](../../principle-attack-the-premise/SKILL.md) | Two or more fixes that share one premise have failed the same gate |
| [`principle-explain-the-number`](../../principle-explain-the-number/SKILL.md) | Before measuring, and before trusting or reporting a measured number |
| [`principle-test-behavior-not-implementation`](../../principle-test-behavior-not-implementation/SKILL.md) | Writing, changing, or keeping a test |

## Delegation and long runs

| Principle | Apply when |
| --- | --- |
| [`principle-guard-the-context-window`](../../principle-guard-the-context-window/SKILL.md) | Large outputs, long files, repeated reads, or fan-out planning |
| [`principle-never-block-on-human`](../../principle-never-block-on-human/SKILL.md) | Tempted to ask before a reversible action the task already authorizes |
| [`principle-encode-lessons-in-structure`](../../principle-encode-lessons-in-structure/SKILL.md) | Writing the same instruction a second time, or a recurring correction |

## Finishing

| Principle | Apply when |
| --- | --- |
| `principle-prove-it-works` | Before declaring any task done |

## When principles pull against each other

- **Verifiable units vs. planned breakage.** [`principle-sequence-verifiable-units`](../../principle-sequence-verifiable-units/SKILL.md) keeps every unit green. [`principle-outcome-oriented-execution`](../../principle-outcome-oriented-execution/SKILL.md) allows breakage only inside a declared phase of a planned migration, and the phase still ends green. Validation, security, and data-safety boundaries (AGENTS.md) never break.
- **Several prototypes vs. the smallest change.** [`principle-exhaust-design-space`](../../principle-exhaust-design-space/SKILL.md) applies only to novel, hard-to-reverse decisions. Everywhere else, [`principle-laziness-protocol`](../../principle-laziness-protocol/SKILL.md) and AGENTS.md's smallest complete version win.
- **Building levers vs. authorized delegation.** [`principle-build-the-lever`](../../principle-build-the-lever/SKILL.md) favors tools and fan-out, but delegate only when the task or user authorizes it and the work splits cleanly.
- **Root cause vs. premise.** Start with `principle-fix-root-causes`. Switch to [`principle-attack-the-premise`](../../principle-attack-the-premise/SKILL.md) once repeated fixes built on the same assumption keep failing.
