---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I ran `wrk -t4 -c64 -d30s` against the new caching layer and got 2.3x more requests per second than main. Before I post this number in the PR, sanity-check the measurement: did it measure what I think, is it repeatable, what limited it?
