---
name: show-me-your-work
description: Keep a compact, reviewable decision trail for long-running, unattended, or multi-phase work. Use when a reviewer needs to trust the path from decision to evidence.
---

# Show me your work

Keep one canonical TSV outside the repository by default. Commit it only when the reviewer needs the trail as a project artifact.

Use one row per meaningful decision or checkpoint:

```text
ts	phase	decision	why	evidence	result
```

- `ts` is an ISO 8601 timestamp.
- `phase` names the workstream.
- `decision` says what was chosen or done.
- `why` gives the plain-language reason.
- `evidence` points to a path, command result, SHA, PR, or artifact.
- `result` says the predicate state, such as `verified`, `reverted`, `blocked`, or `open`.

Log forks, completed verified units, pivots, reverts, blockers, and gates. Do not log every command. On pickup, read the last rows first and add a new `start` row when another run wrote to the log.
