---
name: conventional-commit
description: Write Conventional Commit messages for code changes and git history.
license: MIT
---

# Conventional commits

Use this format:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

The header is required. Keep it under 70 characters. Use an imperative, lower-case subject with no final period. Keep all lines under 100 characters.

Allowed types include `build`, `chore`, `ci`, `deps`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, and `test`.

Use the body for the reason and user-visible effect. Add a footer for issue references or `BREAKING CHANGE: ...`. Add `!` after the type or scope for a breaking change.

Prefer one stable, reviewable change per commit. Do not invent a scope. Inspect the actual diff before writing the message.

```text
fix(api): reject an empty webhook secret

Reject empty secrets before the request reaches the signer. This prevents
unsigned callbacks from being accepted.
```

See the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/).
