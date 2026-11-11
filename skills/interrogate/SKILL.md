---
name: interrogate
description: Adversarial review where independent adversaries try to break a change or design, and only findings proven by a run survive. Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this", "find blind spots", or "tear this apart". Not for routine diff review (use `change-review`) or security-focused audits (use `security-audit`).
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings; do not apply fixes, and route accepted fixes to the owning implementation skill.

## Frame

The scope is what the user names; otherwise the branch diff from its merge base with the base branch, through the working tree. State the intent with `in-your-own-words`, from the user's message, the commits, and the PR description. Ask the user before fanning out when the intent is unclear.

## Fan out

Run Phase A steps 3 and 4 and Phase B of `arena`, with these changes: pick adversaries the way arena picks runners, copy the scope's uncommitted changes into each worktree, and in place of the arena task give each adversary the scope, the intent, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Rerun each finding's command from the main workspace (arena Phase F). Keep a finding only when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and which adversaries found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, how many findings were dropped and why.
- **Models**: which models the adversaries ran on, and whether cross-family diversity was available.

## Done when

Every kept finding carries a command and output you reran yourself, and no fix was applied. A finding that does not reproduce from the main workspace is dropped, not softened. Reissue an adversary's brief once when it returns nothing runnable.

## Example

- **Intent**: `parse_date` rejects malformed dates with exit code 2 and writes nothing.
- **Findings**: 1. Partial write on bad month. `python cli.py --date 2026-13-01 out.txt; echo $?; wc -c out.txt` printed `0` and `12 out.txt`; the intent requires `2` and no file. Found by adversaries 1 and 3.
- **Dropped**: adversary 1: 1 (naming, no run). Adversary 2: 2 (needs a future refactor). Adversary 3: 0.
- **Models**: `<model-a>`, `<model-b>`, `<model-c>`; cross-family diversity was available.
