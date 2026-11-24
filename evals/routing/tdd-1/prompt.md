---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

There's a bug: `slugify('Ünïcode Title')` returns an empty string. Fix it test-first: write a failing regression test, watch it fail for the right reason, then fix it.
