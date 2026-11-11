---
name: webapp-testing
description: "Host-neutral browser QA that proves a web app works the way a user would: start the app, drive flows in a real browser with Playwright using role and label locators, assert what the user sees and what the system stored, and keep screenshots, console errors, and failed requests as rerunnable evidence. Use for QA of a web UI, reproducing a browser bug, writing or fixing Playwright tests, or verifying a frontend change. Not for a reusable project harness; use create-verification-skill."
license: MIT
---

# Web app testing

A frontend change is not verified until a browser has run the flow and you have looked at the result. Passing unit tests and a clean build do not show that a page works.

## Set up

1. Find how the app runs: the dev server command, port, and required environment from `package.json`, the README, or the framework config. Start it in the background, wait until the URL answers, and stop it when you finish.
2. Use the project's existing Playwright setup (`playwright.config.*`, `tests/e2e/`) when present. Otherwise use a scratch script outside the repository: `npm i -D @playwright/test` in a scratch directory, then `npx playwright install chromium`. Add Playwright to the project only when the user wants permanent tests.
3. Use the host's browser tool or Playwright MCP server for exploration when available. Record the final checks as a script that reruns with `npx playwright test`.

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

## Not for

- Unit or API-only tests with no browser: use the project's test runner or `tdd`.
- Load performance (`web-perf`) or visual design quality (`frontend-design`).

## Hand back

The flows tested and their results, the commands to rerun them, screenshots of the key states, console and network errors found, and the flows you did not test. Use `create-verification-skill` to turn these flows into a repeatable project harness.

## Done when

- The rerun command passes on a fresh app start, and the screenshots of the key states were looked at.
- No unexplained console, page, or 4xx/5xx errors remain, and untested flows are listed.

## If it fails

Quote the first real error from the trace, fix the app or the locator, and rerun the whole flow. Stop and report after two reruns with no new evidence. Never loosen an assertion to get a pass.

## Example

```
Flows: sign in, add item (pass); empty cart, 500 on checkout (pass).
Rerun: npx playwright test tests/e2e/cart.spec.ts
Screenshots: <dir>/cart-badge.png, <dir>/checkout-error.png
Errors: none unexplained. Not tested: password reset (out of scope).
```
