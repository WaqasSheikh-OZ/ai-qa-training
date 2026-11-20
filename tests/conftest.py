from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright, sync_playwright
from api.products_api import ProductsApi
from pages.home_page import HomePage
from pages.navigation import Navigation
from utilities.test_data import load_test_data

from config.settings import API_BASE_URL, BROWSER, HEADLESS, BASE_URL

@pytest.fixture(scope="session")
def playwright() -> Iterator[Playwright]:
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser_type = getattr(playwright, BROWSER)
    browser = browser_type.launch(headless=HEADLESS)
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(base_url=BASE_URL)
    try:
        page = context.new_page()
        page.goto("/")
        yield page
    finally:
        context.close()

@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def navigation(page: Page) -> Navigation:
    return Navigation(page)


@pytest.fixture(scope="session")
def test_data() -> dict:
    return load_test_data()


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    request_context = playwright.request.new_context(base_url=API_BASE_URL)
    yield request_context
    request_context.dispose()


@pytest.fixture
def products_api(api_request_context: APIRequestContext) -> ProductsApi:
    return ProductsApi(api_request_context)

