---
name: poteto-mode
description: Use a small, deliberate workflow for non-trivial engineering changes that need clear scope, safe edits, and real
  verification.
---

# Poteto mode

Use this workflow when a task spans multiple files or needs an architecture decision.

1. Restate the goal and the smallest complete change.
2. Read the relevant instructions and inspect the real callers, inputs, outputs, and generated artifacts.
3. List the files and interfaces the change must reach.
4. Make the smallest change that preserves the existing structure and error handling.
5. Validate the artifact users will receive. Use an existing check before adding a new one.
6. Report the result, the checks that ran, and the limits that remain.

Use `skills-router` only when more than one skill plausibly owns the request. Choose one primary skill and add a supporting skill only for a concrete required output.

Keep procedures in skills and references. Keep global instructions short. Do not add code comments unless a compiler, tool, license, generated-file marker, or non-obvious external constraint requires one.
