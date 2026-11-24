---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

This script makes 300 independent API calls one at a time and takes 20 minutes. Decide which calls can run in parallel, which should be batched offline, and which have side effects that must stay sequential.
