### Opening a PR

Run at the end of any playbook that changes a repository.

1. Work on a task branch or worktree off the default branch, never on a shared branch. Keep unrelated local work out of it.
2. Rebase into small, ordered commits that each land on their own. Write messages with `conventional-commit`; commit bodies explain why and do not restate the subject.
3. Before opening, run `unslop` on the prose you wrote and the repository's required checks, and read the full diff yourself (`git diff --staged`, then `git diff <default>...HEAD`).
4. Open the PR ready for review, not as a draft, using `create-pr`. Title: Conventional Commits `type(scope): subject`. Body: a one-minute briefing for a reviewer who has the diff, with why, what changed, scope and what it leaves out, blast radius, and verification as real commands and outcomes, with no `Test plan` heading and no checkbox lists. Put long evidence in a linked artifact, not the body.
5. Prefer several narrow PRs to one large one. Stack a PR on its parent's branch only when it needs the parent's code; branch independent work from the default branch.
6. Post the URL and keep working. Opening a PR does not start `babysit.md`, and does not authorize a merge.
