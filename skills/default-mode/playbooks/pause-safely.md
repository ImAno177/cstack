### Pause safely

Stop an ongoing task at a recoverable boundary only when asked to pause. "Keep going" or "run until done" is not a pause request.

1. Finish the current atomic operation or roll it back if safe. Start no new agents, writes, or long jobs. Stop child work only through controls this host actually provides.
2. Inspect the worktree and identify owned versus unrelated changes. Never reset or delete other work to manufacture a clean tree. Do not push, merge, deploy, or message a third party just to pause.
3. Save a compact checkpoint through agent-context or the existing show-me-your-work trail: goal, pinned version/branch, done predicate, verified steps, pending work, key paths, blockers, and one next command. Store it in an appropriate task-owned location, not a transient directory the next session cannot access.
4. If preserving edits requires a WIP commit, stage only task-owned paths on a task branch and follow the repository's existing commit authorization and policy; leave other edits intact. Record explicitly whether anything is uncommitted or unpushed.
5. Check that the checkpoint actually exists and can be read. A description in chat alone is not a durable handoff when the next agent runs elsewhere.

**Reply:** stopped boundary, durable checkpoint path, branch and commit state, uncommitted work, and the first resume action.
