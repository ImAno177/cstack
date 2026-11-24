---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

the agent keeps re-reading the same files and losing track after compaction on this long migration. how do we structure the run with bounded phases and checkpoints so it doesn't loop
