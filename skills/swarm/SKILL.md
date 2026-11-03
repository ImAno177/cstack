---
name: swarm
description: Fan out bounded workers across independent coverage slices or identical race attempts, drain them, and return one evidence-backed report. Use for parallel research, audits, or verification.
---

# Swarm

1. State the done predicate and the report or artifact the swarm must return.
2. Choose one shape: disjoint slices, identical race attempts, or a declared mixture. State the selection rule before spawning.
3. Give each worker an isolated scope, exact inputs, verification command, and result schema. Measurements include the sample method and relevant revision.
4. Start all independent workers with bounded retries and no nested delegation.
5. Read terminal results. A missing SHA, method, scope, or evidence is a gap, not a pass. Respawn once only when the missing proof is recoverable.
6. Consolidate findings, drop duplicates, name dropouts and gaps, and verify the final claims against the real artifacts.

Do not paste raw worker reports into the final answer. Do not hide an uncovered slice behind an aggregate result.
