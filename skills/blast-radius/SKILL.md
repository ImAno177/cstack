---
name: blast-radius
description: "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it is safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you do not trust. Not for a general quality review of the change (use `change-review`), a whole-repository audit (use `repo-audit`), or a threat model and secrets review (use `security-audit`)."
---

# Blast radius

Find what a change breaks somewhere else, before it ships.

Companion to `how` and `why`. `how` tells you what the code does. `why` explains the evidence behind its shape. Blast radius tells you what it breaks somewhere else.

Listing callers is not the job; `grep` does that in a second. The job is the breakage grep won't show you.

## Don't trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it's true. So don't hand back the writeup. Find the one or two facts the whole thing depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, get it as far down this list as is cheap, and say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, or the library's own source.
3. You showed the bad case can't happen. You walked the failure step by step and it doesn't reach.
4. You ran it. A script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app.

Step 4 is usually one small script that imports the same library the app ships and calls the exact function you're worried about.

## Steps

1. Read the change. The diff, the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff doesn't spell out. Use the repository history when the decision matters.
2. Find the one fact it's safe because of. Most changes that look risky are safe because of a single fact, like "this call only drops already-dead cache entries and does nothing else". Find that fact: once it holds, most risky cases are cleared at once. Spend your time here, not on a long list of maybes.
3. Look where grep stops. Read the source of the library you call, and check its pinned version and any local patch. Work out when things run: microtasks, unmount and teardown, Solid versus React. Follow what a symbol search misses: the JSON an API returns, a DB column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. Be honest about each risk. Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed. List the ones you checked and cleared separately. Cite a real `file:line`, a search that finds nothing is still an answer, and never make up a caller or an API.
5. Prove the one fact. Write a script or test that calls the real code (in a scratch path, not the repo), run it with the project's runner (for example `python3 /tmp/check.py` or `npm test -- <file>`), and paste the command and its output. It must fail loudly when the fact is false.
6. Split a big or wide change by boundary (see `multi-agent-workflow`) and keep each claim tied to a command or artifact.

## What to hand back

- **What it does.** What changed, including the part that isn't obvious.
- **The one fact it's safe because of.** State it, say which step you got it to, and show the proof. If you couldn't prove it, write unproven.
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad, and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it's fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Write it plainly, cite real code, and strip anything private before it goes anywhere public.

## Not for

- A line-by-line quality review, a repo audit or a threat model (see description).
- Listing callers alone, or a change you can only describe: read the diff first.

## Done when

- The reply has the five parts above, and the one safety fact is marked with its step (1 to 5) or `unproven`.
- Every risk cites a real `file:line`; the proof script's command and output are pasted, or its absence is stated.

## If it fails

When the script passes although you expected a failure, or fails unexpectedly, fix the script's setup (version, imports, inputs) before changing the claim; never loosen the check to get a pass. After two failed attempts, report the fact as `unproven` with the best step reached.
