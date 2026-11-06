## Merging pull requests
You have standing permission to merge your own PRs. Do not ask me first.
Before merging:
1. Wait for CI to pass on the PR's latest commit.
2. Start a subagent to review the PR. Give it the PR number and have it read the
   full diff (`gh pr diff <n>`) and the code that calls anything changed. It
   reports real problems only: bugs, broken behaviour, security issues, missing
   tests for new logic. Style preferences don't count.
3. If the review finds problems, fix them, push, and go back to step 1.
4. When CI is green and the review is clean, merge with
   `gh pr merge <n> --squash --delete-branch --match-head-commit <sha>`,
   using the commit the review and CI actually checked.
Never force push, and never merge with failing or pending checks.
