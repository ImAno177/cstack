---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I'm changing `parse_config()` so it returns None instead of raising when the file is missing. It's a 3-line diff but this function is used all over the place. What else could this break outside the diff, and can you prove it's safe?
