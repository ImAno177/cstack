---
name: skills-router
description: Choose the smallest set of installed skills when a request plausibly matches multiple capabilities or spans domains,
  artifacts, or connected apps. Do not use when one skill clearly owns the request.
license: MIT
---

# Skills router

Use this router only when skill selection is ambiguous or the request spans more than one capability. If the user explicitly names a skill, use it. If one skill clearly owns the task, use that skill directly.

## Routing map

- image generation or raster image editing → imagegen
- DOCX or Word layout, redlining, or comments → documents:documents
- PDF work or visual PDF verification → pdf:pdf
- PowerPoint or presentation work → presentations:Presentations
- spreadsheet files → spreadsheets:Spreadsheets; live Excel → spreadsheets:excel-live-control
- connected Google Drive, Docs, Sheets, or Slides → the matching google-drive skill
- ChatGPT Pages or Spaces → the matching pages skill
- website creation or management → sites:sites; Site remix → sites:sites-remix
- ChatGPT Work pets → the matching work-pets skill
- Cloudflare Workers or platform work → cloudflare, agents-sdk, durable-objects, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, workers-best-practices, wrangler, or turnstile-spin as narrowly matched
- sandboxed or untrusted code execution → sandbox-sdk
- Android AGP migration or native Android testing → agp-9-upgrade or testing-setup
- frontend design, scroll animation, or web performance → frontend-design, gsap-framer-scroll-animation, or web-perf
- test-first coding → tdd
- repository docs, commits, PRs, prose cleanup, architecture, or Kaggle benchmarks → doc, conventional-commit, create-pr, improve-codebase-architecture, or write-kaggle-benchmarks
- AI-sounding prose cleanup → unslop; do not load multiple prose-cleanup skills
- create, install, discover, or manage skills/plugins → skill-creator, skill-installer, find-skills, or plugin-management
- Codex/OpenAI product behavior or configuration → openai-docs
- non-trivial engineering workflow, rigorous verification, or an explicit pstack request → poteto-mode
- pstack command help → poteto-help; pstack model or reasoning setup → setup-pstack
- a named pstack workflow such as investigation, architecture, swarm, interrogation, unslop, or technical writing → the matching pstack skill
- a named pstack principle → the matching principle skill; principles are supporting guidance, not a reason to load the whole set

## Selection rules

1. Choose one primary skill that owns the requested outcome.
2. Add a supporting skill only when it contributes a concrete required part.
3. For combined work, order skills as domain or artifact, implementation, then validation or review.
4. Read the selected SKILL.md before acting and follow its required tools, references, and validation.
5. Do not load every skill, use unrelated skills, or invent a skill when the installed catalog has no match.
6. When two skills have the same or overlapping purpose, select one canonical skill: prefer the narrower, current, or plugin-managed version, and do not invoke both unless the second contributes a concrete independent requirement.
7. If a requested capability is absent, state that briefly and continue only with a clearly suitable alternative.

