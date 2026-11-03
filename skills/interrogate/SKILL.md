---
name: interrogate
description: Run an adversarial review of a change or design where every surviving finding must be proven by a repro, failing check, or direct artifact evidence. Use for blind-spot and stress-test requests.
---

# Interrogate

1. State the intended behavior, scope, and evidence that would prove a break.
2. Fan out independent adversaries with isolated scratch space and the same scope. Each tries to break the intent across behavior, boundaries, scale, cleanup, and integration.
3. Require every finding to include the exact command or observation, the output, and the expected output. Unrun concerns are not findings.
4. Re-run each candidate finding from the main workspace. Keep only failures that break the stated intent and merge findings with one root cause.
5. Report verified findings, dropped findings, gaps, and commands. Do not apply fixes in this skill; route accepted fixes to the owning implementation skill.
