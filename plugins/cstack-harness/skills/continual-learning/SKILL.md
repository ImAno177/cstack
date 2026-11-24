---
name: continual-learning
description: "Help an agent improve its reusable skills, rules, and memory from ordered task experience with audit, replay, transfer checks, and retirement. Use when a learning should persist across many episodes and its retention must be measured. Not for mining one episode into skill edits; use `reflect`."
license: MIT
---

# Continual learning

Use this skill to have Codex, Claude Code, Grok Build, or Grok Bot look back at prior work, extract a reusable improvement, and verify it helps later tasks without damaging earlier ones.

Boundary with `reflect`: `reflect` runs once per episode, produces candidate edits from three reviewers, and ends at user approval. This skill takes candidates (from `reflect` or elsewhere), replays them over an ordered task stream, measures retention, and decides promotion or retirement. Hand a one-episode request to `reflect`; hand its Accepted edits here only when they must persist and be measured.

This is agent-side learning through skills, rules, memory, and evaluation. It does not train the model, tune model settings, or make a hook itself learn. For stale wording or rules written for an older model or host, use [prompt-audit](../prompt-audit/SKILL.md).

## Learning loop

1. Capture the episode: task, context, action, outcome, feedback, artifact, evaluator, source, host, and privacy class.
2. Classify the candidate as a fact, procedure, preference, correction, temporary note, or skill change. Keep user-specific information separate from general guidance.
3. Audit the current skill/rule surface for overlap, conflict, stale assumptions, broken references, host boundaries, expiry, and privacy risk.
4. Prefer a narrow, additive, versioned candidate. Keep a working rule when only one episode contradicts it, and promote a self-explanation only with external evidence.
5. Replay representative prior tasks, the triggering task, held-out related tasks, and unrelated protected tasks. Keep the evaluator outside the learner's write scope.
6. Promote a candidate only after the target behavior improves and protected tasks stay within declared tolerances. Record rejected candidates and reasons.
7. Keep the update reversible and idempotent; record provenance, scope, dependencies, evidence, and rollback path.
8. Retire stale, contradicted, unsafe, private, or unused memories and skills.

## Evidence

Keep a result matrix `A[i,j]`: the score for task `j` after update `i`. Report current-task success, average seen-task performance, per-task retention, forgetting or backward transfer, forward transfer on held-out tasks, context/storage/latency cost, and privacy cost. Do not hide a protected regression behind one aggregate score.

Use [the paper notes](references/papers.md) for the research basis and [the agent evaluation protocol](references/agent-evaluation.md) for metrics and promotion gates. Reflection generates candidates; an independent artifact-based evaluator decides whether one is durable. A lifecycle hook may surface an episode or load already-approved context; it must not silently rewrite skills, persist secrets, upload task data, or treat a successful process exit as evidence of learning.

## Not for

- A single completed episode or a one-off lesson; use `reflect`.
- Model training, or comparing configurations with no learning step; use `agent-evaluation`.

## Done when

- `A[i,j]` exists for the declared task stream with evaluator version, and each promoted candidate names its source episode, scope, evidence path, and rollback.
- Any change to the evaluator, task order, or prompt invalidates earlier cells; mark them inconclusive and replay.

## If it fails

- Separate a lost capability from a retrieval or activation failure before editing; change the candidate's scope or trigger, then rerun the full replay.
- Keep tolerances fixed. Reject the candidate and log the reason after two failed revisions.

## Example result

```
step i=3 candidate: <skill>/SKILL.md add rule R7 (evaluator v2)
A[3,3]=0.80 (trigger task)  seen-task avg 0.74 (was 0.71)
forgetting worst: t02 0.9 -> 0.7 (protected, tolerance 0.05) => REJECT
rollback: git revert <sha>
```
