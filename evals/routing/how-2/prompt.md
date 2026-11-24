---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

how does the plugin loading system in this repo actually work? where do plugins get discovered, how are they ordered, what happens when one fails to load? i need to change it next week
