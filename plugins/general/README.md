# General

General is a standalone skills plugin for ChatGPT, Codex, Grok Bot, and compatible agent hosts.

It includes a concise engineering mode, academic research skills, and a continual-learning skill for evidence-backed maintenance of reusable agent guidance. The package is built only from `source/general`; it does not synchronize from external repositories.

Codex uses the lifecycle hook to load General context at session start. Grok Build runs the same hook in its passive session-start mode without relying on stdout injection. Grok Bot uses the portable skills and does not depend on a lifecycle hook. The hook does not write memory, modify skills, or claim that a hook execution is learning.
