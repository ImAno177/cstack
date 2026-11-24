---
tags: [routing, via-default-mode]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Stress-test my design for the new distributed lock: have independent adversaries try to break it, and keep only the findings they can prove with a run.
