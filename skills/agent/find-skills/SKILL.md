---
name: find-skills
description: Find or install an existing skill when the user asks for a capability, tool, template, or workflow.
---

# Find skills

Use this skill when the user asks whether a skill exists, wants a skill for a task, or wants to extend an agent.

## Workflow

1. Restate the capability in concrete terms.
2. Search the installed catalog first.
3. Search the public skills catalog only when the local catalog has no clear match.
4. Compare each candidate's description, host support, source, license, and maintenance status.
5. Recommend the smallest matching skill and explain one close trade-off.
6. Install only when the user asks. Use the approved installer and verify the installed path.

Do not create a new skill when an existing one owns the task. Do not claim a skill exists without checking its source or installed catalog.

For each candidate, give its name, source, supported host, purpose, and why it matches. If no candidate fits, state what is missing and recommend the smallest new skill scope.
