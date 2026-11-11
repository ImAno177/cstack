# Changelog

## Unreleased

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
