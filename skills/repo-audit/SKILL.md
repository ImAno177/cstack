---
name: repo-audit
description: "Quality audit of a whole repo or folder: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delete, merge or split. Ranked, each finding explained in plain English. One-shot report, changes nothing. Use for \"audit this codebase\", \"review the whole repo\", \"find bloat\", or \"what can I delete\". Not for one diff, commit or PR (use `change-review`), a dedicated threat model or secrets review (use `security-audit`), or proving by running code what a small change breaks elsewhere (use `blast-radius`)."
---

Audit the whole repo like the senior developer who just inherited it and
will be paged when it breaks. Order of importance: correct, safe, holds under
load, tested, fast, lean. Lean still matters: every extra line must be read,
tested and fixed later.

## 1. Map first

- Audit what the user names: a folder, a package, or (by default) the whole repo.
- Read the README, deploy and build config, dependency list, entry points
  (main, routes, handlers, jobs, CLI) and the tests.
- Find the expected load (one script, or many users and processes). Judge
  scale against it and say which load you assumed.
- Trace the main flows end to end: where data comes in, what is stored,
  what goes out. Read those paths fully: input from users, money, auth,
  data writes, background jobs, anything shared between processes.
- Go deep where a mistake costs the most, not file by file. Say which parts
  you did not read.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), callers that disagree with what a function returns,
   the same rule applied differently in two places.
2. **Risk:** security holes (injection, weak randomness, secrets, unchecked
   user input), data loss (errors swallowed, writes in the wrong order).
3. **Scale:** fine for one user, wrong for many: check-then-write races, the
   same work done by every process, memory or lists that only grow, a query
   per item, O(n^2) on big input, per-process state that must be shared.
4. **Missing test:** risky logic (branch, parser, money, security, data
   writes) with no test that fails when it breaks. One test, not coverage.
5. **Speed:** big slowdowns are problems; small wins are suggestions.
6. **Lean:** code that should not exist or should be smaller.
   delete (dead code, unused options, flags, config), reuse (two helpers doing
   one thing: keep one, name the path), stdlib or native (instead of a
   dependency), yagni (one-implementation interface, pass-through wrapper),
   merge (near-copies), split (one unit with several unrelated jobs; split by
   job, never by line count).

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Grep the whole tree (tests, fixtures, config, string and dynamic references)
  before calling code unused.
- A shortcut marked with a `shortcut:` comment that names its limit is a
  decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works, preferring deletion. Add no layers,
  frameworks or config. No style taste, no "consider", no vague worries.

## 4. Output

Very simple English: short sentences, everyday words. Explain a technical
term the first time you use it. The reader may never have seen this code.

Start with `What this repo does:` in two or three sentences, and the load
you assumed.

Then the findings in three groups, most important first, skip empty groups:
- **Must fix:** bug, security, data loss, breaks at the expected load.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Number findings across all groups, so the user can say "fix 2 and 5". At
most 20 findings; if you left smaller ones out, say how many.
Every finding has a bold title with `path:Lstart-end`, then four parts in this
order, each one or two short sentences: **What this is**, **Problem** (the
concrete case and wrong result), **Fix** (smallest change), **If we skip it**.

End with:
- `Verdict:` one line: healthy, or what to fix first.
- `Lean: -<N> lines, -<M> dependencies possible.` when lean findings exist.
- `Not checked:` the parts you did not read or could not run.

Nothing found: `What this repo does:`, then `Healthy. Nothing to fix.` and
one line on what you checked.

## Not for

- One diff, a threat model, or run-proven breakage (see description). Fixing code.

## Done when

- The report starts `What this repo does:` with the assumed load, has at most
  20 numbered findings, and ends with `Verdict:` and `Not checked:`.
- Every finding has four parts, a real `path:Lstart-end` and a re-read case;
  `git status` shows no edit.

## If it fails

Move a finding with no concrete case, or a part you could not read, to
`Not checked:` or drop it. Never pad the list.

## Example

What this repo does:
A small web shop. Customers order, a nightly job bills them. I assumed one server and about
50 orders a day.

**Must fix**

1. **Late orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which uses UTC (the world time
     standard, not local time). An order placed at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone:
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`. Nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.

**Should fix**

2. **A whole library is used for one line** (`requirements.txt:L7`, `shop/slug.py:L3`)
   - **What this is:** The `python-slugify` package turns a product name into a URL piece.
   - **Problem:** Only `shop/slug.py` imports it (I grepped tests and config too).
   - **Fix:** Write that line in `shop/slug.py` and remove the package from `requirements.txt`.
   - **If we skip it:** We keep patching a dependency that does almost nothing.

Verdict: fix 1 first.
Lean: -4 lines, -1 dependencies possible.
Not checked: I did not read `admin/` and did not run the tests.
