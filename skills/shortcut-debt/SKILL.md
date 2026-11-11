---
name: shortcut-debt
description: List every `shortcut:` comment as a debt ledger. One-shot report, changes nothing.
  Use for "shortcut debt" or "list the shortcuts".
---

Every deliberate shortcut is marked with a `shortcut:` comment naming
its ceiling and upgrade path. This collects them into one ledger so a deferral
can't quietly become permanent.

## Scan

Grep the repo for comment markers, skipping `.git` and everything the
`.gitignore` files ignore (dependencies, build output, caches, in any stack):

`git grep --no-index --exclude-standard -nE '(#|//|/[*]) ?shortcut:'`  (add other comment prefixes if your stack uses them)

Grep for the user's marker word instead when they name another.

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger. Skip hits that are not a deferral, like a note
about a keyboard shortcut.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `shortcut: <ceiling>, <upgrade path>`, so pull the ceiling
and the trigger straight from the comment. Add an owner per row with
`git blame -L<line>,<line> <file>` when the user asks for one.

Flag the rot risk: any marker comment that names no upgrade path or
trigger gets a `no-trigger` tag, those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No shortcut debt. Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. Write the ledger to a file (e.g. `shortcut-DEBT.md`) only when the user asks. One-shot.

## Not for

- Fixing or removing shortcuts; use the repo's normal edit flow.
- Auditing general code quality; use `repo-audit`.

## Done when

- The last line is `<N> markers, <M> with no trigger.` (or the clean-ledger line), and N equals the row count.
- Rerun the grep if files changed since the scan.

## If it fails

- Zero hits in a repo that uses the convention: the comment prefix is probably missing from the pattern (`--`, `;`, `<!--`). Add it and rerun; keep the marker word fixed.
- Report the exact command used.

## Example

```
src/cache.py:41, in-memory dict instead of Redis. ceiling: one process. upgrade: second worker added.
src/auth.py:88, plaintext token compare. ceiling: unknown. upgrade: none. no-trigger
2 markers, 1 with no trigger.
```
