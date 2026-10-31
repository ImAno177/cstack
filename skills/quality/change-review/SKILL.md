---
name: change-review
description: Review a code change for correctness, safety, load, tests, speed, and unnecessary code. Use for code or PR review.
---

# Change review

Review the code the change touches, not only the diff. Report findings. Do not edit code.

## Inspect

1. Identify the scope: named files, staged or unstaged changes, the branch, or the PR. If none is named, use uncommitted changes or the last commit.
2. Read the diff, changed functions, their callers, tests, configuration, and relevant docs.
3. Trace input, state changes, output, and failure paths.
4. Infer expected load from the repository. State the load you used.

## Check

- Bugs: wrong results, crashes, edge cases, broken callers, and partial fixes.
- Safety: injection, weak randomness, secret leaks, missing input checks, data loss, and bad write order.
- Load: races, repeated work, unbounded memory, N+1 queries, and poor complexity.
- Tests: risky branches, parsers, money, security, writes, and bug fixes need a behavior test.
- Speed: report only measured or clearly hot-path regressions.
- Waste: delete dead code, reuse existing helpers, prefer native APIs, and reject unused abstraction or configuration.

## Report

Start with `What this change does:` in two or three sentences. Number findings across these groups, omitting empty groups:

- **Must fix:** bugs, security, data loss, or failure at expected load.
- **Should fix:** missing tests, real slowness, duplication, mixed responsibilities, or unnecessary code.
- **Nice to have:** small measured improvements.

For every finding, include a short title and path with line, what the code does, a concrete failing case, the smallest fix, and the result of skipping it.

End with `Verdict: Ship.` or `Verdict: fix 1 and 3 first.` Add `Lean: -N lines possible.` when relevant. Add `Not checked:` when a material check was unavailable.

Report no finding without rereading the relevant code and confirming the case.
