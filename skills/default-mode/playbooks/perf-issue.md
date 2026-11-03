### Performance issue

Own the measurement story. Do not infer a speedup from source inspection.

1. Capture a production-shaped baseline and vet it with `benchmark-checklist`.
2. Identify the limiter, then try the cheapest valid reduction first: remove, avoid repeat work, do less, defer, overlap, or make it cheaper.
3. Change one causal variable at a time and capture a post-change artifact.
4. Compare repeated, alternating runs and report the metric, range, limiter, and artifact path.
