---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

i want our agent's learned rules to persist across episodes, but only the ones that actually improve results over time. design the replay, transfer check and retirement process
