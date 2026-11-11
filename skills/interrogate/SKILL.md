---
name: interrogate
description: Adversarial review where independent adversaries try to break a change or design, and only findings proven by a run survive. Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this", "find blind spots", or "tear this apart".
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings; do not apply fixes, and route accepted fixes to the owning implementation skill.

## Frame

The scope is what the user names; otherwise the branch diff from its merge base with the base branch, through the working tree. State the intent with `in-your-own-words`, from the user's message, the commits, and the PR description. Ask the user when the intent is unclear.

## Fan out

Run Phase A steps 3 and 4 and Phase B of `arena`, with these changes: pick adversaries the way arena picks runners, copy the scope's uncommitted changes into each worktree, and in place of the arena task give each adversary the scope, the intent, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Rerun each finding's command from the main workspace (arena Phase F). Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and which adversaries found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, how many findings were dropped and why.
- **Models**: which models the adversaries ran on, and whether cross-family diversity was available.
