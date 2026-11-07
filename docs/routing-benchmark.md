# Routing benchmark

The 32 cases in `benchmarks/skill-routing/cases.json` distinguish similar skills by outcome, scope, stage, and platform. This is an **evaluation dataset**, not a claim that the router passed.

1. Print the cases: `python scripts/evaluate_skill_routing.py`.
2. Run each task at least 3 times on the **same host, model, tool catalog and permissions** before and after a router change; use 5+ when measuring small gains.
3. Store one JSONL line for each real attempt (no fabricated traces):

```json
{"id":"audit-repo","run":1,"primary":"repo-audit","supporting":[],"success":true,"tokens":1200,"latency_ms":3000}
```

`success` must be based on independent inspection of the resulting artifact or task, not the agent's own completion claim. Save baseline and candidate runs outside the skill directory, then compare:

```sh
python scripts/evaluate_skill_routing.py --baseline baseline.jsonl --candidate candidate.jsonl --output routing-report.json
```

The scorer checks matching (case, run) pairs and reports primary-routing accuracy, supporting-skill precision, outcome success, mean tokens, mean latency, and top confusion pairs. Inspect failures individually. Do not promote a context-saving change that decreases outcome success on protected tasks. Do not call a shorter startup prompt a quality improvement until measured real-task results support it.

## Startup-context experiment

`hooks/cstack-session-start.js` now injects a brief bootstrap by default. To recover the previous full router injection for a controlled baseline, set `CSTACK_ROUTER_MODE=full` in the hook's environment. Compare both modes with the same benchmark. The full routing map remains in `skills/skills-router/SKILL.md` for on-demand reading.
