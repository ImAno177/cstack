---
name: bitsandbytes-quantization
description: Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memory
  is limited, need to fit larger models, or want faster inference. Supports INT8, NF4, FP4 formats, QLoRA training, and 8-bit
  optimizers. Works with HuggingFace Transformers. Not for CPU-only inference (GGUF) or production serving throughput (GPTQ/AWQ).
license: MIT
---

# bitsandbytes-quantization

Read [the full guide](references/full-guide.md) first: quick start, the three workflows (load, QLoRA, 8-bit optimizer), alternatives, and common issues.

Read a deeper reference only for its topic:

- [quantization-formats.md](references/quantization-formats.md) to choose between INT8, NF4, FP4 or set double quantization.
- [qlora-training.md](references/qlora-training.md) before fine-tuning with LoRA adapters or multi-GPU training.
- [memory-optimization.md](references/memory-optimization.md) after an out-of-memory error or to add offloading and gradient checkpointing.

Run `python -m bitsandbytes` first to confirm the install sees the GPU; `nvcc --version` shows the CUDA version to match.

## Done when

- The model loads with a `BitsAndBytesConfig` and generates text on a test prompt.
- Measured GPU memory (`torch.cuda.max_memory_allocated()`) is reported next to the FP16 estimate, with the quantization type used.

## If it fails

- Fix the CUDA/bitsandbytes mismatch from the install check before retrying a load.
- On OOM, change one thing per retry (smaller bits, offload, smaller batch) as the memory reference lists; stop and report if 4-bit with offload still does not fit.
