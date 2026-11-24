---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

we bumped the default timeout in the shared http client from 30s to 5s. before this ships, figure out what in the rest of the codebase could break because of it, beyond the files I touched
