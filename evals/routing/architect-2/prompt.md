---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

i need to split the monolithic `payments.py` (3k lines) into a proper package with a clean interface for the new Stripe and Adyen providers. design the module structure and the interfaces first, i don't want you to just start moving code around
