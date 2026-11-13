# Changelog

## Unreleased

## 0.5.0

- Add Claude Code subagents in `agents/`: `pr-reviewer` (now on Haiku, ends with `VERDICT: CLEAN` or `VERDICT: PROBLEMS`), `researcher` (read-only, cited report), and `implementer` (branch, checks, and pull request; never merges).
- `default-mode` gains operating lessons: denied tools end the action, one CI watch instead of polling, list-then-delete cleanup, no `git commit -a` in repositories with submodules, Windows Git Bash path and line-ending rules.
- Narrow the descriptions of `find-skills` (only when asked to find or install a skill), `principle-build-the-lever`, `principle-prove-it-works`, and `unslop` (when rewriting AI-sounding prose).
- `AGENTS.md` names the `cstack:pr-reviewer` agent, which runs on Haiku, for the pre-merge review step.
- Add `CONTRIBUTING.md` with contributor guidance for this repository: validators, upstream-synced skills, host sync, and validator-enforced skill rules.

## 0.4.0

Changes from paired Haiku runs of 0.2.0 against 0.3.0 (14 runs, three tasks): agents skipped the owning skill in a third of review runs, three of four built services exposed sequential ids and dropped the connection on a non-ASCII URL, and one baseline agent ran a recursive delete outside its workspace.

- AGENTS.md names the skill that owns each phase (review, bug fix, build, commit, PR, done) and tells agents to open it before acting and to follow its output format exactly.
- AGENTS.md and `principle-boundary-discipline` add safe defaults: unguessable public identifiers, one error format for every request, deliberate handling of each input class, absolute paths for destructive commands.
- `principle-prove-it-works` and the feature playbook add hostile-input probes through the real interface (empty, oversized, non-ASCII, duplicate, concurrent, unsupported, restart).
- `change-review` leads its description with the trigger and requires `What this change does:` as the first line.

## 0.3.0

Changes grounded in 2026 skill-utility research (arXiv 2610.25064, 2610.11647, 2611.04367, 2610.08875, 2610.04832, 2610.14216):

- AGENTS.md policies are direct imperatives instead of condition-first sentences, and agents name the skill that shaped the work.
- The 51 cstack-owned skills other than `frontend-design` and the principles gain `Not for`, `Done when`, and `If it fails` sections where they apply, imperative-first rules, concrete commands, and, for fixed output formats, exactly one worked example that follows every rule of the skill. `conventional-commit` keeps one example instead of six; `create-pr` agrees with `conventional-commit` and `opening-a-pr`.
- `validate_skill_stack.py` enforces `overlap_groups` in `.cstack/skill-policy.json`: overlapping skills must name each other in their descriptions.
- The authoring playbook carries the evidence-based checklist, and `docs/skill-effect-benchmark.md` documents paired, repeated, exposure-aware measurement; the Codex A/B runner records which skills each run opened and per-pair deltas.

## 0.2.0

- Breaking: every skill now lives at `skills/<name>/`, the one-level layout Claude Code, Codex, Cursor, Grok, and the `skills` CLI all scan. The `cloudflare/`, `kaggle/`, `colab/`, `huggingface/`, and `frontend/` group folders are gone, and `.claude-plugin/plugin.json` no longer lists extra skill roots.
- Breaking: remove `skills-router`. Hosts choose skills from their descriptions; overlapping skills now name each other and say when to use which.
- Cloudflare skills are copied verbatim from `cloudflare/skills` by the upstream sync, like Kaggle, Colab, and Hugging Face. `sandbox-sdk` is replaced by upstream's `sandbox-stable`, `sandbox-next`, and `sandbox-migrate-to-next`, and `cf-cli` is added because `wrangler` now defers to it.
- Document installs for Cursor (Agent Plugin) and other Agent Skills hosts through `npx skills add`; ship the Apache-2.0 license text for the synced upstream skills.
## 0.1.7

- Replace `doc`, which carried another project's instructions (AgentOps, an `ocppoc` cluster, missing Council and explorer skills), with `md-docs`, adapted from iliaal/ai-skills, for README.md, AGENTS.md, CLAUDE.md, CONTRIBUTING.md, and DOCS.md.
- Add a principles index (`default-mode/references/principles.md`) with when to apply each of the 24 principles and how to resolve tensions between them; name principles by their skill names.
- Safety: `find-skills` installs only after the user reviews the skill and never passes `-y`; `scientific-slides` no longer reads `.env` from parent directories and asks before sending private decks to OpenRouter.
- Fixes: `create-pr` uses repository PR templates and plain skill references; `swarm` follows `multi-agent-workflow`'s concurrency cap; `ketchup` no longer names a nonexistent `/visualize` command; PEFT and bitsandbytes guides use `dtype` and the current bitsandbytes build.
- Restore pstack depth in `architect`, `arena`, `swarm`, `interrogate`, `how`, `why`, `reflect`, `show-me-your-work`, and `figure-it-out` (phases, rubrics, reviewer prompts, `log.sh`), with host-neutral delegation in `default-mode/references/subagents.md`.
- Hide AI attribution in commits and PRs for Claude Code sessions in this repository with `.claude/settings.json` (`attribution` off).

## 0.1.6

- Add `literature-review`, `security-audit`, and `webapp-testing`; port `tdd`, `create-verification-skill`, and `maintain-verification-skill` from pstack; add the `opening-a-pr`, `babysit`, and `shipping` playbooks to `default-mode`; route them all from `skills-router` and add five routing benchmark cases.
- Credit pstack (MIT, Lauren Tan) in `THIRD_PARTY_NOTICES.md` with its license text, and document where cstack diverges from it.
- Fix audit findings: `doc` no longer requires the missing `code-map-standard` skill and has a usable description; `doc` and `scientific-slides` call bundled scripts relative to the skill directory, not the repository root; rename the Android-only `testing-setup` to `android-testing-setup`; `web-perf` documents adding the Chrome DevTools MCP server on Claude Code and a Lighthouse fallback.
- Claude Code: keep slash-only skills (`ketchup`, `ketchup-video`, `sharpen`, `in-your-own-words`) out of always-on context with `disable-model-invocation`, scope `typescript-best-practices` to `.ts`/`.tsx` files with `paths`, and add a `pr-reviewer` subagent for the pre-merge review.
- Add a root `CLAUDE.md` that imports `AGENTS.md`, and list `.claude-plugin/plugin.json` in the release checklist.
- Add a Claude Code `plugin.json` that exposes all nested skill groups, validate that every skill is discoverable by Claude Code, and give the router Claude equivalents for document skills.
- Propose upstream updates through reviewed pull requests instead of direct pushes to `main`.
- Preserve installed skills on failed upstream replacements and record source revisions in an upstream lockfile.
- Remove the redundant session-start routing hook; keep the optional skills-router for ambiguous tasks and add a 32-case empirical routing benchmark.
- Add release documentation, third-party source notices, license text, and full manifest-path CI coverage.

## 0.1.5

- Current version declared by root, Codex, Grok, and Claude marketplace manifests.
- Existing portable skill catalog and plugin infrastructure.
