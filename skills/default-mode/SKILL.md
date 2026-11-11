---
name: default-mode
description: Coordinate non-trivial engineering work that has no clearly matching narrow skill. Select a small task playbook, set a verifiable outcome, and inspect the resulting artifact. Do not load on top of a more specific skill by default.
---

# Default mode

Use when multi-step engineering needs a workflow and no narrower installed skill already owns the outcome. Do not make it mandatory for every multi-file change.

## Start

1. State the user's goal, the problem it solves, and the smallest complete change you expect to make.
2. Define a done predicate that a command, artifact, or user-visible result can prove.
3. Read the nearest instructions and only the files, callers, configuration, and generated artifacts that the change can reach.
4. Choose the narrowest skill that owns the work. Add a supporting skill only for a concrete required output.

## Route

- Select one matching playbook under [playbooks](playbooks/) before executing a non-trivial workflow. Read only that playbook and the skills it names.
- `investigation.md` is read-only research; `bug-fix.md` is for a reproduced defect; `feature.md` adds behavior; `refactoring.md` preserves behavior; `perf-issue.md` requires measurements; `prototype.md` settles one question; `eval.md` evaluates an agent and harness; `multi-phase-plan.md` stops at a plan; `authoring-a-skill.md` changes a skill; `opening-a-pr.md` ends any playbook that changes a repository; `babysit.md` drives an open PR to merge-ready; `shipping.md` lands verified PRs.
- A read-only explanation -> `how` or `why`.
- A defect with a reproducible symptom -> `principle-fix-root-causes`, then the narrow implementation skill; `tdd` when there is a cheap local test path.
- A new behavior or structural change -> `architect` when a boundary changes, then the implementation skill.
- A novel design fork -> `principle-exhaust-design-space`, then prototype behavior through the available tools.
- Several independent workers -> `multi-agent-workflow`; same-task alternatives -> `arena`; coverage slices -> `swarm`.
- Parallel, async, programmatic, or offline batch tool calls -> `tool-orchestration`.
- An adversarial review -> `interrogate`; an ordinary change review -> `change-review`; a security review -> `security-audit`.
- Proving UI, CLI, or service behavior the way a user would -> `webapp-testing` for a web app now, `create-verification-skill` for a repeatable project harness.
- A research question answered from papers -> `literature-review`.
- A long or unattended run -> `agent-context`, `agent-completion`, and `show-me-your-work` when a reviewer needs the decisions.
- A skill, rule, hook, or prompt change -> `prompt-audit`, then `continual-learning` when the change is meant to persist.
- An agent loop, local model adapter, Pi package, or harness evaluation -> `agent-harness`.

Do not route automatically to review or audit skills unless the request or the work's risk requires them; use `tdd` only when the user asks for it or the defect has a cheap local test path. Do not use Cursor-only features, model names, or paths on Codex, Claude Code, Grok Build, or Grok Bot.

## Execute

- Name the data shape and ownership before code crosses a module or function boundary.
- Make one smallest change that can move the done predicate, then verify it before the next unit.
- Prefer deletion and existing interfaces over wrappers, speculative guards, compatibility layers, or one-off helpers.
- Keep comments out of code unless they preserve a non-obvious contract, tool requirement, generated section, or license fact.
- For delegation, give each worker an isolated scope, a standalone brief, an evidence requirement, and a bounded budget. Start one unit first when the fan-out shape is unproven.
- Read the resulting diff or artifact yourself. A worker summary, clean exit, green check, or hook exit code is evidence of execution, not proof of completion.

## Finish

Check the real artifact against the done predicate. Report what changed, what was verified, what was skipped, partial or blocked work, and remaining risk. Never relax the predicate to declare success.
