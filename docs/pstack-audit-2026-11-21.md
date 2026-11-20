# pstack full-inventory review for cstack

Reviewed on 2026-11-21 against pstack 0.15.46 (cursor/plugins commit aaeb0ea3a0584995aa8f55ce44c6c5259414b896, 2026-11-20) and cstack main 688d3853713761b0cfc2f72967144220f050ce81 (2026-11-20).

Source: https://github.com/cursor/plugins/tree/main/pstack

## Inventory and conclusions

- pstack has 58 public skills. Fifty-one have a name-equivalent or renamed counterpart in cstack 0.7.0, including all 24 principles. Seven are absent by name; adding all seven would duplicate behavior or couple cstack to Cursor.
- pstack's main mode includes 22 playbooks: 12 existed in cstack; seven portable missing workflows are brought in by this change; three remain separate candidates.
- pstack also bundles two Cursor subagents, a large, tested PR watcher, a worktree-audit shell script, TLA+ statechart tooling with tests/fixtures, and the dormant Benny two-automation package. These are not interchangeable with host-neutral skills.

## The seven missing public skills

| pstack skill | Decision | Reason |
| --- | --- | --- |
| recall | Add portable cstack skill | Prior conversations plus current repository facts solve a distinct problem from ketchup (this chat) and agent-context (state capture). |
| automate-me | Defer | Its preference mining overlaps reflect and continual-learning; personal mode generation needs an explicit target and held-out evaluation. |
| setup-pstack | Do not copy | Cursor-specific model slugs and persistent rule path; cstack already supports host-specific worker configuration in default-mode/references/subagents.md. |
| poteto-help | Do not copy | An additional router contradicts cstack's host-native skill-discovery policy. |
| no-comments | Do not copy | An aggressively comment-deleting subagent duplicates cstack's code/comment policy and can erase useful constraints. |
| make-bot-ui | Do not copy | Depends on Grok Bot routines, secret-request actions, and Tailscale choices; better as a separately scoped integration. |
| bro | Do not copy | One instruction to simplify the previous reply does not justify a listed skill. |

## The 51 existing counterparts

The following 27 workflow skills already exist, often adapted rather than copied verbatim:

architect, arena, benchmark-checklist, blast-radius, correct, create-formal-verification-skill, create-verification-skill, figure-it-out, how, in-your-own-words, interrogate, ketchup-video, ketchup, maintain-formal-verification-skill, maintain-verification-skill, poteto-mode -> default-mode, reflect, sharpen, show-me-your-work, statechart, swarm, tdd, teach, technical-writing, typescript-best-practices, unslop, why.

All 24 principle skills already exist in cstack:

principle-attack-the-premise, principle-boundary-discipline, principle-build-the-lever, principle-encode-lessons-in-structure, principle-exhaust-the-design-space, principle-experience-first, principle-explain-the-number, principle-fix-root-causes, principle-foundational-thinking, principle-guard-the-context-window, principle-laziness-protocol, principle-make-operations-idempotent, principle-migrate-callers-then-delete-legacy-apis, principle-minimize-reader-load, principle-model-the-domain, principle-never-block-on-the-human, principle-outcome-oriented-execution, principle-prove-it-works, principle-redesign-from-first-principles, principle-separate-before-serializing-shared-state, principle-sequence-verifiable-units, principle-subtract-before-you-add, principle-test-behavior-not-implementation, principle-type-system-discipline.

Three portable cstack names omit redundant words: principle-exhaust-design-space, principle-never-block-on-human, and principle-subtract-before-add. The other 21 retain their names. Preserve cstack's existing validation and host neutrality instead of overwriting those 51 skills.

## All 22 playbooks

| pstack playbook | cstack outcome |
| --- | --- |
| authoring-a-skill | Already present |
| autonomous-run | Added, with an explicit host scheduling boundary |
| autopilot-full | Deferred: requires per-PR ownership, trustworthy workers, and safe merge control |
| autopilot-stack | Deferred with autopilot-full; no implicit merge rights |
| babysit | Already present, keeps conservative no-rebase policy |
| bug-fix | Already present |
| eval | Already present |
| feature | Already present |
| hillclimb | Added: fixed harness, single hypothesis, keep/revert, budget |
| investigation | Already present |
| multi-phase-plan | Already present |
| opening-a-pr | Already present |
| pause-safely | Added: durable checkpoint and no destructive cleanup |
| perf-issue | Already present |
| prototype | Already present |
| refactoring | Already present |
| runtime-forensics | Added: live capture separated from a fix |
| session-pickup | Added: resume one run without replaying completed work |
| shipping | Already present, requires head-SHA verification |
| trace-forensics | Added: work from a fixed capture, source attribution |
| visual-parity | Added: immutable visual baseline and fixed threshold |
| worktree-cleanup | Deferred: destructive operations need a tested, cross-platform read-only audit |

## Other components examined

| Component | What is useful | Recommendation |
| --- | --- | --- |
| poteto-agent / worker.md | Standalone brief, explicit budget, evidence at handoff | Existing multi-agent-workflow and subagents reference cover the portable contract; avoid forced model identifiers. |
| comment-sicko | Independent code/comment cleanup | Do not add automatic comment deletion. |
| watch-pr CLI (github.ts, policy.ts, types.ts, tests) | Typed PR states, CI/review blockers, bounded retry and machine-readable verdicts | Future standalone PR: reuse policy ideas but test them against GitHub API and cstack's current merge requirements. |
| worktree-audit.sh | Read-only audit of WIP, PR status, merged base, disk use | Good standalone candidate after portability and pinned-session tests. Never auto-delete. |
| statechart scripts and fixtures | TLA+ model checking, state counterexamples, diagrams and differential tests | Already present in cstack, but upstream code diverged. Compare and selectively sync under dedicated test coverage. |
| Benny automation pack | Two-stage Slack report triage -> trusted marker -> repeatable UI reproduction -> draft PR | Do not bulk-copy Cursor-only automations. Extract the fail-closed gates into a separate provider-neutral design only if cstack gains an issue-intake workflow. |
| make-bot-ui | Server-side webhook credentials; no browser secrets | Existing Cloudflare/agent integrations can reuse the security principle, not the Cursor/Grok routine protocol. |
| setup-pstack and 10 guide chapters | Per-role model budgets; skill/task examples | Keep model availability host-defined; do not hardcode dated model slugs. |

## Safety and verification

- Maintain native skill discovery; do not add a routing hook or hidden startup prompt.
- Do not treat host-specific Cursor paths, cloud-agent controls, model identifiers, or automations as portable dependencies.
- Keep live and offline forensics read-only; require separate implementation authorization.
- For autonomous work, only claim continued operation after a real supported scheduler or worker is configured.
- For visual parity, freeze the baseline and threshold before implementation.
- After changing the catalog, validate plugin structure, cross-links, the generated Grok index, and real routing probes before claiming an improvement.

## Evaluation targets

1. A project-wide historical recall should select recall, not ketchup or agent-context.
2. A known branch takeover should select default-mode's session-pickup, not bulk history mining.
3. Sustained quantitative optimization should select hillclimb inside default-mode and preserve baseline/guardrail artifacts.
4. A fixed trace should select trace-forensics, while a live process diagnosis selects runtime-forensics.
5. A paused task should have a readable checkpoint and no accidental merge, deletion, or claimed background worker.

The 37-case pre-change routing suite is an evaluation dataset, not measured proof. New routing cases cover these boundaries; repeat host-native trials before attributing quality gains to this port.
