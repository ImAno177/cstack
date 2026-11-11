---
name: peft-lora-qlora
description: Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models
  (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter
  serving. HuggingFace's official library integrated with transformers ecosystem.
license: MIT
---

# peft-lora-qlora

Read [the full guide](references/full-guide.md) before writing any PEFT code. It covers LoRA parameter selection, QLoRA setup, loading and merging adapters, and integration patterns.

- Read [advanced-usage](references/advanced-usage.md) before using DoRA or another non-default variant, or multi-adapter serving.
- Read [troubleshooting](references/troubleshooting.md) as soon as an install, CUDA, out-of-memory, or adapter-loading error appears.

## Not for

- Full fine-tuning of small models (<1B parameters) or work that needs maximum quality at any compute cost.

## Done when

- The training script runs at least one step on the target GPU and saves an adapter.
- The saved adapter reloads and generates; for a merged model, the merged output matches the adapter's output on one fixed prompt.

## If it fails

Look up the exact error text in troubleshooting before changing code. Change one thing (rank, target modules, batch size, quantization) per retry. After three failed retries, report the error and the environment (GPU, library versions) instead of continuing to tune.
