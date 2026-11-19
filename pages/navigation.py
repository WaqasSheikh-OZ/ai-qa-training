from playwright.sync_api import Page

from components.header_component import HeaderComponent
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.products_page import ProductsPage


class Navigation:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._header = HeaderComponent(page)

    def open_home(self) -> HomePage:
        self._page.goto("/")
        return HomePage(self._page)

    def open_cart(self) -> CartPage:
        self._header.click_cart()
        return CartPage(self._page)

    def open_category(self, category_name: str) -> ProductsPage:
        self._header.click_categories()
        self._header.select_category(category_name)
        return ProductsPage(self._page)
