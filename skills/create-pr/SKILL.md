---
name: create-pr
description: Create Pull Requests following best conventions. Use when opening PRs, writing or editing PR descriptions, or preparing changes for review. Not for committing (use `conventional-commit`), reviewing a diff (use `change-review`), or merging (use `default-mode` and its shipping playbook).
license: MIT
compatibility: Requires GitHub CLI (gh) authenticated and available
metadata:
  version: 1.2.0
---

# create-pr

Read [the full guide](references/full-guide.md) before running `gh pr create` or `gh pr edit`. Check readiness with `gh auth status`.

## Not for

- Committing, reviewing or merging; those have their own skills (see description).

## Done when

- `gh pr view --json url,title,body,isDraft` shows a ready (not draft) PR whose title is `type(scope): subject` and whose body follows the guide.

## If it fails

- Read the `gh` error before retrying and change the cause (auth, unpushed branch, template, `gh` version); the guide lists the fixes. Do not relax the format to get the PR created.
