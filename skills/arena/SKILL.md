---
name: arena
description: Run isolated alternative attempts at the same design or artifact, compare them against a declared rubric, and graft only proven improvements. Use for design bakeoffs or when one attempt could lock in the wrong shape.
---

# Arena

Use an arena only when alternatives can be judged independently and the comparison is worth the extra work.

1. Define the artifact, the done predicate, and three to six gradeable criteria before spawning workers.
2. Give every candidate the same task contract and an isolated output path or worktree.
3. Run candidates concurrently with a bounded budget. Each candidate reports the artifact, evidence, rejected alternatives, and known gaps.
4. Cross-judge the candidates with a read-only reviewer that did not produce them. The judge applies the rubric and points to evidence.
5. Pick a base, graft only changes supported by the rubric, and discard the rest.
6. Re-run the done predicate on the final artifact and report dropouts, discarded work, and unresolved gaps.

Do not let candidates edit shared state. Do not select by prose quality, worker confidence, or a clean process exit.
