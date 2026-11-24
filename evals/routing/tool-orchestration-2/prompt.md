---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

my agent calls the same lookup tool serially 50 times per task. should those be parallel, programmatic or batched? work out the right execution strategy given the dependencies
