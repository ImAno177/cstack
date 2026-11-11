---
name: principle-prove-it-works
description: Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read
  the actual value, inspect the diff), not a proxy, self-report, or 'it compiles', and probe it with hostile inputs (empty, oversized, non-ASCII, concurrent, unsupported).
---

# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

## Probe hostile inputs through the real interface

Passing the happy path proves little. Before declaring done, drive the real entry point (the CLI, the HTTP port, the public function) with each class below and read the result back end to end:

- empty, missing, and wrong-type fields;
- oversized input;
- non-ASCII text, sent in and read back out through every route that returns it;
- the same request twice, and many at once (`threading` or `xargs -P`) when state is shared;
- every method or subcommand the interface can receive but does not support;
- a restart, when state persists.

Each probe ends in a correct result or the documented error. A stack trace, a framework default page, a dropped connection, or a silent wrong answer is a failed probe: fix it or list it as unfinished.

## Script the check when you can

The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Write the script, run it, and keep its output as an artifact a reviewer can re-run instead of trusting your word.

Keep the artifact visible for the human. Record the decision trail only when the work is large or complex enough that a reviewer needs it later.
