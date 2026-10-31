---
name: technical-writing
description: Write and review concise technical docs, READMEs, RFCs, PRs, and commit messages with clear structure and plain language.
---

# Technical writing

Write so a tired engineer understands the first time. Cut words that do no work. Prefer the short, concrete word. Use the repository's real names, paths, flags, and commands.

## Choose one mode

- Tutorial: teach by producing a visible result at each step.
- How-to: solve a task with direct actions and only needed context.
- Reference: state complete facts, options, limits, and errors.
- Explanation: explain one bounded design or reason, including trade-offs.

Do not mix modes in one document. Use one h1. Use sentence-case headings. Use numbered lists for sequences and bullets for unordered facts.

## Write clearly

- Address the reader as `you` and use the present tense.
- Put the condition before the instruction.
- Name the actor: "the compiler checks", not "is checked".
- Keep one instruction per sentence and one idea per sentence.
- Split long sentences. Keep articles such as "a" and "the" when they remove ambiguity.
- Use periods instead of semicolons and em dashes.
- Keep `only`, `not`, `and`, and `or` next to the words they modify.
- Use one name for each thing throughout the document.
- Remove filler, hedging, slogans, metaphors, generic conclusions, and AI-sounding phrases. Apply `unslop` when this skill edits prose.

## Verify

Ground claims in code, configuration, measured results, or named sources. Include the command that regenerates generated text. Report skipped evidence instead of implying full coverage.
