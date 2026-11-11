---
name: web-perf
description: Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary
  metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching
  issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores,
  or site speed. Biases towards retrieval from current documentation over pre-trained knowledge.
---

# web-perf

Read [the full guide](references/full-guide.md) when this skill applies.

This skill needs the `chrome-devtools` MCP server, which cstack does not bundle. On Claude Code, the user adds it with `claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest` and restarts the session. If the user cannot add it, measure lab metrics with `npx -y lighthouse <url> --output=json --output-path=./lighthouse.json --chrome-flags="--headless"` and say that trace-level findings (dependency chains, layout-shift culprits) were not available.
