---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

i've got uncommitted changes in the auth middleware, about 200 lines. give it a proper review before i commit: correctness, security, anything that falls over under load, missing tests
