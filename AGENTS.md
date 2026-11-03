# cstack

The repository root is the installable plugin. Keep skills, hooks, manifests, scripts, and docs at the root; do not recreate `source/`, `plugins/`, or `general/` layers.

Use the explicitly named skill first. Use `skills/skills-router/SKILL.md` only when several installed skills plausibly apply.

## Work rules

- Read only the instructions and files relevant to the task. Do not scan the whole repository for a small change.
- State the outcome and scope, then execute the smallest complete change. Use a plan only for work that is multi-file, long-running, or risky.
- Inspect `git status` first and preserve unrelated user changes. Do not reset, checkout, or overwrite them.
- Search for the existing target, callers, exports, and configuration before creating a file or parallel implementation. Update the existing path when it owns the behavior.
- Reuse existing code and commands. Do not add a one-off helper, abstraction, fallback, compatibility layer, or scratch file for a single use. If a temporary artifact is necessary, keep it outside the repository and remove it before handoff.
- If a command fails because of permissions or sandbox policy, read the error and use a known writable path. Do not retry random paths or claim a workaround worked without rerunning the real command.
- Do not ask for approval for reversible work already covered by the request. Ask only when the scope or an irreversible external action is genuinely unclear.

## Execution and temporary work

- Batch or parallelize independent, read-only operations when the tools support it. Do not batch dependent calls, calls that share mutable state, or side-effecting actions.
- Keep writes, deletes, approvals, migrations, and final validation on an explicit serial path. Inspect every result before using it as input to the next step.
- For a one-off operation, prefer an existing command or an inline expression. If a temporary script is necessary, create it outside the repository, give it explicit inputs and outputs, verify the result, and remove it before handoff.
- Promote temporary code into a repository-owned script only when the operation will recur, has meaningful control flow, changes important data, needs provenance, or deserves its own verification.

## Multi-agent

- Delegate only independent, bounded work. Keep short, sequential, or shared-state work in one agent.
- Prefer read-only lanes. Every writing agent needs a separate worktree, branch, or output path; never let parallel agents edit the same working tree.
- Start with at most three concurrent agents and one delegation level. Give each a scope, allowed paths, expected output, done condition, and bounded time/retry budget. Do not treat a missing result or clean exit as success; the parent must verify and merge results.

## Agent state

- Separate attempted, executed, and verified. Inspect the real artifact or side effect before claiming completion.
- For long work, use bounded phases and compact checkpoints. Cap unknown command output and stop repeated reads, retries, or plans that produce no new evidence.
- When evaluating an agent workflow, inspect the trajectory and artifact, repeat representative tasks, and report variance, cost, latency, partial completion, and cleanup—not only the final message.

## Tests and handoff

- Do not add tests by default. Add or change a test when behavior, a public contract, a bug fix, a parser, a branch, security, or a data-writing path needs regression coverage. Tests verify the implementation; they do not define a workaround.
- Prefer the smallest existing check that proves the real artifact. Do not treat compilation or a green test as proof of user-visible behavior, side effects, cleanup, or security. Inspect the resulting artifact or effect.
- Do not change or delete a test just to make it pass. Report checks that were skipped and why.
- Remove debug output, generated files, temporary fixtures, and one-off scripts before handoff unless the repository explicitly owns them.

## Version control

- Inspect `git status --short`, the current branch, and its upstream before editing. Separate pre-existing changes from the files owned by the current task.
- After the requested change passes its relevant checks, inspect the real diff, run `git diff --check`, and stage only files owned by the current task.
- Commit completed repository changes with a clear conventional commit message, then push the current branch to its configured upstream unless the user explicitly says not to publish the change.
- Never stage unrelated work, secrets, generated noise, or temporary artifacts. Never use force-push, rewrite remote history, or change the configured remote as part of routine task completion.
- If the branch has unrelated unpushed commits, the upstream is missing, authentication fails, or publication would include work outside the task, stop before pushing and report the exact blocker.
- After pushing, verify the remote branch and commit with `git status --short` and `git log -1 --oneline`. Report the commit and remote branch in the handoff.

Skills listed in `.cstack/upstreams.json` are managed copies. Update them with `python scripts/sync_upstream_skills.py --write`; do not hand-edit them. The sync job runs on schedule and manual dispatch.

Validate a stack change from the repository root:

```powershell
python scripts/validate_plugin.py --root .
python scripts/validate_skill_stack.py --source-root . --plugin-root . --policy .cstack/skill-policy.json
python scripts/generate_grok_plugin_index.py --check
```

Keep hooks fail-open, preserve trust-boundary validation, and do not add code comments unless a tool, compiler, license, public contract, or non-obvious external constraint requires one.
