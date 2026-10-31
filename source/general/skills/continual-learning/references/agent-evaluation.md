# Agent and skill evolution evaluation

## Task stream

Version an ordered stream of tasks with prompts, expected observable outcomes, environment state, evaluator, and declared protected-task tolerances. Keep held-out related tasks and unrelated safety or regression tasks outside the learner's write scope. Never let the learner edit the evaluator or reorder the stream after seeing results.

## Result matrix

Record `A[i,j]`, the score for task `j` after the update produced at step `i`. Record the evaluator version, skill-bank version, retrieved context, token and latency cost, storage change, privacy class, and evidence for every cell.

For `n` observed tasks, report:

- current learning: `A[n,n]`;
- average seen-task performance: `1/n * sum(A[n,j])`;
- forgetting at task `j`: `max_i A[i,j] - A[n,j]`;
- backward transfer: `1/(n-1) * sum(A[n,j] - A[j,j])` for `j < n`;
- forward transfer: held-out task score minus the no-update baseline;
- worst protected-task regression, not only the mean.

If scores are binary, include confidence intervals or repeated runs when the task cost permits. If the evaluator, environment, task order, or prompt changes, mark the comparison inconclusive instead of claiming learning.

## Promotion gate

Require a successful triggering task, replay of representative prior tasks, a held-out transfer check, and no protected regression beyond its declared tolerance. A single success, self-critique, retrieval hit, or hook exit is only a candidate signal. Re-run failures with an independent or externally grounded evaluator before promotion.

Prefer a small replay set selected by task family, failure mode, and dependency rather than indiscriminate history. More context can reduce performance through distraction, privacy exposure, or stale instructions.

## Failure analysis

Distinguish erased capability from retrieval or activation failure by testing alternate prompts, retrieval queries, and context budgets. Flag self-feedback loops, task-specific overfitting, fragmented skill accumulation, contradictory memories, preference leakage, evaluator contamination, and negative transfer. Retire or quarantine a candidate when its source, scope, expiry, or rollback path is unclear.

## Hook boundary

The lifecycle hook may collect a redacted episode envelope or point to a pending candidate. It must not silently rewrite shared skills, upload task data, persist secrets, or promote a candidate. It should fail open and leave the repository unchanged when its host, storage, or evaluator is unavailable.
