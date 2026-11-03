---
name: principle-laziness-protocol
description: Apply when refactoring, sizing a diff, or feeling tempted to add abstractions, layers, or signal threading. Prefer deletion and the smallest change that solves the problem.
---

# Laziness protocol

- Put repeated decisions behind one source of truth.
- Prefer fewer lines and fewer layers over elegant boilerplate.
- Delete dead paths and redundant configuration before adding new structure.
