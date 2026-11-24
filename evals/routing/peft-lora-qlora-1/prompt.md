---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

I need to fine-tune Llama 3 70B on a single 48GB GPU for our customer support data. Set up QLoRA with PEFT: target modules, rank, alpha, and the training config.
