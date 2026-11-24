### Session pickup

Resume one known prior agent run or branch. This playbook reconstructs a working state, then routes remaining work; it does not replay the entire task.

1. Scope the exact workspace and input trail: a host-provided session transcript, an agent-context checkpoint, a decision log, a PR, or a branch. Do not scan transcripts from other projects. Prefer the recorded checkpoint if one is present.
2. Read the last state and decision points first, plus relevant evidence links. Verify the current branch, worktree, changes, commits, open PRs, and any uncommitted work. Preserve work from other runs.
3. Separate verified completed units from planned or reported units. Do not redo expensive completed work without a change to its inputs, a failed check, or contradictory evidence. Treat prior agent self-reports as pointers, not proof.
4. Name the exact resume point and unresolved predicate. Route only what remains to a matching playbook. If the request is just to catch up, stop with the state brief and make no edits.
5. Before saying done, prove inherited claims needed for the current outcome against the real artifact using principle-prove-it-works.

**Reply:** inherited state and evidence, work already verified, next action, and any unavailable or stale record.
