### Hillclimb

Own one metric and the integrity of the experiment. Use for sustained, iterative improvement of one measurable thing against a target. A one-off fix is `bug-fix.md` or `perf-issue.md`.

One change, one measurement, keep or revert. Never stack untested changes, and never claim a win from reading code (`principle-prove-it-works`).

1. Ground the workload before choosing the metric: trace the target, name the dimensions that move the result (data size, state, concurrency), and pick a case that reproduces the complaint. Fix one metric, the direction that counts as better, and a stop predicate that pairs a target with a minimum number of attempts, such as "at least 50% better than baseline and at least 10 iterations".
2. Build the measurement harness as one repeatable command that prints the metric as a median of N runs, its error count, and a count of the work done. Show that it separates an easy case from the target case, vet it with `benchmark-checklist`, then freeze it. Record the baseline and a green run of the regression gate (the tests that must keep passing) before any change.
3. Log every attempt with `show-me-your-work`, one row per attempt with the hypothesis, the before and after values, and `kept` or `reverted`. Read the log before each attempt.
4. Run one hypothesis per iteration. Name a specific mechanism ("defer X off the boot path because it blocks first paint"), make the change, measure with the frozen harness, and run the regression gate. Keep the change only when the metric moves past the run-to-run range and the gate stays green; otherwise revert it in full. Commit each kept change on its own, staging only its files.
5. On a plateau of several reverts in a row, change category, combine near-misses, or re-read the source before concluding. Correctness and simplicity outrank the number: revert a win that breaks behavior, and keep a simplification that holds the number.
6. Stop when the predicate is met or the remaining ideas cost more than they can gain. Never relax the predicate or edit the frozen harness to meet it. Finish with `opening-a-pr.md`, with the kept commits in the order they landed.

Reply with the metric and target, baseline to final with the percent change, iterations kept and reverted, each kept change on one line, the log path, and the next idea you would try.
