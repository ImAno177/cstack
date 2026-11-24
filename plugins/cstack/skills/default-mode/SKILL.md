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
- Skills the user starts by name (`arena`, `swarm`, `interrogate`, `figure-it-out`, `show-me-your-work`, the verification skills, and the principles) are not in the skill listing. When a route below names one, read its `SKILL.md` through the link given. Skills from the `cstack-harness` and `cstack-research` plugins apply only when that plugin is installed; otherwise follow the route without them.
- `investigation.md` is read-only research; `bug-fix.md` is for a reproduced defect; `feature.md` adds behavior; `refactoring.md` preserves behavior; `perf-issue.md` requires measurements; `prototype.md` settles one question; `eval.md` evaluates an agent and harness; `multi-phase-plan.md` stops at a plan; `authoring-a-skill.md` changes a skill; `opening-a-pr.md` ends any playbook that changes a repository; `babysit.md` drives an open PR to merge-ready; `shipping.md` lands verified PRs.
- Additional playbooks: `hillclimb.md` for repeated metric improvement; `runtime-forensics.md` for live captures; `trace-forensics.md` for existing traces; `visual-parity.md` for screenshot equivalence; `session-pickup.md` for one prior run; `pause-safely.md` for a durable stop; `autonomous-run.md` for bounded continuation when the host supports it.
- Read-only explanation -> `how` or `why`.
- Defect with a reproducible symptom -> [`principle-fix-root-causes`](../principle-fix-root-causes/SKILL.md), then the narrow implementation skill; add `tdd` when a cheap local test path exists.
- New behavior or structural change -> `architect` when a boundary changes, then the implementation skill.
- Novel design fork -> [`principle-exhaust-design-space`](../principle-exhaust-design-space/SKILL.md), then prototype behavior through the available tools.
- Several independent workers -> `multi-agent-workflow` (cstack-harness); same-task alternatives -> [`arena`](../arena/SKILL.md); coverage slices -> [`swarm`](../swarm/SKILL.md).
- Parallel, async, programmatic, or offline batch tool calls -> `tool-orchestration` (cstack-harness).
- Adversarial review -> [`interrogate`](../interrogate/SKILL.md); one change -> `change-review`; whole repository -> `repo-audit`; threat model or secrets -> `security-audit`; what a small change breaks elsewhere -> `blast-radius`.
- Proving UI, CLI, or service behavior the way a user would -> `webapp-testing` for a web app now, [`create-verification-skill`](../create-verification-skill/SKILL.md) for a repeatable project harness.
- Research question answered from papers -> `literature-review` (cstack-research).
- Prior work across multiple conversations -> `recall`. Resume one known checkpoint, branch, or run -> `session-pickup.md`; do not duplicate completed work.
- Live runtime diagnosis -> `runtime-forensics.md`; a supplied CPU profile, crash dump, or trace -> `trace-forensics.md`.
- Sustained metric optimization with controlled repeated attempts -> `hillclimb.md`; visual rewrite with a reference UI -> `visual-parity.md`.
- Long or unattended run -> `agent-context` and `agent-completion` (cstack-harness), and [`show-me-your-work`](../show-me-your-work/SKILL.md) when a reviewer needs the decisions. Explicit pause -> `pause-safely.md`; authorized bounded continuation -> `autonomous-run.md` only with a real host wake mechanism.
- Skill, rule, hook, or prompt change -> `prompt-audit`, then `continual-learning` when the change is meant to persist (both cstack-harness).
- Agent loop, local model adapter, Pi package, or harness evaluation -> `agent-harness` (cstack-harness).
- Large design or migration that needs an auditable playbook -> [`figure-it-out`](../figure-it-out/SKILL.md); a recurring agent mistake to make impossible -> [`correct`](../correct/SKILL.md); lessons from a finished episode -> [`reflect`](../reflect/SKILL.md).

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

## Operating lessons

- A denied tool call ends that action. Ask the user instead of retrying it or finding another route to the same effect.
- Wait on CI with one `gh run watch` or `gh pr checks --watch`, not a polling loop.
- Cleanup: list what exists, verify merges on the remote, then delete. Never remove a worktree or branch you did not create in this session without listing it first.
- In a repository with submodules, never `git commit -a`; stage paths explicitly.
- Ask before installing tools outside the project's own dependency manager.
- In Git Bash on Windows, set `MSYS_NO_PATHCONV=1` before passing device or Unix-style paths to `adb`.
- Write generated files with the repository's line endings.

## Finish

Done when the real artifact (diff, file, command output, or PR URL) satisfies the done predicate you set in Start. Report what changed, what was verified with which command, what was skipped, partial or blocked work, and remaining risk. Never relax the predicate to declare success.

## If it fails

Diagnose with the smallest probe (`git diff`, the failing command's output) and change the cause before each retry. After two attempts that change nothing, stop or switch method (another playbook or a narrower skill) and report the blocker with the predicate unchanged.
