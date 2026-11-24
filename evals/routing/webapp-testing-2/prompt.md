---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

write playwright tests for the checkout flow in our web app and run them against the dev server, i want real browser evidence that add-to-cart through payment works
