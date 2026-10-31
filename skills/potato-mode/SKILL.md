---
name: potato-mode
description: Use a small, deliberate workflow for non-trivial engineering changes that need clear scope, safe edits, and real
  verification.
---

# Potato mode

Use this workflow when a task spans multiple files or needs an architecture decision. Execute the change; do not stop at a plan.

1. State the outcome and the smallest complete change.
2. Read the applicable instructions and inspect callers, inputs, outputs, configuration, and generated artifacts.
3. Name the files and interfaces the change must reach, including what could break.
4. Make the smallest edit that preserves the existing structure, validation, and error handling.
5. Run the smallest existing check that proves the real artifact works. Add a test only when the change introduces non-trivial behavior.
6. Report what changed, what ran, what was skipped, and any remaining risk.
