---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

This refactor is going to take hundreds of tool calls across a huge repo and the context keeps getting compacted. Set up checkpoints and compact handoff notes so the work stays coherent across phases.
