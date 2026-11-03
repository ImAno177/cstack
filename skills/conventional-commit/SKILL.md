---
name: conventional-commit
description: Create conventional commit messages following best conventions. Use when committing code changes, writing commit
  messages, or formatting git history. Follows conventional commits specification.
license: MIT
metadata:
  version: 1.0.1
---

# Conventional Commit Messages

Follow these conventions when creating commits.

## Before committing

Inspect the current status, branch, upstream, and intended paths. Follow the repository's `AGENTS.md` for branch and publication policy. Do not stage unrelated work, secrets, generated noise, or temporary files.

```bash
# Check current branch
git branch --show-current
```

If the repository requires a feature branch, use the repository's documented branch prefix and workflow. Do not invent a branch policy in this skill.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

The header is required. Scope is optional. All lines must stay under 100 characters.

## Commit Types

| Type | Purpose |
|------|---------|
| `build` | Build system or CI changes |
| `chore` | Routine maintenance tasks |
| `ci` | Continuous integration configuration |
| `deps` | Dependency updates |
| `docs` | Documentation changes |
| `feat` | New feature |
| `fix` | Bug fix |
| `perf` | Performance improvement |
| `refactor` | Code refactoring (no behavior change) |
| `revert` | Revert a previous commit |
| `style` | Code style and formatting |
| `test` | Tests added, updated or improved |

## Subject Line Rules

- Use imperative, present tense: "add feature" not "added feature"
- Do not capitalize the first letter
- No period at the end
- Maximum 70 characters

## Body Guidelines

- Explain **what** and **why**, not how
- Use imperative mood and present tense
- Include motivation for the change
- Contrast with previous behavior when relevant

## Conventional Commits
The commit contains the following structural elements, to communicate intent to the consumers of your library:

- fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
- feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
- BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
- types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
- footers other than BREAKING CHANGE: <description> may be provided and follow a convention similar to git trailer format.


## Examples

### Simple fix

```
fix(api): handle null response in user endpoint

The user API could return null for deleted accounts, causing a crash
in the dashboard. Add null check before accessing user properties.
```

### Feature with scope

```
feat(alerts): add Slack thread replies for alert updates

When an alert is updated or resolved, post a reply to the original
Slack thread instead of creating a new message. This keeps related
notifications grouped together.
```

### Refactor

```
refactor: extract common validation logic to shared module

Move duplicate validation code from three endpoints into a shared
validator class. No behavior change.
```

### Breaking change

```
feat(api)!: remove deprecated v1 endpoints

Remove all v1 API endpoints that were deprecated in version 23.1.
Clients should migrate to v2 endpoints.

BREAKING CHANGE: v1 endpoints no longer available
```

## Revert Format

```
revert: feat(api): add new endpoint

This reverts commit abc123def456.

Reason: Caused performance regression in production.
```

## Principles

- Each commit should be a single, stable change
- Commits should be independently reviewable
- The repository should be in a working state after each commit

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification)
