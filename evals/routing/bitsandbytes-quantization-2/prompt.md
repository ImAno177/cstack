---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

load this model in 8-bit with bitsandbytes so it fits on the T4, and tell me whether int8 or nf4 is the better trade for our use
