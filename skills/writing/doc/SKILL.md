---
name: doc
description: Generate and validate repository docs, READMEs, and open-source doc packs. Use for documentation work.
metadata:
  capabilities: [doc]
  effects: [write_documentation]
  canonical_status: canonical
  disposition: keep_specialist
  tier: product
---

# Documentation

Ground every claim in the current repository. Keep the selected mode explicit and run its checks.

## Modes

- Default: document code and APIs, map the code, and report coverage.
- `readme`: interview the repository, write a problem-first README, de-slop it, and validate it.
- `oss`: audit the open-source doc pack and create missing files. Do not overwrite existing operator-owned docs unless the user asks.

Read the matching reference before using `readme` or `oss` mode:

- `references/readme-craft.md`
- `references/oss-pack.md`

## Default workflow

1. Detect the project from its manifests, source tree, and existing `docs/`.
2. Enumerate bounded areas to research. Mark each area read, skimmed, or skipped.
3. Run the requested discovery, coverage, generation, or validation command.
4. Write the report to `.agents/scratch/doc/YYYY-MM-DD-<target>.md`.
5. Report changed paths, coverage, gaps, validation results, and one non-obvious design fact.

Use `references/default-mode.md` for exact command shapes and report fields. Use `references/de-slopify.md` for README prose.

## Completion rules

- Every claim has a source in code, configuration, or existing docs.
- Generated docs keep useful existing detail.
- Reports disclose skipped areas and unresolved gaps.
- Run the validation script in the skill directory and the mode-specific checks.
