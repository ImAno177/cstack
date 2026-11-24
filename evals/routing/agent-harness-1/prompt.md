---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I'm building my own agent loop around a local 8B model: model adapter, tool registry, permissions and context management. Help me design the runtime and debug why tool calls loop forever.
