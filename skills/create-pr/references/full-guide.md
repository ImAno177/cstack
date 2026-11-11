# Create Pull Request

Open pull requests that a reviewer can judge in one minute.

**Requires**: GitHub CLI (`gh`) authenticated (`gh auth status` exits 0).

## Process

Order matters: commit, verify the branch, read the diff, write the body to a file, push, create.

### Step 1: Commit and verify the branch

Run `git status --porcelain`. Commit every change that belongs in the PR with the `conventional-commit` skill first; leave unrelated work out.

```bash
BASE=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
git status
git log $BASE..HEAD --oneline
```

The result must show a task branch (not `$BASE`) with only this task's commits. When the branch is behind `$BASE`, merge `$BASE` into it; never force-push.

### Step 2: Read what the PR contains

```bash
git log $BASE..HEAD
git diff $BASE...HEAD
```

Understand the scope and purpose of all changes before writing the description.

### Step 3: Write the body

Fill in the repository's template when one exists (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, or `docs/pull_request_template.md`). Otherwise use these paragraphs, in this order:

1. What changed and why, in one short paragraph. Add alternatives you rejected only when they matter.
2. `Scope:` what the PR leaves out.
3. `Blast radius:` what else could be affected, with `file:line` evidence.
4. `Verification:` the real commands you ran and their outcomes.

Rules:
- Link issues or tickets only when one exists.
- Name areas that need careful review.
- Write no `Test plan` heading, no checkbox lists, and no summary that repeats the diff.
- Run the `unslop` skill on the prose, and keep long evidence in a linked artifact.
- End with the attribution line the host or user requires, if any.

### Step 4: Push and create

Write the body to a file first (for example `$TMPDIR/pr-body.md`) so quoting cannot mangle it. Open the PR ready for review; do not pass `--draft`.

```bash
git push -u origin HEAD
gh pr create --title "<type>(<scope>): <subject>" --body-file "$TMPDIR/pr-body.md"
```

Title: Conventional Commits `type(scope): subject`, imperative, lowercase first letter, no trailing period, at most 70 characters. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `chore`.

Keep one concern per PR and keep it reviewable; split unrelated changes into separate PRs.

### Step 5: Check the result

Run `gh pr view --json url,title,body,isDraft`. The URL exists, `isDraft` is `false`, and the title and body match what you wrote. Post the URL. Opening a PR does not authorize a merge.

## Editing an existing PR

Check `gh --version` first.

```bash
# gh 2.82.1 or newer
gh pr edit <number> --title "<new title>" --body-file "$TMPDIR/pr-body.md"

# gh older than 2.82.1, or when gh pr edit fails with "Projects (classic) is being deprecated"
gh api -X PATCH repos/{owner}/{repo}/pulls/<number> -f title='<new title>' -F body=@"$TMPDIR/pr-body.md"
```

## If it fails

- `gh pr create` reports no upstream or unpushed commits: run `git push -u origin HEAD`, then retry.
- The PR already exists: use `gh pr edit`, not a second `gh pr create`.
- Auth errors: run `gh auth status` and fix the login; do not paste tokens into commands.
- Stop and report after two failed attempts with the exact `gh` error. Never drop a format rule to make the command succeed.

## Example

Title:

```
fix(billing): bill late orders on the shop's local day
```

Body:

```markdown
Orders placed after local midnight were billed on the previous day, because the nightly job read "today" from the UTC server clock. The job now computes the day in the shop's time zone, so accounting no longer corrects those orders by hand. Fixes #<issue>.

Scope: only `billing/close_day.py` and its test. The invoice template and CSV export are untouched.

Blast radius: `close_day()` has one caller (`billing/jobs.py:L18`). Reports read stored dates, so they do not change.

Review closely: the time zone comes from `SHOP_TZ` in `billing/config.py:L5`.

Verification: `pytest tests/billing/test_close_day.py` failed before the fix and passes after (4 passed). `ruff check billing` reports no issues.

<attribution line required by the host, if any>
```
