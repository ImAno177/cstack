---
name: agent-completion
description: Establish whether an agent task actually completed after tool calls or side effects by separating attempted, executed, verified, partial, blocked, and failed states. Use when changing files, running commands, or handing off work; not for abstract explanations. For test-driven changes use `tdd`; for diff review use `change-review`.
---

# Agent completion

Name an observable done condition and its authoritative state source before acting.

## Verify

- Track each important action as requested, attempted, executed, and verified. Keep the four states separate.
- Inspect the real artifact or external state after each side effect (`git status`, `ls`, a re-read of the file, an API GET). A clean exit, tool acknowledgement, or generated message proves execution only.
- Run the smallest check that can disprove completion, then read the resulting paths, values, records, or user-visible effect.
- Treat timeout, interruption, partial output, missing artifact, and contradictory evidence as incomplete until resolved.

## Report

- Classify the outcome as verified, partial, blocked, or failed.
- State the changed paths or resources, the commands or tools actually run, the evidence observed, skipped checks, and remaining risk.
- Claim a test, deployment, write, merge, upload, or cleanup succeeded only after observing its result.

## Not for

- Explanations or answers with no side effect to check.

## Done when

- Every requested action has a state, and each "verified" claim cites output you observed after the last change.
- Any edit made after a check invalidates that check; re-run it before reporting.

## If it fails

- Name the failing state (attempted, executed, or verified) and the evidence that contradicts completion.
- Change the action, input, or check before retrying; do not retry unchanged. Report blocked or failed after two distinct attempts, and keep the done condition fixed.

## Example report

```
Outcome: partial
Changed: src/parse.py (verified: `git diff --stat` shows 1 file, +12 -3)
Ran: `pytest tests/test_parse.py` -> 8 passed
Skipped: `pytest tests/` full suite (blocked: fixture DB unreachable)
Risk: <downstream caller> untested
```
