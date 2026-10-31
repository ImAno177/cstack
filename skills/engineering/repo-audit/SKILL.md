---
name: repo-audit
description: Audit a whole repository for bugs, security holes, load failures, missing tests, slow paths, and code to delete. Use for a repository-wide audit. This skill changes nothing.
---

# Repository audit

Audit the repository and return a ranked report. Do not edit files.

## Inspect

1. Map entrypoints, data flow, storage, external calls, deployment, and expected load.
2. Read the highest-risk paths and their callers. Check tests, configuration, and error handling.
3. Run focused checks when they reveal behavior. Do not turn the audit into a test-suite rewrite.

## Find

- Bugs, invalid states, edge cases, and broken callers.
- Injection, authentication, authorization, secret handling, and data-loss risks.
- Races, unbounded work, poor query complexity, and resource leaks.
- Risky logic without a behavior test.
- Dead code, duplicate paths, unnecessary dependencies, and stale configuration.

Every finding needs a concrete failing case and a file path with a line. Recheck the code before reporting it. Do not report style taste or vague concerns.

## Report

Rank findings as must fix, should fix, or nice to have. For each finding, state what the code does, the failing case, the smallest fix, and the result of skipping it. End with the first fix to make, the paths checked, and material gaps.
