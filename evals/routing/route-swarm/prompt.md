---
tags: [routing, via-default-mode]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Fan out parallel workers to check every one of our 40 microservices for the deprecated logging call, one slice each, and give me one combined report with evidence.
