---
name: continual-learning
description: Help an agent improve its reusable skills, rules, and memory from ordered task experience with audit, replay,
  transfer checks, and retirement.
license: MIT
---

# Continual learning

Use this skill when Codex, Grok Build, or Grok Bot should look back at prior work, extract a reusable improvement, and verify that the improvement helps later tasks without damaging earlier ones.

This is agent-side learning through skills, rules, memory, and evaluation. It does not train the model, tune model settings, or make a hook itself learn. For stale wording or rules written for an older model or host, use [prompt-audit](../prompt-audit/SKILL.md).

## Learning loop

1. Capture the episode: task, context, action, outcome, feedback, artifact, evaluator, source, host, and privacy class.
2. Classify the candidate as a fact, procedure, preference, correction, temporary note, or skill change. Keep user-specific information separate from general guidance.
3. Audit the current skill/rule surface for overlap, conflict, stale assumptions, broken references, host boundaries, expiry, and privacy risk.
4. Prefer a narrow, additive, versioned candidate. Do not overwrite a working rule from one episode or promote a self-explanation without external evidence.
5. Replay representative prior tasks, the triggering task, held-out related tasks, and unrelated protected tasks. Keep the evaluator outside the learner's write scope.
6. Promote only when the target behavior improves and protected tasks stay within declared tolerances. Record rejected candidates and reasons.
7. Keep the update reversible and idempotent; record provenance, scope, dependencies, evidence, and rollback path.
8. Retire stale, contradicted, unsafe, private, or unused memories and skills instead of accumulating them forever.

## Evidence

Keep a result matrix `A[i,j]`: the score for task `j` after update `i`. Report current-task success, average seen-task performance, per-task retention, forgetting or backward transfer, forward transfer on held-out tasks, context/storage/latency cost, and privacy cost. Do not hide a protected regression behind one aggregate score.

Use [the paper notes](references/papers.md) for the research basis and [the agent evaluation protocol](references/agent-evaluation.md) for metrics and promotion gates. A lifecycle hook may surface an episode or load already-approved context; it must not silently rewrite skills, persist secrets, upload task data, or treat a successful process exit as evidence of learning.
