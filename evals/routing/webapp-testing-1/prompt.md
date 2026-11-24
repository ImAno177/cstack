---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Prove the signup flow of our Next.js app actually works the way a user would experience it: start the app, drive the form in a real browser with Playwright, and check what ends up in the database.
