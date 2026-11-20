### Trace forensics

Diagnose from an existing fixed artifact such as a CPU profile, heap snapshot, trace, crash dump, or spindump. Do not rerun the system merely because you have a capture.

1. Identify format, provenance, build revision, time window, and whether the capture is complete. Treat private logs and tokens as sensitive.
2. Parse large traces into a queryable form, such as indexed rows in SQLite for samples, stacks, or events. Read aggregates and focused ranges, not the entire raw payload into context.
3. Follow the dominant frames, blocked threads, allocation sites, or retainer paths to the suspected mechanism. Distinguish correlation from an explanation of the symptom.
4. Map the finding to the exact source symbol and line for that build. If symbols or provenance are missing, say diagnosis is incomplete.
5. Compare a paired baseline when available. Without one or a controlled check, report a plausible cause rather than a confirmed fix. Do not modify product code on a read-only diagnosis.

**Reply:** artifact and query, cause and source pointer, evidence, confidence, whether paired comparison confirmed it, and any missing data.
