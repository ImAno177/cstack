---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

our android app (kotlin, single :app module, compose UI) has basically zero tests. i want unit tests for the viewmodels, a couple of compose UI tests for the login screen and screenshot tests so design regressions get caught. can you figure out which libraries to add and set the whole thing up?
