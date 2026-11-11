---
name: maintain-formal-verification-skill
description: 'Bring a project''s formal verification back in line with the code after the code changes: find the commits that
  touched verified code, update the model, harness, or properties to describe the code as it is now, rerun, and say whether
  each failure is drift in the verification or a bug in the code. Use for /maintain-formal-verification-skill, "is the model
  still true to the code", or after merges and refactors that touched verified code without rechecking it.'
---

# Maintain a formal verification skill

A formal check proves a property of what it describes. When the code changes and the verification does not, the check can keep passing while it describes code that no longer exists. This skill is the upkeep loop for a verify skill that `/create-formal-verification-skill` generated, or for any project-local skill that runs a model checker, prover, or code-level verifier against named code. This skill handles changes that skipped the project-local skill: merges, edits made without it, and drift across many commits.

## Outcomes

Give each check one outcome, and say which:

- **in sync**: no change since the last sync alters what the check describes, and the check passes.
- **updated**: the code changed, the verification now describes the new code, and the check passes.
- **bug**: the verification describes the current code, and the code breaks the property. This is a finding about the code. It is not drift.
- **blocked**: the check could not be brought back in line or could not run. Say exactly why.

A check can be both updated and bug: the update makes the verification describe the code again, and then the property fails on it.

## Edit scope

Edit only the verification: models, harnesses, property files, and the verify skill itself. Never edit product code during a run unless the user asks. Report a property that fails on the current code; never weaken the property or the model to make it pass.

## Pass

1. **Find the checks.** A verify skill has no fixed name, so find it by what it does: a project skill that runs a model checker, a prover, or another verifier against named code. Read each one you find, or the one the user named. For each check, collect the property, the code it covers, the bounds and assumptions, the command that runs it, and the commit where it was last confirmed to describe the code. Stop and point at `/create-formal-verification-skill` when no verify skill exists. Use the last commit that changed the verification files, and say that you did, when the skill records no sync commit.

2. **Run it as it is.** Run each check once before you change anything, and record the result. A pass here does not tell you that the code is correct. It tells you that the old description still holds. A failure here can be drift or a bug. Do not decide which until step 5.

3. **Read every change to covered code.** Diff the covered files from the sync commit to the current commit, and read each commit message. Also look for code that moved: a covered function that is renamed, split, or moved to another file is still covered code. Also look for new code that touches the state that a check guards, such as a new function that writes the same fields. For each change, decide which of these it is:
   - **No effect.** The change does not alter anything the verification describes, such as formatting, comments, or code paths that the verification does not cover. Check this against the model or harness, not against the commit message.
   - **The verification no longer describes the code.** A step that was one indivisible action is now two, a branch was added or removed, a check moved, a new path reaches the guarded state, or a value now has a different range. The model or harness must change.
   - **The promise changed on purpose.** The change alters what the code promises, and evidence in the change says that this is intended: the doc comment, the tests, the changelog, or the commit message. The property must change, and you must cite that evidence.
   - **The promise may be broken.** The code changed, and no evidence says that the promise changed. Treat a failure that follows as a bug candidate.

4. **Update from the code, not from the result.** Change the model or harness so that each changed part again points to code that a reviewer can open, and keep one indivisible step in the code as one step in the verification. Write the update from the code before you rerun, and do not shape it by what makes the check pass. Change a property only for a promise that changed on purpose. Write down the old wording, the new wording, and the evidence. Keep the bounds unless the change makes them wrong. If you must reduce a bound, say so in the report.

5. **Rerun and judge each result.**
   - **Pass:** the check can now pass on a description that has lost the ability to fail. Break the new code the way the property guards against, such as removing a new check or reordering a new step, and confirm that the check catches it. Then drop the break.
   - **Fail:** replay the counterexample against the real code, step by step. If a step cannot happen in the code, the verification is wrong. Fix the verification, and say what was wrong. If every step can happen, it is a bug. Name the commit that introduced it, tell the counterexample as a sequence of steps in the code's own words, and state the harm in one sentence. If a cheap test or reproduction against the real code shows the bug, add it to the report as evidence. Do not commit it to the product code.

6. **Update the verify skill.** Update the code that each check covers, the commands, the bounds, the assumptions, and the sync commit. Set the sync commit to the commit that you checked. Leave the sync commit unchanged for a blocked check, and say so in the report. Then follow the verify skill once as the next agent would, so that you know its steps still run.

## Report

Tell the user, for each check:

- the outcome, and the commits that you read;
- what changed in the verification and why, with a short reason for each change: the code changed shape, or the promise changed on purpose (with the evidence);
- the rerun result, and the break that you used to show the updated check can still fail;
- each bug, in plain words: the counterexample as steps in the code's words, the harm, and the commit that introduced it;
- what the verification still does not cover, including new code that it should cover and does not.

Say outright which failures were drift in the verification and which were bugs in the code. Say that the old pass was on a stale description for a check that passed before you updated it and fails after.

Put the verification updates in a change of their own, separate from any product fix.

## Not for

- Writing a first verification skill: use `/create-formal-verification-skill`.
- Maintaining a UI or CLI feature map: use `maintain-verification-skill`.

## Done when

- Every check has one outcome in the report, and each updated check has a recorded rerun and a break the check caught.
- Each updated verify skill names the commit you checked as its sync commit, and the verification change contains no product-code edits.

## If it fails

Read the first counterexample or tool error, then change the model, harness, or bounds before rerunning. Mark the check `blocked`, with the exact reason, after two reruns that change nothing new. Never loosen a property to get a pass.

## Example

```
<check>: updated.
Read: <sha-old>..<sha-new> (2 commits).
Changed: split `<step>` into `<step>` and `<step-2>` in the model, because <sha-new> made them two steps (code changed shape).
Rerun: pass. Removing the new owner check makes TLC report <property> violated, so the check can still fail.
Bugs: none. Sync commit is now <sha-new>.
Not covered: the retry path added in <path>.
```
