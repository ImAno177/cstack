---
name: default-mode
description: Coordinate non-trivial engineering work that has no clearly matching narrow skill. Select a small task playbook, set a verifiable outcome, and inspect the resulting artifact. Do not load on top of a more specific skill by default.
---

# Default mode

Use for multi-step engineering that needs a workflow when no narrower installed skill owns the outcome. A multi-file change alone does not require it.

## Start

1. State the user's goal, the problem it solves, and the smallest complete change you expect to make.
2. Define a done predicate that a command, artifact, or user-visible result can prove.
3. Read the nearest instructions and only the files, callers, configuration, and generated artifacts that the change can reach.
4. Choose the narrowest skill that owns the work. Add a supporting skill only for a concrete required output.

## Route

- Select one matching playbook under [playbooks](playbooks/) before executing a non-trivial workflow. Read only that playbook and the skills it names.
- `investigation.md` is read-only research; `bug-fix.md` is for a reproduced defect; `feature.md` adds behavior; `refactoring.md` preserves behavior; `perf-issue.md` requires measurements; `prototype.md` settles one question; `eval.md` evaluates an agent and harness; `multi-phase-plan.md` stops at a plan; `authoring-a-skill.md` changes a skill; `opening-a-pr.md` ends any playbook that changes a repository; `babysit.md` drives an open PR to merge-ready; `shipping.md` lands verified PRs.
- Read-only explanation -> `how` or `why`.
- Defect with a reproducible symptom -> `principle-fix-root-causes`, then the narrow implementation skill; add `tdd` when a cheap local test path exists.
- New behavior or structural change -> `architect` when a boundary changes, then the implementation skill.
- Novel design fork -> `principle-exhaust-design-space`, then prototype behavior through the available tools.
- Several independent workers -> `multi-agent-workflow`; same-task alternatives -> `arena`; coverage slices -> `swarm`.
- Parallel, async, programmatic, or offline batch tool calls -> `tool-orchestration`.
- Adversarial review -> `interrogate`; one change -> `change-review`; whole repository -> `repo-audit`; threat model or secrets -> `security-audit`; what a small change breaks elsewhere -> `blast-radius`.
- Proving UI, CLI, or service behavior the way a user would -> `webapp-testing` for a web app now, `create-verification-skill` for a repeatable project harness.
- Research question answered from papers -> `literature-review`.
- Long or unattended run -> `agent-context`, `agent-completion`, and `show-me-your-work` when a reviewer needs the decisions.
- Skill, rule, hook, or prompt change -> `prompt-audit`, then `continual-learning` when the change is meant to persist.
- Agent loop, local model adapter, Pi package, or harness evaluation -> `agent-harness`.

Route to review or audit skills only when the request or the work's risk requires them, and to `tdd` only when the user asks or a cheap local test path exists. Use only features the current host provides (Codex, Claude Code, Grok Build, Grok Bot); do not assume another host's tools, model names, or paths.

## Principles

The principle skills behind these playbooks are indexed, with when to apply each and how to resolve tensions between them, in [references/principles.md](references/principles.md). Read the index before a non-trivial run, then read each principle you apply.

## Execute

- Name the data shape and ownership before code crosses a module or function boundary.
- Make one smallest change that can move the done predicate, then verify it before the next unit.
- Prefer deletion and existing interfaces over wrappers, speculative guards, compatibility layers, or one-off helpers.
- Keep comments out of code unless they preserve a non-obvious contract, tool requirement, generated section, or license fact.
- For delegation, give each worker an isolated scope, a standalone brief, an evidence requirement, and a bounded budget. Start one unit first when the fan-out shape is unproven.
- Read the resulting diff or artifact yourself. A worker summary, clean exit, green check, or hook exit code is evidence of execution, not proof of completion.

## Not for

- A task a narrower skill owns, or a short single-file edit: act directly.

## Finish

Done when the real artifact (diff, file, command output, or PR URL) satisfies the done predicate you set in Start. Report what changed, what was verified with which command, what was skipped, partial or blocked work, and remaining risk. Never relax the predicate to declare success.

## If it fails

Diagnose with the smallest probe (`git diff`, the failing command's output) and change the cause before each retry. After two attempts that change nothing, stop or switch method (another playbook or a narrower skill) and report the blocker with the predicate unchanged.
