# Incident-driven guards

Use this reference when converting an agent failure into a reusable rule. The Reddit links below are operational anecdotes, not normative engineering evidence; they are useful because they expose failure shapes that a clean demo can hide.

| Failure shape | Smallest guard | Evidence to retain | Owning cstack skill |
| --- | --- | --- | --- |
| A verifier silently checked zero items | Assert the expected subject count and matched-evidence count before returning pass | Scope, expected count, matched count, unknown reason | `agent-completion`, `agent-evaluation` |
| A hook or worker leaked processes or touched an unsaved artifact | Give each operation an identity, timeout, owner, and cleanup receipt | Process or artifact identity, cleanup result, stop reason | `agent-harness`, `principle-make-operations-idempotent` |
| Fan-out spawned too many expensive workers | Require explicit model, depth, concurrency, token, and time budgets | Spawn decision, budget, worker result, cancellation result | `multi-agent-workflow` |
| A driver exhausted context between execution and review | Checkpoint durable state before compaction and start the next phase from a compact handoff | Checkpoint path, summary version, replay boundary | `agent-context`, `default-mode` |
| A local model hallucinated tools or a changing tool list destroyed cache locality | Keep a small phase-stable catalog and defer discovery to a boundary | Catalog version, tool-validation result, phase id | `agent-harness`, `tool-orchestration` |
| Batching hid a failed or overlapping write | Batch only read-only or disjoint calls, define result order, and retain each outcome | Per-call status, resource set, ordering, retry identity | `tool-orchestration` |
| The skill stack grew faster than its measured value | Require an activation reason and representative eval; retire unused additions | Activation count, outcome delta, load cost, retirement date | `prompt-audit`, `continual-learning` |

## Procedure

1. Record the incident and the smallest reproducible trace.
2. Add one guard at the boundary where the failure first becomes observable.
3. Run the failing case and a control case; distinguish `pass`, `fail`, and `unknown`.
4. Store the evidence needed to replay the decision without trusting the final model text.
5. Remove or revise the guard when the incident no longer reproduces and its maintenance cost exceeds its measured value.

## Incident sources

- [19 hooks, 36 skills setup](https://www.reddit.com/r/ClaudeCodeTLDR/comments/1w6ohxp/tldr_my_claude_code_setup_after_7_months_of_daily/) reports orphaned processes, runaway subagents, batching failures, and a verifier that matched zero of 154 verdicts.
- [Scripted automated compaction](https://www.reddit.com/r/ClaudeCode/comments/1w7vopj/scripted_automated_compaction_in_driver_skills/) describes context overload between execution and review and the value of durable pre-compaction state.
- [Harnesses for local models](https://www.reddit.com/r/ollama/comments/1tn3l7y/harnesses/) describes hallucinated tool names and invalid tool-call JSON when the tool surface is too broad.
- [KV-cache harness failure](https://www.reddit.com/r/AI_Agents/comments/1xe90df/psa_if_you_build_agents_my_harness_was_silently_breaking_its_own_kv_cache_43_of_a_run/) describes latency from changing prompt and tool-set shape during a run.
- [Minimal Claude Code setups](https://www.reddit.com/r/ClaudeCode/comments/1rovknm/am_i_using_claude_code_wrong_my_setup_is_dead/) argues for adding skills from repeated friction and deleting complexity that does not earn its load cost.
