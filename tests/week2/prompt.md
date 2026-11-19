# Week 2 automation prompt

Implement automated tests for the shop using `tests\week2\test_cases.csv` as
the source of requirements. Start with the selected cases TC-01, TC-03, TC-06,
TC-08, TC-09, TC-11, TC-17 and TC-18; together they cover search, sorting,
cart and contact. Select additional cases from the CSV when practical, and
identify the automated case IDs in the test names or report.

- Never presses Send on a filled-in contact form. It sends a real message
- Only press Send when at least one required field is empty; never submit a
  completed form, including through Enter, JavaScript or an API. For contact
  retention, fill all five fields and inspect them without submitting.
- Create test files only in `tests\week2`. Do not look for existing test files
  in any other folder. Use `test_*_week2.py` names to avoid pytest module-name
  collisions; same-named files in separate folders are acceptable only if
  collection permits them.
- Follow the existing Python, pytest, synchronous Playwright and Page Object
  Model patterns, coding standards and fixtures. Read the framework
  documentation, configuration, page objects and components as needed, but
  not other folders' test files. Reuse shared navigation and helpers; extend
  page objects or components only where needed, preserving existing behavior.
- Keep each test isolated, use stable semantic or test-id locators, Playwright
  auto-waiting assertions and explicit expected outcomes. Avoid hard sleeps,
  brittle selectors, silent failures and assumptions about unspecified stock
  messages or eco discount rates. Do not cover login, checkout, payment or
  order history.
- Run the week 2 tests from the project root and report selected case IDs,
  results, failures and any blocked cases without masking defects. Treat an
  applicable eco discount as intentional while checking the line price.
- You should only run the first draft and report the failures. Do not try to fix any failures. 
