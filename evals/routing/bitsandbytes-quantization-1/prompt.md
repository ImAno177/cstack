---
tags: [routing, train]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
plugins: ["../../../plugins/cstack", "../../../plugins/cstack-harness", "../../../plugins/cstack-research"]
---

Our 13B model doesn't fit in GPU memory for inference. Quantize it to 4-bit NF4 with bitsandbytes and check how much accuracy we lose.
