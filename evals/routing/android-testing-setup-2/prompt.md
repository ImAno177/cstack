---
tags: [routing, test]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

We're shipping a native Android banking app and QA keeps finding broken flows late. Set up an instrumented end-to-end test harness (Espresso or whatever fits) that runs on an emulator in CI, plus Robolectric for the fast tests.
