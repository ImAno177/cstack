---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

We need to migrate our job queue from Celery to a Postgres-backed queue. It touches the workers, the API, deployment config and a data backfill. Plan it out and carry it through end to end with checks at each step.
