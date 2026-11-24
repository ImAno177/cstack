---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

review the types in `src/state/store.tsx`. there are a lot of `as` casts and optional fields that are really required, clean it up the right way
