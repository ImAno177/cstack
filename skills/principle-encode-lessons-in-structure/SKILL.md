---
name: principle-encode-lessons-in-structure
description: Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode
  the rule as a lint, metadata flag, runtime check, or script instead of more text.
disable-model-invocation: true
---

# Encode Lessons in Structure

Turn a recurring instruction into something that fails when it is ignored. Text depends on every future reader noticing it; a check does not.

**Why:** A rule written a second time has already been missed once. Repeating it louder adds context load and still fails silently.

**Pattern:**
- Pick the strongest mechanism that fits, in this order: make the mistake impossible (one source of truth, a type, a deleted option), then a lint or validator whose error names the fix, then a runtime check, then a script that does the step.
- Prove the mechanism fails on the real past mistake before relying on it.
- Run the same check locally and in CI, and delete the prose rule it replaces.

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** If the fix is structural, only use the structural fix. The instruction is the symptom.

For repeated mistakes across a whole repository, run the `correct` skill.
