import pytest
from playwright.sync_api import Page, sync_playwright
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from components.header_component import HeaderComponent

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
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def home_page(page) -> HomePage:
    page.goto("/")
    return HomePage(page)

@pytest.fixture
def header_component(home_page) -> HeaderComponent:
    page = home_page.page
    page.header = HeaderComponent(page)
    return page.header


@pytest.fixture
def open_category(header_component):
    def _open(name: str) -> ProductsPage:
        header_component.click_categories()
        header_component.select_category(name)
        page = header_component.page
        return ProductsPage(page)
    return _open

