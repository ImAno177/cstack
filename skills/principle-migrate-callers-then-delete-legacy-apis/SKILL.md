---
name: principle-migrate-callers-then-delete-legacy-apis
description: Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API
  in the same wave instead of preserving compatibility layers.
disable-model-invocation: true
---

# Migrate Callers Then Delete Legacy APIs

Replace an internal API in one wave: add the new one, move every caller, delete the old one. Do not leave both alive behind a compatibility layer.

**Why:** Two ways to do one thing double the surface to read and test, and the next contributor copies whichever example is nearest, often the old one.

**Pattern:**
- Find every caller before starting (`rg` for the symbol, plus string, config, and dynamic references).
- Migrate all callers and delete the old API in the same change, or in a stack that ends with the deletion. A deprecation shim with no removal step is the debt this principle prevents.
- Let the compiler or a failing import find the callers you missed; do not add an alias to silence them.
- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details.

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative

When external users do depend on the old API, keep it, version the change, and state the removal date.
