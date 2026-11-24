---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Why does the order service retry exactly 7 times with a 90-second cap? Someone chose those numbers on purpose. Dig through the git history, PRs and issues and tell me the reasoning, citing what the authors wrote.
