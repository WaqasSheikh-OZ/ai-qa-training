# Week 3 Assignment – Data-Driven UI Testing and API Validation in Existing Playwright Python Framework

## 1. Your Role

Act as a Senior QA Automation Architect, Senior SDET, and expert Playwright Python automation engineer.

I am working on an existing Playwright Python automation framework.

I have completed Assignment 2, reviewed the AI-generated implementation, corrected it, and organized it using a structured framework architecture.

Now I want to implement Week 3 Assignment 3 within the SAME framework.

Your task is to implement the Week 3 requirements without abandoning or unnecessarily changing my existing architecture.

**Important: I do not want a standalone implementation of the instructor's sample scripts. I want the same learning objectives implemented using my existing framework architecture and coding conventions.**

The actual website, its DOM, actual API responses, and assignment requirements are the sources of truth.

Never invent application behavior or technical details.

## 2. First Inspect the Existing Project

Before making any modifications, inspect the existing repository.

Pay particular attention to:

- `conftest.py`
- `pages/`\*
- `components/`
- Existing fixtures
- Existing browser and page initialization
- Base URL and environment configuration
- Existing Week 2 tests
- `tests/week2/test_cases.csv`
- Existing helper modules
- `pytest.ini` or equivalent configuration
- Existing API-related utilities, if any
- `.github/copilot-instructions.md`, if present

Inspect the actual repository structure rather than assuming every file exists at the paths mentioned above.

Understand how:

1. The browser is initialized.
2. The Playwright page is created.
3. Page objects are instantiated.
4. Components are accessed through fixtures or page objects.
5. Test data is currently managed.
6. Tests are executed.

Preserve the existing synchronous Playwright Python implementation.

Do not introduce asynchronous Playwright.

Do not create duplicate fixtures or utilities if equivalent functionality already exists.

## 3. Understand Week 3 Assignment Requirements

The assignment has two main testing requirements.

### A. Data-driven UI testing

Select one existing Week 2 test that accepts product or product quantity as an input value.&#x20;

Create a CSV-driven test implementation.

The assignment requires a `data.csv` file containing the input values and expected outcomes.

Use pytest parametrization so that each CSV row executes as an independent test case.

Use:

`@pytest.mark.parametrize`

The test should execute each row independently.

The CSV should contain meaningful columns appropriate to the selected feature.

### B. API testing

API base url: https\://[api.practicesoftwaretesting.com](https://api.practicesoftwaretesting.com/products)

endpoint: [/products](https://api.practicesoftwaretesting.com/products)

Implement one separate API test that:

1. Sends a GET request to an actual public practice-site API endpoint.
2. Validates the HTTP status code.
3. Validates at least three actual response fields.
4. Validates the appropriate data types.
5. Compares at least one API response value with the corresponding value displayed in the website UI.

These two testing requirements must be implemented in the existing framework architecture and you should enhance the framework for adding API module as per enterprise grade framework style. however, keep the scope limited to the assignments work only.

&#x20;For example, for adding api module, you should be adding only the required endpoints, clients and stuff. do not go for full scope api testing module implementation for the website under test

### 4. API architecture

Keep API testing separate from page-object responsibilities.

If the framework already contains an API client or API fixture, reuse it.

Otherwise, determine the appropriate location for a small reusable API utility or fixture.

Use Playwright's synchronous API request capabilities or an existing compatible HTTP utility.

Do not introduce an unnecessary API framework or additional dependencies.

The API test and UI test should remain independently understandable.

The API/UI comparison should happen at the test level, using the relevant page object to read the displayed UI value.

### 5. Important requirements

- Read test data from CSV.
- Assignment 3 test cases should be placed in tests/week3 folder. do not modify the week1 and week2 tests
- Each CSV row must produce an independent pytest test result.
- Ensure pytest displays individual test cases using `pytest -v`.
- Use readable parametrized test IDs.
- Handle empty values correctly.
- Handle invalid inputs according to actual observed application behavior.
- Avoid hardcoding the CSV contents inside the test function.
- Do not use `time.sleep()`.

### 6. Framework integration

Use the existing framework architecture. Adding any architectural thing must have solid reason and enterprise grade implementation. If a required method is missing from an existing component, implement it in the correct architectural location.

Do not rewrite working functionality.

## 7. Suggested Project Organization

Use the existing project structure and adapt the following organization only where appropriate.

The intended logical organization is:

- Existing `pages/` for page objects.
- Existing `components/` for reusable UI components.
- Existing shared fixtures and utilities.
- `tests/week3/` for Week 3 executable tests.
- A `week3/` assignment folder for:
  - `data.csv`
  - `prompt.md`
  - `notes.md`

Keep executable tests separate from assignment documentation and data where appropriate.

Do not create duplicate copies of the same CSV file.

Do not change the existing Week 2 implementation unnecessarily.

## 8. Required Initial Deliverables

Prepare the following:

### A. Data-driven UI test

One parametrized UI test using the selected Week 2 feature and CSV test data.

### B. API test

One separate API test that checks:

- HTTP status.
- At least three actual response fields and their types.
- At least one API/UI value comparison.

### C. data.csv

At least six test rows, including one unacceptable input.

Clearly distinguish manually verified expected results from proposed/unverified results.

### D. notes.md

Create a notes file
