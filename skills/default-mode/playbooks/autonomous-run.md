### Autonomous run

Drive a bounded task toward a verifiable exit condition using the current host's actual continuation mechanism.

1. State an observable done predicate, explicit scope, iteration limit or budget, and stop conditions before the first pass.
2. If the host supports a durable scheduled or event-based wake, use it for the specific dependency and persist state through agent-context. Otherwise run only the iterations possible in this session. Never promise continued background work without a running scheduler.
3. Each iteration reads the checkpoint, takes the smallest evidence-supported action, verifies the predicate, and records the result through show-me-your-work. Keep useful changes; discard speculative ones.
4. Separate side quests and unrelated failures from the original goal. Do not escalate authority for deployments, deletion, external messaging, or merges. A failed check is a reason to diagnose, not to quietly weaken the check.
5. If the task stalls, pivot once on new evidence or stop at the declared budget and report the blocked predicate. Checkpoint before a handoff or pause.

**Reply:** predicate, iterations actually run, accepted and discarded changes, durable checkpoint, actual completion state, and any wake still configured.
