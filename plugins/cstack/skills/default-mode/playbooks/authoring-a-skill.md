### Authoring a skill

1. Give the skill one recognizable outcome and a description that states what it does, when to use it, and which sibling skill to use instead when one overlaps. Add the sibling to `overlap_groups` in `.cstack/skill-policy.json` so the validator checks both descriptions name each other.
2. Keep `SKILL.md` as the interface. Put conditional detail in focused references, scripts, or assets, and say at the step that needs one exactly when to read it.
3. Write rules as direct imperatives ("Run `x` before y"), not conditions first ("If y, run `x`"). Name the concrete command, path, flag, or identifier each rule needs; prose that names none rarely changes behaviour.
4. Cover, where they apply: when the skill does not apply; required tools with a readiness check; executable invocation with arguments and expected output; ordering and how intermediate artifacts pass; the outcome an alternative method must preserve.
5. End with `Done when` criteria on the real deliverable and an `If it fails` section: how to diagnose, what must change before a retry, when to stop or switch method. Never relax the acceptance criteria during repair.
6. For a fixed output format, end with exactly one worked example and check it against every rule of this skill and of any overlapping sibling. A one-sided example makes agents drop the other skill's rules when both are loaded.
7. Link every supporting file from the entrypoint and avoid copied manuals or placeholder files.
8. Validate metadata, paths, and links with the stack validators. Measure behaviour with the paired protocol in `docs/skill-effect-benchmark.md` when selection or side effects are easy to regress; keep a change only when it fired and helped across repeated runs.
9. Delete prose that does not change a decision.
