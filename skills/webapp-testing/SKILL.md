---
name: webapp-testing
description: Test a web application end to end in a real browser with Playwright - start the app, drive user flows, check the result, and capture screenshots, console errors, and network failures as evidence. Use for QA of a web UI, reproducing a browser bug, writing or fixing Playwright tests, or verifying a frontend change actually works.
license: MIT
---

# Web app testing

A frontend change is not verified until a browser has run the flow and you have looked at the result. Passing unit tests and a clean build do not show that a page works.

## Set up

1. Find how the app runs: the dev server command, port, and required environment from `package.json`, the README, or the framework config. Start it in the background, wait until the URL answers, and stop it when you finish.
2. Use the project's existing Playwright setup if it has one (`playwright.config.*`, `tests/e2e/`). Otherwise use a scratch script outside the repository: `npm i -D @playwright/test` in a scratch directory, then `npx playwright install chromium`. Add Playwright to the project only when the user wants permanent tests.
3. If the host gives you a browser tool or a Playwright MCP server, you may use it for exploration. Record the final checks as a script so they can be rerun.

## Drive the flows

- Write down each flow as steps and an expected outcome before you start, such as "sign in, add an item, the cart badge shows 1".
- Find elements as a user would: `getByRole`, `getByLabel`, `getByText`. Use test IDs only when the project already uses them. Avoid CSS paths tied to layout.
- Wait for conditions, never for fixed times: `await expect(locator).toBeVisible()`, `page.waitForURL`, `page.waitForResponse`.
- Assert what the user sees and what the system stored: the visible text, the URL, and the API response or database row when it matters.
- Cover the unhappy paths: validation errors, empty states, slow or failing requests (use `page.route` to simulate them), and the narrow mobile viewport.

## Collect evidence

- Attach listeners for `console` errors, `pageerror`, and failed or 4xx/5xx responses. Any of them fails the run unless you can explain it.
- Take a screenshot at each checkpoint and look at it. A test that passes while the page shows an error banner or broken layout has not passed.
- On failure, keep the trace (`trace: 'retain-on-failure'`) and quote the first real error, not the last timeout.

## Hand back

The flows tested and their results, the commands to rerun them, screenshots of the key states, console and network errors found, and the flows you did not test. Use `create-verification-skill` to turn these flows into a repeatable project harness, `web-perf` for load performance, and `frontend-design` for visual design quality.
