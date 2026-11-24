---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

our custom agent harness keeps losing tool results between turns and the permission checks are inconsistent. help me debug and redesign the loop, the tool registry and the state handling
