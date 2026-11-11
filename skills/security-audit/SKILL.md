---
name: security-audit
description: Security review of a repository or change - threat model, secrets, dependencies, authentication and authorization, injection, and unsafe data handling - where every finding comes with proof and a fix. Use for "security audit", "is this safe", threat modeling, pre-release security checks, or reviewing auth, input handling, or secrets.
license: MIT
---

# Security audit

Find the ways an attacker or a mistake turns this code into harm, and prove each one. Report-only unless the user asks for fixes. Audit only systems the user owns or is authorized to test, and never exploit anything beyond a local proof.

## Threat model first

1. Name the assets: credentials, user data, money, compute, availability, and the integrity of what the system publishes.
2. Name the entry points: HTTP routes, webhooks, queues, CLI arguments, file uploads, environment variables, CI workflows, and plugin or prompt inputs read by an agent.
3. Name the trust boundaries: where data from users, other services, or the network becomes trusted, and who can reach each entry point unauthenticated, as a user, or as an admin.

Spend the audit on the paths that cross a boundary toward an asset. A long generic checklist is not a threat model.

## Checks

- **Secrets.** Search the tree and history for keys, tokens, and private keys (gitleaks or trufflehog if available, otherwise targeted `git log -p` searches). Check `.env` handling, CI logs, error messages, and client bundles. A secret that ever reached a remote counts as leaked: rotate it, do not just delete the line.
- **Dependencies.** Run the ecosystem's audit (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `osv-scanner`). Report only advisories whose vulnerable code is reachable or whose package is exposed, and check for unpinned, typo-squatted, or install-script dependencies.
- **Authentication and authorization.** For each sensitive action, find where identity is checked and where permission is checked. Look for missing object-level checks (IDOR), client-side-only checks, privilege changes without re-authentication, and weak session or token handling.
- **Injection and unsafe input.** Trace untrusted input to SQL, shell, templates, file paths, deserializers, redirects, outbound requests (SSRF), and HTML output (XSS). Check for prompt injection where untrusted text reaches an agent that holds tools or secrets.
- **Data handling.** Check crypto choices, password hashing, transport security, logging of personal data, retention, and backups.
- **Configuration and CI.** Check debug modes, CORS, security headers, default credentials, workflow permissions, `pull_request_target` use, and third-party actions pinned by tag instead of SHA.

## Proof

Each finding needs evidence: the `file:line` of the flaw, the path from the entry point to it, and a local reproduction (a failing test, a request against a local instance, or a script) when that is cheap and safe. Rate it by how reachable and how damaging it is, not by category name. Put suspected issues you could not confirm in a separate list.

## Hand back

1. The threat model in a few lines.
2. Findings ranked by severity, each with evidence, impact, and a concrete fix.
3. Unconfirmed suspicions and what would confirm them.
4. What you checked and found clean, and what you could not check.

Do not paste live secrets into the report. Name the location and say it must be rotated.
