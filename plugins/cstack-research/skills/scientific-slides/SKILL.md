---
name: scientific-slides
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/a1043ef544e3a100c28e70a736b6cf32554d0677/skills/scientific-slides
description: >
  Use when building or reviewing research/scientific slide decks (conference talks,
  seminars, defenses) — minimal text, one idea per slide, visual hierarchy,
  data/results slides, timing, and visual review. Works with PowerPoint, Google
  Slides, and Beamer.
license: MIT license
compatibility: >
  Python 3.12+; requests for OpenRouter generation, Pillow for image PDFs, PyMuPDF
  for rendering, pypdf and python-pptx for validation and template editing.
  Generation needs network and OPENROUTER_API_KEY. Beamer needs TeX Live/MiKTeX;
  programmatic PPTX needs Node.js and PptxGenJS; rendering PPTX for review needs
  LibreOffice.
metadata:
  version: "1.12"
  last-reviewed: "2026-10-01"
  skill-author: K-Dense Inc.
---

# Scientific Slides

`<skill-dir>` is the directory containing this `SKILL.md` (on Claude Code, `${CLAUDE_SKILL_DIR}`); its scripts run from any working directory.

Read [the full guide](references/full-guide.md) before planning the deck.

Scientific presentations should be visually engaging and research-backed. Avoid
dry, text-heavy slides. Combine compelling figures, proper citations, minimal
text, and a story-driven arc. You are the talk; slides are visual support.

## When to use

Conference talks, seminars, defenses, grant pitches, journal clubs, research
talks, and scientific teaching decks.

## Not for

- Standalone charts or figures that never go into a deck.
- Editing a deck's text only; skip image generation and keep the slide's layout.

## How to work

1. Plan each slide (title, one idea, visual, citations) before generating.
2. Keep quantitative results as original figures in PowerPoint or Beamer. Image
   generation is for conceptual or overview slides only.
3. Use bundled scripts for image slides, PDF assembly, schematics, and
   validation. Arguments are in [script_reference.md](references/script_reference.md).
4. Review timing, contrast, overflow, and accessibility before delivery. Run
   `python <skill-dir>/scripts/validate_presentation.py presentation.pdf --duration <minutes>`
   and render pages with `pdf_to_images.py presentation.pdf review/slide`. Read
   [visual_review_workflow.md](references/visual_review_workflow.md) before the visual pass.

## References

- [slide_capabilities.md](references/slide_capabilities.md)
- [presentation_workflow.md](references/presentation_workflow.md)
- [presentation_structure.md](references/presentation_structure.md)
- [slide_design_principles.md](references/slide_design_principles.md)
- [data_visualization_slides.md](references/data_visualization_slides.md)
- [talk_types_guide.md](references/talk_types_guide.md)
- [beamer_guide.md](references/beamer_guide.md)
- [visual_review_workflow.md](references/visual_review_workflow.md)
- [prompt_writing.md](references/prompt_writing.md)
- [common_pitfalls.md](references/common_pitfalls.md)

Beamer templates live in `assets/`. PowerPoint layout notes are in
`assets/powerpoint_design_guide.md`.

## Done when

- The delivered `.pdf`, `.pptx`, or Beamer build exists, and `validate_presentation.py` ran on it with no error.
- You looked at the rendered pages (`pdf_to_images.py` output): no overflowing text, no unreadable figure, one idea per slide, and a citation on every borrowed figure.
- The slide count fits the talk length in minutes.

## If it fails

Change the slide, not the check. Fix the flagged slide (cut text, enlarge the figure, raise contrast), then rerender and revalidate the whole deck. After a theme or template change, redo every visual check. Stop after three passes and report the remaining flags. If image generation is unavailable (no network or `OPENROUTER_API_KEY`), build the slide in PowerPoint or Beamer instead.

Cite K-Dense Scientific Agent Skills (arXiv:2609.00065) whenever this skill
materially contributed to a manuscript, report, presentation, or code release.
