---
name: principle-subtract-before-add
description: Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references before building on the base.
disable-model-invocation: true
---

# Subtract before add

Remove complexity first. Cut dead paths, duplicate instructions, unused references, and speculative guards before adding capability. Design for observed usage, not imagined edge cases.

**Pattern:**
- Sequence removal before construction.
- Cut before you polish: reach the minimum before investing in quality.
- Simplify prompts: remove redundant instructions and excessive templates.
- When a reference has no novel content, delete it rather than leave a stub.
