---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I want to create a Kaggle Benchmark task that evaluates LLMs on our Vietnamese legal QA dataset, push it with the kaggle CLI, run it and publish the leaderboard.
