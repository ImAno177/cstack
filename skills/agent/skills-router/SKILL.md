---
name: skills-router
description: Choose the smallest set of installed skills when a request plausibly matches multiple capabilities or spans domains,
  artifacts, or connected apps.
license: MIT
---

# Skills router

Use this router only when selection is ambiguous or the request spans more than one capability. If the user explicitly names a skill, use it. If one skill clearly owns the task, use that skill directly.

## Routes

- image generation or raster image editing → `imagegen`
- DOCX or Word layout, redlining, or comments → `documents:documents`
- PDF work or visual PDF verification → `pdf:pdf`
- PowerPoint or presentation work → `presentations:Presentations`
- spreadsheet files → `spreadsheets:Spreadsheets`; live Excel → `spreadsheets:excel-live-control`
- connected Google Drive, Docs, Sheets, or Slides → the matching `google-drive:*` skill
- ChatGPT Pages or Spaces → the matching `pages:*` skill
- website creation or management → `sites:sites`; Site remix → `sites:sites-remix`
- ChatGPT Work pets → the matching `work-pets:*` skill
- Cloudflare work → the narrowest matching skill among `cloudflare`, `agents-sdk`, `durable-objects`, `cloudflare-email-service`, `cloudflare-one`, `cloudflare-one-migrations`, `workers-best-practices`, `wrangler`, and `turnstile-spin`
- LoRA or QLoRA fine-tuning → `peft-lora-qlora`
- bitsandbytes quantization → `bitsandbytes-quantization`
- TRL training → `trl-training`
- Kaggle CLI work → `kaggle-cli`
- Google Colab sessions, runtimes, or `colab` CLI → `colab-operator`
- Hugging Face Hub, `hf` CLI, or Hugging Face ecosystem work → `hf-cli`
- scientific or publication figures → `scientific-visualization`
- sandboxed or untrusted code execution → `sandbox-sdk`
- Android AGP migration → `agp-9-upgrade`; native Android testing → `testing-setup`
- frontend design → `frontend-design`; scroll animation → `gsap-framer-scroll-animation`; web performance → `web-perf`
- repository docs → `doc`; conventional commits → `conventional-commit`; pull requests → `create-pr`; architecture boundaries → `architect`; codebase walkthroughs → `how`; Kaggle benchmarks → `write-kaggle-benchmarks`
- code quality review → `change-review`; whole-repository audit → `repo-audit`; blast-radius analysis → `blast-radius`; recurring mistake prevention → `correct`
- shortcut debt or deferred work → `shortcut-debt`
- design rationale, regressions, or postmortems → `why`
- continual learning, agent memory, skill updates, retention, or transfer → `continual-learning`
- stale prompts, outdated model assumptions, skill/rule cruft, or conflicting agent instructions → `prompt-audit`
- AI-sounding prose cleanup → `unslop`
- create or update a skill → `skill-creator`; install or discover skills → `skill-installer` or `find-skills`; plugin management → `plugin-management:plugin-management`
- Codex or OpenAI product behavior and configuration → `openai-docs`
- non-trivial engineering workflow → `poteto-mode`; broad multi-part work with no narrower owner → `figure-it-out`

## Selection rules

1. Choose one primary skill that owns the requested outcome.
2. Add a supporting skill only for a concrete required output.
3. For combined work, order skills as domain or artifact, implementation, then validation or review.
4. Read the selected `SKILL.md` before acting and follow its required tools, references, and validation.
5. Use only skills present in the active catalog and allowed by policy. Never invent a missing route or load a host-specific skill.
6. Treat review skills as alternatives unless the user asks for independent review passes.
7. Do not automatically route to `tdd`; use it only if an active policy explicitly permits it and the user asks for test-first, a failing test, or a regression test.
