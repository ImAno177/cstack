---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I just joined the team and need to understand how request authentication works in this codebase, from the HTTP middleware down to the token store. Walk me through the architecture, the runtime flow, and the gotchas.
