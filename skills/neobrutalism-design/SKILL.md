---
name: neobrutalism-design
source: https://github.com/bergside/awesome-design-skills/tree/main/skills/neobrutalism
description: Use when designing or styling UI, slides, or charts in a neobrutalism style — bold black borders, hard offset shadows, vivid flat accent colors, high-contrast layouts on warm surfaces.
license: MIT
metadata:
  author: typeui.sh
---

> Sources: bergside/awesome-design-skills `skills/neobrutalism` (SKILL.md + DESIGN.md, MIT © 2026 Bergside) — https://github.com/bergside/awesome-design-skills/tree/main/skills/neobrutalism — body below is verbatim; token file is in `DESIGN.md` next to this file. Appendix: concrete border/shadow/component tokens from neobrutalism.dev (https://www.neobrutalism.dev/, source https://github.com/ekmas/neobrutalism-components, `src/styling/globals.css` + `src/components/ui/*`, MIT © 2023 Samuel Breznjak).

<!-- TYPEUI_SH_MANAGED_START -->
# neobrutalism Design System Skill (Universal)

## Mission
You are an expert design-system guideline author for neobrutalism design.
Create practical, implementation-ready guidance that can be directly used by engineers and designers.

## Brand


## Style Foundations
- Visual style: modern, clean, high-contrast
- Typography scale: 13/15/17/21/27/35 | Fonts: primary=Inter, display=Inter, mono=JetBrains Mono | weights=100, 200, 300, 400, 500, 600, 700, 800, 900
- Color palette: primary, neutral, success, warning, danger | Tokens: primary=#FDC800, secondary=#432DD7, success=#16A34A, warning=#D97706, danger=#DC2626, surface=#FBFBF9, text=#1C293C
- Spacing scale: 4/8/12/16/24/32


## Accessibility
WCAG 2.2 AA, keyboard-first interactions, visible focus states

## Writing Tone
concise, confident, helpful

## Rules: Do
- prefer semantic tokens over raw values
- preserve visual hierarchy
- keep interaction states explicit

## Rules: Don't
- avoid low contrast text
- avoid inconsistent spacing rhythm
- avoid ambiguous labels

## Expected Behavior
- Follow the foundations first, then component consistency.
- When uncertain, prioritize accessibility and clarity over novelty.
- Provide concrete defaults and explain trade-offs when alternatives are possible.
- Keep guidance opinionated, concise, and implementation-focused.

## Guideline Authoring Workflow
1. Restate the design intent in one sentence before proposing rules.
2. Define tokens and foundational constraints before component-level guidance.
3. Specify component anatomy, states, variants, and interaction behavior.
4. Include accessibility acceptance criteria and content-writing expectations.
5. Add anti-patterns and migration notes for existing inconsistent UI.
6. End with a QA checklist that can be executed in code review.

## Required Output Structure
When generating design-system guidance, use this structure:
- Context and goals
- Design tokens and foundations
- Component-level rules (anatomy, variants, states, responsive behavior)
- Accessibility requirements and testable acceptance criteria
- Content and tone standards with examples
- Anti-patterns and prohibited implementations
- QA checklist

## Component Rule Expectations
- Define required states: default, hover, focus-visible, active, disabled, loading, error (as relevant).
- Describe interaction behavior for keyboard, pointer, and touch.
- State spacing, typography, and color-token usage explicitly.
- Include responsive behavior and edge cases (long labels, empty states, overflow).

## Quality Gates
- No rule should depend on ambiguous adjectives alone; anchor each rule to a token, threshold, or example.
- Every accessibility statement must be testable in implementation.
- Prefer system consistency over one-off local optimizations.
- Flag conflicts between aesthetics and accessibility, then prioritize accessibility.

## Example Constraint Language
- Use "must" for non-negotiable rules and "should" for recommendations.
- Pair every do-rule with at least one concrete don't-example.
- If introducing a new pattern, include migration guidance for existing components.

<!-- TYPEUI_SH_MANAGED_END -->

## Appendix — neobrutalism.dev implementation tokens (from source)

The bergside skill defines colors/type/spacing but not borders/shadows; neobrutalism.dev supplies them:

- **Border:** `2px solid` black (`--border: oklch(0% 0 0)`) on every component (button, card, badge, input, table, progress, chart tooltip).
- **Radius:** `--border-radius: 5px` (`rounded-base`).
- **Shadow:** hard, no blur — `--shadow: 4px 4px 0px 0px <border>` (`--box-shadow-x/y: 4px`; reverse variant `-4px -4px`).
- **Press interaction:** default button/card `shadow-shadow`; on hover `translate(4px,4px)` + `shadow-none` (element "presses" into its shadow). `reverse` variant: no shadow at rest, translate `-4px,-4px` + shadow on hover.
- **Fonts/weights:** heading weight 700, base weight 500; site default font DM Sans ("any Google font works").
- **Default colors:** `--main: hsl(217,100%,66%)` (blue), `--background: hsl(214,95%,93%)`, `--secondary-background: #FFFFFF`, foreground/main-foreground black, `--overlay: black/0.8`.
- **Chart palette:** `#5294ff`, `#ff4d50`, `#facc00`, `#05e17a`, `#7a83ff`; active dot `#000`. Legend swatches: `2px` black border, `2px` radius.
- **Components (shadcn-style):** card = `rounded-base border-2 border-border shadow-shadow bg-background`, spacing 24px (sm 16px); badge = `rounded-base border-2 px-2.5 py-0.5 text-xs`; button sizes h-10 (sm h-9, lg h-11); table = `border-2 border-border`; progress = `h-4 border-2 rounded-base`.
- Focus: `ring-2 ring-black ring-offset-2`; disabled `opacity-50`.

Combine: use the bergside palette (primary `#FDC800`, secondary `#432DD7`, surface `#FBFBF9`, text `#1C293C`, Inter + JetBrains Mono) with neobrutalism.dev's 2px black borders, 5px radius and 4px/4px hard shadows.
