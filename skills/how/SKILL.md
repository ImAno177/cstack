---
name: how
description: Explain how a codebase works, where behavior belongs, and what a change can affect before implementation.
---

# How

Use this skill for a code walkthrough, ownership question, placement question, or non-trivial change that needs a working mental model.

1. State the question and the boundary being investigated.
2. Read the entrypoint, callers, configuration, data flow, and closest validation.
3. Trace the path from input to observable output.
4. Name the ownership boundary, hidden state, error path, and relevant gotchas.
5. Present the explanation with `Overview`, `How it works`, `Where things live`, and `Gotchas` sections when they apply.

Use the smallest evidence set that answers the question. Do not invent runtime behavior that the code or a command did not show.
