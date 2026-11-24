---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I'm writing a new `src/api/client.ts` for our REST API. Make the types strict: no `any`, parse the JSON responses at the boundary, and use discriminated unions for the error cases.
