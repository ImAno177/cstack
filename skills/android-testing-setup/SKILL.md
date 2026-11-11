---
name: android-testing-setup
description: Analyze and create a testing strategy for native Android apps - install testing libraries, set up test infrastructure,
  create harnesses for unit tests, UI tests, screenshot tests, and end-to-end tests.
license: Complete terms in LICENSE.txt
metadata:
  author: Google LLC
  last-updated: '2026-08-06'
  keywords:
  - android
  - testing
  - ui tests
  - screenshot tests
  - coverage
---

## Step 1: analyze the current testing setup

To understand the testing setup of an existing project, look for these dependencies in the libs.versions.toml file, or build files:

1. Dependency Injection framework used. Examples: Hilt, Koin, Anvil, vanilla Dagger...
2. Unit (local) testing framework this project uses, Example JUnit4, JUnit5...
3. Mocking framework (if any) used for unit tests, and for Instrumented and UI tests. Examples: Mockito, Mockk...
4. Robolectric. It can be used in 3 ways:
   1. Used in unit tests to have fakes for platform entities
   2. To run behavior UI tests without a device or emulator. For example, used to run Espresso or Compose tests.
   3. To do screenshot testing with Roborazzi
5. Is the app 100% Compose, Views or hybrid?
6. Behavior UI tests:
   1. Compose Tests (`androidx.compose.ui:ui-test-*`)
   2. Espresso Tests for Views. Might use wrappers like Kaspresso. Dependencies: `androidx.test.espresso:espresso-core`, `androidx.test:runner`, `androidx.test:rules`.
7. Screenshot tests can be:
   1. Instrumented (device-based). For example, using Dropshots.
   2. Based on Robolectric, so they run locally. For example, using Roborazzi.
   3. Based on LayoutLib, so they run locally. For example, Paparazzi, or the Compose Preview Screenshot Testing tool.
8. End to end tests (Release Candidate tests) run on device with UIAutomator, Appium, or Robotium.
9. Generate a Markdown report with the analysis

## Step 2: Set up Dependency Injection frameworks for testing

Install a Dependency Injection framework when the project has none: ask the user to choose Koin or kotlin-inject for a multiplatform app, and install Hilt otherwise.

Install the testing dependencies (for example `com.google.dagger:hilt-compiler` that should be applied with a `kspAndroidTest` configuration).

> [!IMPORTANT]
> Consult the documentation of the applicable framework to learn about testing (for example: [Hilt testing guide](references/android/training/dependency-injection/hilt-testing.md), [Koin Instrumented tests](https://insert-koin.io/docs/reference/koin-android/instrumented-testing)).

For instrumented tests, create and configure (by adding `testInstrumentationRunner` to the build gradle files) a new test runner and apply the testing rules required by the framework (for example in Hilt, annotate your test classes with `@HiltAndroidTest` and apply the `HiltAndroidRule`). Other frameworks use other mechanisms, consult their documentation.

## Step 3: Install frameworks

Unless otherwise specified, respect the current stack of testing frameworks.

Install the following when the project has no testing frameworks and the user stated no preference:

- JUnit4 for local and instrumented tests
- Jacoco for test coverage
- For UI tests: if the project has views, Espresso. If it's fully Compose, use the Compose Testing APIs.
- Robolectric to run UI Tests
- Compose Preview Screenshot Testing tool for screenshot tests - check [setup documentation](references/android/studio/preview/compose-screenshot-testing.md) and follow it strictly.
- Dropshots for device screenshot tests
- If a mocking framework is necessary, install Mockk (`io.mockk:mockk`). Do not install it unless it is clearly necessary.

Install Dropshots when instrumented screenshot tests are requested, and UI Automator when end-to-end testing is requested.

## Step 4: Refactor and create fakes for testing

### **Refactor for unit tests**

For dependencies on Android framework classes or entities outside the codebase:

- First, use a fake. If it doesn't exist, create an interface for the class and a "Default" implementation with the existing code. Add the Fake version to the test sourceset (test or androidTest).

- Mock the dependency when a fake is impossible (example: no access to the class or interface).

### **Refactor for UI tests**

Replace slow and problematic dependencies with runtime fakes through the installed Dependency Injection framework to:

- **Simulate** different scenarios with the user (wrong credentials, reset password flow...), with a server (no connection, server down, bad JSON from server...) or with a platform component (insufficient permissions, no disk space, no front camera available)
- **Improve** speed and reliability (replacing a database with an in-memory database, replacing a repository with an in-memory fake to avoid hitting the network)

## Step 5: Unit testing

Add or review unit tests in every file with business logic (ViewModels, Repositories, DAOs). Skip Activities, Compose layouts, and dependency injection configuration.

## Step 6: UI testing

Put Espresso or Compose UI tests in the `test` sourceset (Robolectric), and in `androidTest` when instrumented tests are requested.

## Step 7: Test databases

Create instrumented tests with an in-memory database for any SQLite database (Room, SQLDelight, etc.) to confirm they work with the SQLite engine on device.

## Step 8: Screenshot tests

Irrespective of the framework used, screenshot tests focus on 2 types of tests:

- Screen-level screenshot tests, where each screen is tested in 9 different sizes, combining compact, medium and expanded widths (400, 610, 900 dp) and heights (400, 500 and 1000 dp).
- Screen-level variations. Add a mobile (400x500) screenshot of:
  - All the alternative themes, if used.
  - Font scale set to 1.5.
- Component-level screenshot tests, where each component is tested in different themes and font scales.

Do not test behavior with screenshots, but cover common scenarios whose UI changes a lot with state (for example, inject a loading state or simulate it with a fake).

## Step 9: UI Behavior tests

Test that the UI reacts as expected to different states and user actions.

### **Compose UI behavior tests**

- Use the ComposeTestRule with a `ComponentActivity` to access resources such as strings.
- Always try to match with semantic matchers first. If the matcher is too complicated to write (using more than 3 matchers to find a single element), use `testTag`.
- Always verify state restoration

### **Views (XML) UI behavior tests**

Use Espresso to match and interact with views.

## Step 10: Navigation tests

Create a suite covering back handling, deeplinks, and patterns like "exit through home" with multiple backstacks.

## Step 11: Simulate different window sizes and settings

Use `DeviceConfigurationOverride` described in "[UI testing common patterns](references/android/develop/ui/compose/testing/common-patterns.md)" to simulate different window sizes, font scales

## Step 12: End-to-end tests

Create a low number (about 5% of all tests) of end-to-end tests that cover big user journeys. Use Compose Test APIs or Espresso for that. If you have to access platform features (notifications, system UI...), use UI Automator.

If you need to take screenshots of the app running in a device, use [Dropshots](https://raw.githubusercontent.com/dropbox/dropshots/refs/heads/main/README.md). You need a device for screenshot tests when verifying interaction with the system UI (examples: edge-to-edge rendering, notifications, picture-in-picture)

### Step 13: Instrumented Screenshot tests

Install the `com.dropbox.dropshots` plugin in the module and a `Dropshots()` JUnit Rule. Create an instrumented screenshot test for one feature.

### Step 14: Install jacoco

Add the `jacoco` plugin to each module that contains tests.

## Final touches

- Ask whether to document the analysis findings and the changes applied to the testing strategy. On agreement:
  - Update AGENTS.md or CLAUDE.md with the testing-strategy changes when one exists.
  - Otherwise create docs/testing.md (strategy, commands to run every type of test, screenshot reference file locations), plus a root AGENTS.md (CLAUDE.md on Claude Code) linking to it.

## Not for

- Feature tests in an already-configured project (`tdd`) or web UI testing (`webapp-testing`).

## Done when

- `./gradlew test` passes (plus `./gradlew connectedAndroidTest` when instrumented tests were added; it needs a device or emulator) after the last dependency or runner change, and the Step 1 report lists the detected stack and added libraries.

## If it fails

- Read the first Gradle error; check dependency version, configuration (`kspAndroidTest`, `testInstrumentationRunner`), and sourceset (`test` vs `androidTest`). Fix that cause and rerun the same task.
- Report blocked after two different fixes fail, naming the missing device or credential.
