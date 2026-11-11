### Shipping

You own what lands. Merge only the commit that CI and an independent review checked, from the bottom of the stack up, and only with authority: an explicit request to merge, or a repository policy that permits merging your own PRs.

1. Wait for required CI on each PR's latest commit. Never merge with failing or pending checks.
2. Get an independent verdict per PR from a reviewer that did not write it (on Claude Code, the `cstack:pr-reviewer` agent). It reads the full diff and the code that calls anything changed, runs the change the way a user would where it can, and reports only real problems: bugs, broken behavior, security issues, missing tests for new logic. Green CI and a bot approval are not verdicts. Fix what it finds, push, and return to step 1.
3. Before trusting an older verdict, confirm it still covers the code: compare `git patch-id` at the reviewed SHA with the current head. A changed patch needs a fresh review.
4. Land bottom-up, one PR at a time. Squash-merge with a head-commit guard so a later push cannot slip in: `gh pr merge <n> --squash --delete-branch --match-head-commit <sha>`, or the REST merge endpoint with `sha=<sha>`.
5. Read the result back: the PR shows merged into the default branch, not into a parent branch or only queued. Retarget the next PR in a stack to the default branch, move its patch onto the merge result, and let its checks rerun before merging it.
6. Stop at the first PR without a current verdict. Report what landed with commit SHAs, each verdict and who produced it, CI on the default branch after the merge, and anything left, such as branches the host would not delete.
