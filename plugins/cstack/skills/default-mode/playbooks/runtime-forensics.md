### Runtime forensics

Diagnose an active runtime symptom from captured evidence, not from code inspection alone. Diagnosis is read-only unless the user separately authorizes a fix.

1. Name the symptom and capture method: CPU profile for a spin, allocation or heap snapshot for a leak, scheduler or network trace for a stall, or a UI trace for jank. Use tools supported by this host and target; do not install instruments or change production traffic without authority.
2. Capture the shortest representative failing interval and record version, workload, time window, and environmental effects. Do not collect credentials or unrelated user data.
3. Reduce large data off the main context; identify the hot path, retention chain, or blocked thread. Map it to a real file, function, and source revision.
4. Try a minimally invasive confirmation against the same surface when safe. If no repeatable confirmation exists, label the cause a hypothesis.
5. Preserve an evidence pointer and hand the diagnosis to bug-fix, perf-issue, or hillclimb only when implementation is requested.

**Reply:** symptom, capture path, suspected mechanism, supporting frames and source location, confirmation level, and next experiment.
