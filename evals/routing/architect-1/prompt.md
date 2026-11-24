---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Before anyone writes code: we're adding multi-tenant billing to the orders service, which touches the orders, invoicing and auth modules. Sketch the types, function signatures and module boundaries first, and give me two different designs to compare.
