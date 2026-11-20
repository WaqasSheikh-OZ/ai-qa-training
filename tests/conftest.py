import pytest
from playwright.sync_api import Page, sync_playwright
from pages.home_page import HomePage
from pages.navigation import Navigation
from utilities.test_data import load_test_data

from config.settings import BROWSER, HEADLESS, BASE_URL

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
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

