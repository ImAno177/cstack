---
name: correct
description: Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then
  types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake.
  Repeat this each time the operator corrects you. Use for /correct.
---

# Correct

The operator keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Not for

- One-off mistakes that have not happened twice; fix them and move on.
- Rewriting the code review process or the operator's instruction files wholesale.

## Find the mistake classes

Read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** Add a lint or CI check whose error names the file, type, or function to use instead whenever bad code still compiles. Fail only on added instances when the pattern is already common.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check fails on a real past mistake. Run the same command locally and in CI. Exceptions go on the offending line with a reason, an expiry date, and a human's approval.

## Keep the rule table

Keep a table in the agent instruction file that pairs each rule with what enforces it. Fix the mistake and add the rule whenever the operator corrects you. A rule that was already there with nothing enforcing it is a repeat: fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

## Done when

- Each fixed class has its own commit, and its check fails on a real past mistake and passes on the fixed tree.
- The rule table lists every rule with its enforcer, and CI runs the same command as local.

## If it fails

A check that cannot fail on the past mistake is wrong: change its pattern or move up a level before committing. After two attempts at one level, go to the next level up. Do not add a docs-only rule to close a class.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.

Example:

> Class: handlers pass hand-built SQL strings to `db.run` (3 reverts, latest `<sha>`). Level: types. `db.run` now takes a `Query`, so a raw string fails `tsc`. Checked: `tsc` fails on `<sha>` and passes on the fixed tree. Architecture did not work because handlers need dynamic filters, so `db.run` stays public.
