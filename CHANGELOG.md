# Changelog

## Unreleased

- Add a Claude Code `plugin.json` that exposes all nested skill groups, validate that every skill is discoverable by Claude Code, and give the router Claude equivalents for document skills.
- Propose upstream updates through reviewed pull requests instead of direct pushes to `main`.
- Preserve installed skills on failed upstream replacements and record source revisions in an upstream lockfile.
- Remove the redundant session-start routing hook; keep the optional skills-router for ambiguous tasks and add a 32-case empirical routing benchmark.
- Add release documentation, third-party source notices, license text, and full manifest-path CI coverage.

## 0.1.5

- Current version declared by root, Codex, Grok, and Claude marketplace manifests.
- Existing portable skill catalog and plugin infrastructure.
