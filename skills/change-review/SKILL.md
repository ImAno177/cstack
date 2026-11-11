---
name: change-review
description: "Quality review of one change (uncommitted work, a commit, a branch or a PR): is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is every line needed. Reads the connected code, not only the diff. Each finding is explained in plain English. Use for \"review this\", \"code review\", \"review the last commit\", \"review my PR\", or \"is this over-engineered\". Not for a whole repository (use `repo-audit`), a threat model or secrets sweep (use `security-audit`), or running code to prove what a small change breaks elsewhere (use `blast-radius`); for adversarial, run-proven findings use `interrogate`."
---

Review a change like the senior developer who will be paged when it breaks.
Order of importance: correct, safe, holds under load, tested, fast, lean.
Lean still matters: every extra line must be read, tested and fixed later.

## 1. Understand first

- Review what the user names (`gh pr diff <n>` for a PR). Default to the
  uncommitted changes (`git diff HEAD`), or the last commit (`git show`)
  when there are none.
- Read the diff, then the callers, callees, tests and README it touches.
- A change can break code it does not touch. Grep every caller whenever a
  signature, return value or behavior changes.
- Find the expected load in the README or deploy config (one script, or many
  users and processes). Judge scale against it and say which load you assumed.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), a caller broken by the change, a fix applied in one
   caller while the shared function stays broken.
2. **Risk:** security holes (injection, weak randomness, secrets, missing
   checks on input from users), data loss (errors swallowed, writes in the
   wrong order, no transaction).
3. **Scale:** fine for one user, wrong for many: check-then-write races, the
   same work done by every process, memory or lists that only grow, a query
   per item, O(n^2) on big input, per-process state that must be shared.
4. **Missing test:** risky new logic (branch, parser, money, security, data
   writes, bug fix) with no test that fails when it breaks. One test, not coverage.
5. **Speed:** big slowdowns are problems; small wins are suggestions.
6. **Lean:** code that should not exist or should be smaller.
   delete (dead code, unused options), reuse (name the repo path of the
   existing helper), stdlib or native (instead of a new dependency), yagni
   (one-implementation abstraction, config nobody sets), merge (near-copies),
   split (one function with several unrelated jobs; split by job, never by
   line count).

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Re-read the lines: the caller exists, the value can be empty, the code is unused.
- A shortcut marked with a `shortcut:` comment that names its limit is a
  decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works, preferring deletion. Add no layers,
  frameworks or config. No style taste, no "consider", no vague worries.

## 4. Output

Very simple English: short sentences, everyday words. Explain a technical
term the first time you use it. The reader may never have seen this code.

Start with `What this change does:` in two or three sentences.

Then the findings in three groups, skip empty groups:
- **Must fix:** bug, security, data loss, breaks at the expected load.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Number findings across all groups, so the user can say "fix 2 and 5".
Every finding has a bold title with `path:Lstart-end`, then four parts in this
order, each one or two short sentences: **What this is**, **Problem** (the
concrete case and wrong result), **Fix** (smallest change), **If we skip it**.

End with:
- `Verdict: Ship.` or `Verdict: fix 1 and 3 first.`
- `Lean: -<N> lines possible.` when lean findings exist.
- `Not checked:` one line, if something mattered and you could not check it.

Nothing found: `What this change does:`, then `Looks good. Ship.` and one line
on what you checked.

## Not for

- Whole repos, threat models, run-proven breakage (see description). Fixing code.

## Done when

- The report starts `What this change does:`, ends `Verdict:`, and every
  finding is numbered with four parts, a real `path:Lstart-end` and a case
  you re-read in the code.
- `Lean:` appears exactly when a lean finding exists; `git status` shows no edit.

## If it fails

Move a finding with no concrete case, or a file you could not read, to
`Not checked:` or drop it. Never keep a vague worry.

## Example

What this change does:
It adds a nightly job that bills every order of the day that just ended, and an
`--export-csv` option. The job runs once a day on one server.

**Must fix**

1. **Late orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight the job closes the day and bills all orders of that day.
   - **Problem:** It reads "today" from the server clock, which uses UTC (the world time
     standard, not local time). An order placed at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone:
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`. Nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.

**Should fix**

2. **The new CSV option is never used** (`billing/cli.py:L12-30`)
   - **What this is:** `--export-csv` writes the day's orders to a file.
   - **Problem:** I searched the whole tree, including tests and config, and nothing sets it.
     The 12 lines are code nobody can reach.
   - **Fix:** Delete the option and the `write_csv` helper it calls.
   - **If we skip it:** Someone must read, test and keep 12 lines that never run.

Verdict: fix 1 first.
Lean: -12 lines possible.
Not checked: I did not run the job against the live billing database.
