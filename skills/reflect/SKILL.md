---
name: reflect
description: Mine a completed or failed agent episode for durable improvements, route each learning to an existing skill or rule, and separate accepted edits from rejected and deferred candidates.
---

# Reflect

Use after a non-trivial episode or explicit reflection request. Do not turn a one-off preference or private detail into a global rule.

1. Capture the task, host, actions, outcome, feedback, artifact, evaluator, and privacy class from the current episode.
2. Review the relevant transcript and repository state in bounded slices. Skip unrelated chats and never read another workspace's history.
3. Produce candidates as facts, procedures, corrections, preferences, or skill changes. For each, name the supporting evidence, scope, conflict, overlap, and expiry risk.
4. Prefer encoding a recurring lesson in structure, metadata, validation, or a narrow skill over adding repeated prose.
5. Replay the triggering task, representative prior tasks, a held-out related task, and one protected unrelated task. Keep the evaluator outside the learner's write scope.
6. Accept only candidates that improve the target behavior without protected regression. Apply accepted edits through the owning skill, record rejected candidates, and leave deferred work explicit.

Hooks may load approved context or surface an episode. They must not silently rewrite skills, persist secrets, or treat a successful process exit as evidence of learning.
