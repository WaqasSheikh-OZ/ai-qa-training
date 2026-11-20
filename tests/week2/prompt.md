# Task: Inspect the Actual Website DOM and Correct the Playwright Python Framework Architecture and Assignment 2 Implementation

## 1. Your Role

Act as a Senior QA Automation Architect and Senior Playwright Python Automation Engineer.

You are working on an existing Playwright Python automation framework. Your responsibility is to understand the existing framework, inspect the actual application under test (AUT), identify architectural and implementation mistakes, and implement the required Assignment 2 functionality correctly.

Do not make assumptions about the application's DOM, selectors, HTML attributes, API endpoints, component hierarchy, or behavior.

**The actual running website and its DOM are the source of truth.**

The screenshot attached to this task is a visual reference, not a replacement for DOM inspection.

## 2. First Understand the Existing Framework

Before modifying any code:

1. Inspect the entire existing project structure.
2. Read the existing:
   - `conftest.py`
   - `base_page.py`
   - Existing page objects
   - Existing components
   - Fixtures
   - Configuration files
   - Existing tests for Assignment 2 in week2/test_cases.csv
   - `pytest.ini` or equivalent configuration
   - Any existing framework documentation or Copilot instructions.
3. Understand how the browser, page, base URL, and page objects are initialized.
4. Identify the existing architectural conventions and naming patterns.
5. Understand how components are currently instantiated and exposed to tests.

Do not unnecessarily restructure working framework code.

Do not introduce a second implementation of functionality that already exists.

Preserve the existing Playwright Python synchronous API and do not go for asynchronous implementation.&#x20;

## 3. Inspect the Actual Application and DOM

Use the browser automation tools already available in this VS Code/Copilot environment.

Use the configured application base URL from the existing project configuration. Do not invent a URL.

If the browser automation capability is unavailable, clearly report that limitation instead of pretending to have inspected the website.

Open the actual application and perform the following investigation.

### A. Global Header

Inspect the header visible at the top of the supplied screenshot.

It contains elements such as:

- Home
- Categories dropdown
- Contact
- Sign in
- Language selector
- Other navigation elements, if present.

Investigate:

1. Actual HTML structure.
2. Whether the header is present across different page types.
3. Actual accessible roles, names, labels, attributes, and links.
4. How the Categories dropdown opens.
5. How individual categories are represented.
6. What happens when a category is selected.

The existing `HeaderComponent` is already implemented and working through a fixture in `conftest.py`.

Preserve this implementation unless actual DOM inspection demonstrates a concrete defect.

### B. Product Listing Page

Navigate to the Home page and select different product categories through the actual Categories dropdown.

Inspect the resulting product listing pages.

Identify:

- Product listing container.
- Individual product cards.
- Product names.
- Product images.
- Product prices.
- Product detail links.
- Pagination, if present.
- Empty-state messages, if present.
- Any category-specific page title or heading.

Verify whether different categories use the same DOM structure or different structures.

The existing `ProductsPage` should remain responsible for page-level product listing functionality.

### C. Left Sidebar: Critical Investigation

This is the most important part of this task.

The supplied screenshot shows a left-hand sidebar containing:

1. Sort
   - Sorting dropdown.
2. Price Range
   - Minimum and maximum price controls.
3. Search
   - Search input.
   - Reset/clear button.
   - Search button.
4. Filters
   - Product category checkboxes.
   - Other filters, if present.

Do not implement these controls directly inside `ProductsPage` without first investigating their actual DOM and architectural responsibility.

Inspect the sidebar in detail.

For assignment 2, only sort and search controls need to be implemented. Do not implement all the DOM of website. only necessary parts should be implemented but the implementation should be performed on correct places. For example, the sidebar seems to be implemented in a product_list_compoment. but this is a suggestion, you must have to observe it yourself as a senior architect and SDET and then decide the correct way of implementing it.

For each control that need to be implemented (search and sort), establish:

- Actual HTML element and hierarchy.
- Parent container.
- Actual labels and accessible names.
- Input types.
- Available dropdown options.
- Actual attributes and IDs.
- Whether controls are native HTML elements or custom widgets.
- Whether the sidebar is present on all pages or only product listing pages.
- Whether it is shared between different category listing pages.
- Whether interaction changes the URL, page content, or both.

Also inspect the behavior of each control by actually interacting with it.

For example:

**Search**

- Enter a search term.
- Click Search.
- Observe the resulting product listing.
- Test the reset/clear functionality.
- Check whether Enter also triggers the search.

**Sorting**

- Inspect all available sorting options.
- Select different options.
- Observe how product ordering changes.



Do not assume these interactions trigger particular API endpoints.

Do not go for API implementation as it is not required in Assignment 2.

Inspect actual network requests only when necessary to understand application behavior or when the assignment explicitly requires API-level validation.

## 4. Establish Correct Component Boundaries

Based on actual DOM inspection, determine the correct ownership of each element.

The intended architectural direction is:

### HeaderComponent

Responsible for global navigation and header interactions.

Existing implementation should be retained if correct.

### ProductsPage

Responsible for product listing page-level functionality, such as:

- Getting product cards.
- Getting product names and prices.
- Opening a product detail page.
- Getting the page title.
- Managing page-level listing interactions where appropriate.

### ProductsSidebarComponent

If DOM inspection confirms the sidebar is a reusable, independently identifiable UI component, create a dedicated component in the existing `components/` folder.

It should own sidebar-related interactions:

- Search.
- Clear search.
- Sorting.
- Price range.
- Category filters.
- Other sidebar controls discovered in the actual DOM.

ProductsPage should compose or delegate to this component instead of implementing all its internal controls itself.

If the sidebar is not reusable or has a different actual structure, explain the appropriate alternative before implementing it.

Do not create unnecessary abstractions or components just to satisfy a predefined architecture.

## 5. Locator Strategy

Use Playwright's recommended locator strategy.

Prioritize:

1. `get_by_role()`
2. `get_by_label()`
3. `get_by_placeholder()`
4. `get_by_text()` when appropriate.
5. Actual stable IDs, names, and data attributes found in the DOM.
6. CSS selectors only when semantic locators are unsuitable.

Important rules:

- Never invent `data-test` or `data-testid` attributes.
- Never assume an element has a particular ID or class.
- Never use selectors copied from an unrelated application.
- Avoid brittle positional selectors.
- Avoid unnecessary XPath.
- Scope locators to the appropriate component or container.
- Check locator uniqueness where appropriate.
- Prefer accessible names and semantic HTML.

Every selector must be traceable to actual DOM evidence.

## 6. Review the Existing ProductsPage Implementation

Review the existing `pages/products_page.py` implementation.

In particular, investigate:

- `_PRODUCT_CARD`
- `_PRODUCT_NAME`
- `_PAGE_TITLE`
- `get_product_cards()`
- `get_product_name()`
- `click_nth_product()`
- `search()`
- `clear_search()`
- `sort_by_price_high_to_low()`
- `_wait_for_product_action()`
- `get_all_products()`
- `open_product()`

Identify which methods are correct, which need modification, and which should be delegated to components.

Do not automatically discard working methods.

### Important: Network Response Assertions

The existing implementation assumes endpoints such as:

- `/products`
- `/products/search`

It also assumes a JSON response structure containing `data`, `id`, and `name`.

Verify these assumptions against the actual application.

Do not introduce API-response assertions into ordinary UI page-object methods unless:

1. The actual network behavior has been inspected.
2. The response structure has been verified.
3. There is a clear testing requirement for such assertions.

For normal UI tests, prefer observable UI behavior and Playwright's retrying assertions.

## 7. Implement Assignment 2

After completing the DOM investigation and architectural review, implement the test cases of assignment 2 present in tests/week2/test_cases.csv

Use the existing assignment instructions and test cases as the source of truth for the required functionality.

Requirements:

- Reuse existing page objects and components.
- Create a dedicated sidebar component if justified.
- Keep page objects readable and maintainable.
- Keep selectors centralized within their appropriate page/component objects.
- Avoid duplicated locator definitions.
- Use appropriate return types and type hints.
- Use Playwright's auto-waiting and retrying assertions.
- Do not use explicit waits
- Avoid API dependencies.
- Follow existing fixture and dependency-injection patterns.
- Do not modify unrelated framework functionality.

Do not invent assignment requirements that are not documented.

## 8. Validation

After implementation:

1. Run the relevant existing tests.
2. Run the Assignment 2 tests.
3. Verify category navigation.
4. Verify product listing.
5. Verify sidebar search.
6. Verify sorting.
7. Check for locator strict-mode violations.
8. Check for flaky waits and unnecessary timeouts.
9. Check that the existing HeaderComponent still works.

Do not report a test as passing unless it was actually executed successfully.

## 9. Required Deliverables

Provide the following:

### A. DOM Investigation Report

Document the actual DOM structure and observed behavior of:

- Global header.
- Product listing.
- Left sidebar.
- Product cards.
- Pagination, if present.

Include the actual selectors and explain why they are reliable.

### B. Architecture Report

Explain:

- Which elements are global components.
- Which elements are page-specific components.
- Which responsibilities belong in ProductsPage.
- Which responsibilities belong in ProductsSidebarComponent.
- Which existing files can remain unchanged.

### C. Implementation

Implement the required changes in the existing project structure.

Show the files created, modified, and deleted, with a brief explanation of each change.

### D. Test Execution Report

List:

- Tests executed.
- Tests passed.
- Tests failed.
- Any unresolved issues.

## 10. Strict Rules

- Inspect first; implement second.
- The actual website DOM is the source of truth.
- Never invent selectors, attributes, endpoints, or response structures.
- Do not rewrite the entire framework.
- Do not unnecessarily change the existing HeaderComponent.
- Do not put all sidebar functionality inside ProductsPage.
- Do not create unnecessary components or fixtures.
- Do not silently remove existing working functionality.
- Do not claim browser inspection or test execution that did not happen.
- If any critical requirement cannot be established from the website or assignment instructions, report the uncertainty rather than guessing.

**Final objective:** Deliver a correctly structured, maintainable Playwright Python implementation that reflects the actual website architecture and DOM, rather than an implementation based on assumptions.
