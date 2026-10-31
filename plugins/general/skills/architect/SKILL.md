---
name: architect
description: Define data shapes, interfaces, ownership, and error boundaries before a change crosses a module or function
  boundary.
---

# Architect

Use this skill for a change that crosses a function, module, package, or service boundary.

1. Read the current implementation and every caller that the change can affect.
2. Write the data shapes, public signatures, ownership, and error boundaries.
3. Compare the proposed shape with the existing module boundaries.
4. Choose the smallest design that keeps invalid states and duplicate work out of callers.
5. Implement the chosen shape and verify the affected callers.

Skip this skill when one existing owner and one existing interface already make the change obvious.
