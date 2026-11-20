# Playwright Framework

A beginner-friendly Python test framework scaffold using the Playwright synchronous API, Pytest, and Page Object Model.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Adjust `BASE_URL`, `BROWSER`, or `HEADLESS` in `.env` for your local environment. The `.env` file is ignored by Git.

## Run tests

```powershell
pytest
```

## Fixtures and shared navigation

The function-scoped `page` fixture creates a fresh browser context and opens
`/` relative to `BASE_URL` before each test that needs it. The context is
closed after the test, keeping browser state isolated. The browser itself is
shared for the test session.

Request the fixture your test needs: `page` for direct Playwright access,
`home_page` for home-page actions, `header_component` for header actions, or
`navigation` for transitions between pages. These fixtures all depend directly
or indirectly on `page`, so tests do not need to request `page` separately.
No category is opened unless the test explicitly navigates to one.

`HeaderComponent` owns header locators and UI actions, but does not import
destination page objects. `Navigation` coordinates shared header actions and
constructs the destination page using the current Playwright `Page`.

The function-scoped `navigation` fixture shares the test's browser tab and can
open the cart from any page, not just the home page:

```python
def test_add_product_to_cart(navigation):
    products = navigation.open_category("Hand Tools")
    details = products.click_nth_product(0)
    details.add_to_cart()
    cart = navigation.open_cart()
    expect(cart.get_cart_items()).to_have_count(1)
```

Use `navigation.open_home()` to open the home page and
`navigation.open_category(name)` for category transitions from the current
page. Tests use returned page objects rather than constructing them.
Keep `Navigation` out of `BasePage` and component imports so dependencies remain
one-way and do not introduce circular imports.

## Product listings, search and sorting

The home page and category pages share the same product grid and left sidebar,
so both are modelled as components and composed into the pages:

- `ProductListComponent` owns product cards, prices, eco badges, search result
  messages and pagination. `get_all_products()` collects every page and returns
  to page 1.
- `ProductsSidebarComponent` owns search, clear search and sorting.
- `HomePage` composes both and adds flows such as `search(word)`,
  `clear_search()`, `sort_by(option)` and `search_and_open_product(name)`.
  `ProductsPage` (category pages) composes the same components.

Page objects wait for observable UI state: `open_home()` waits for the initial
catalog, searches wait for the app's search-completed marker, and sorting waits
for the sorting-completed marker.

## Test data, helpers and markers

Test data lives in `test_data/test_data.json` and is available through the
session-scoped `test_data` fixture. Shared helpers such as `parse_price` and
`format_price` live in `utilities/helpers.py`. Tests contain no locators or
helper functions; they call page-object methods and assert the outcome.

Assignment tests are marked `assignment1` or `assignment2` (registered in
`pytest.ini`), so `pytest -m assignment2` runs only the Week 2 tests.

The contact page's `submit_incomplete()` refuses to press Send on a completed
form and blocks outgoing writes, because a sent form reaches a real inbox.

The cart test verifies navigation from home, category, and product-details pages
after adding an item, since the application does not expose the cart control
when the cart is empty.

`HeaderComponent.click_cart()` checks icon visibility using Playwright's
auto-retrying assertion before clicking. If the icon remains unavailable within
the assertion timeout (5 seconds by default), it raises an `AssertionError`
explaining that an item must be added first. No click is attempted and
`Navigation.open_cart()` does not construct a destination page on failure.
