---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

is this flask app safe to put on the public internet? check for secrets in the repo, sql injection, broken access control, that kind of thing
