---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

why is the cache layer built as a separate process instead of in-memory in the api? i want the actual design rationale from the commits and pr discussions, not a guess from reading the code
