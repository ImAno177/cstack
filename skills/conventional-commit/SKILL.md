---
name: conventional-commit
description: Create conventional commit messages following best conventions. Use when committing code changes, writing commit
  messages, or formatting git history. Follows conventional commits specification. Not for branch, push, or PR policy; follow the repository's AGENTS.md for those.
license: MIT
metadata:
  version: 1.0.1
---

# Conventional Commit Messages

Follow these conventions when creating commits.

## Before committing

Inspect the current status, branch, upstream, and intended paths. Follow the repository's `AGENTS.md` (or `CLAUDE.md` on Claude Code) for branch and publication policy. Do not stage unrelated work, secrets, generated noise, or temporary files.

```bash
git status --short
git branch --show-current
git diff --staged --stat
```

Use the repository's documented branch prefix and workflow when it requires a feature branch. Do not invent a branch policy in this skill.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

The header is required. Scope is optional. Keep every line under 100 characters.

## Commit Types

| Type | Purpose |
|------|---------|
| `build` | Build system or CI changes |
| `chore` | Routine maintenance tasks |
| `ci` | Continuous integration configuration |
| `deps` | Dependency updates |
| `docs` | Documentation changes |
| `feat` | New feature (MINOR in SemVer) |
| `fix` | Bug fix (PATCH in SemVer) |
| `perf` | Performance improvement |
| `refactor` | Code refactoring (no behavior change) |
| `revert` | Revert a previous commit |
| `style` | Code style and formatting |
| `test` | Tests added, updated or improved |

## Subject Line Rules

- Use imperative, present tense: "add feature" not "added feature"
- Start with a lowercase letter
- End without a period
- Keep the subject at most 70 characters

## Body Guidelines

- Explain **what** and **why**, not how
- Write the change itself in imperative mood and present tense
- State the motivation and the previous behavior as plain facts
- Wrap lines under 100 characters

## Breaking changes and footers

- Mark a breaking change with `!` after the type or scope, and add a `BREAKING CHANGE: <description>` footer (MAJOR in SemVer). Any type can break.
- Write other footers as git trailers, such as `Refs: #<ticket>`.
- For `revert`, use the reverted commit's header as the subject, then `This reverts commit <sha>.` and the reason in the body.

## Done when

- `git log -1 --format=%B` shows the message, and `git log -1 --format=%B | awk 'length > 99'` prints nothing.
- The type is from the table, the subject is lowercase with no period and at most 70 characters, and the staged diff holds only this change.

## If it fails

Amend an unpushed commit with `git commit --amend`; never rewrite a pushed commit. Keep every rule above while fixing it.

## Example

```
fix(api): return 404 for deleted user accounts

The user endpoint dereferences a null record for deleted accounts and
the dashboard fails to load. Return 404 for them instead.

Refs: #<ticket>
```

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification)
