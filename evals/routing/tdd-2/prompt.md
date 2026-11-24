---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

users report that the cart total is wrong when a discount code and free shipping are both applied. i want a regression test that reproduces it before you touch the code, then the fix
