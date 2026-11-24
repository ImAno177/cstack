---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

delegate the research to a few subagents in parallel: one reads the postgres docs, one reads our schema, one checks the github issues. then combine and verify what they report
