---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

PR #482 adds retry logic to the webhook sender (branch `feat/webhook-retries`). Can you review it before I merge? I'm mostly worried about the backoff math and whether it double-sends under concurrency.
