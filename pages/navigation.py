from playwright.sync_api import Page

from components.header_component import HeaderComponent
from pages.cart_page import CartPage
from pages.contact_form_page import ContactFormPage
from pages.home_page import HomePage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


class Navigation:
    _HOME_PATH = "/"

    def __init__(self, page: Page) -> None:
        self._page = page
        self._header = HeaderComponent(page)

    def open_home(self) -> HomePage:
        self._page.goto(self._HOME_PATH)
        home_page = HomePage(self._page)
        home_page.wait_for_page_loaded()
        return home_page

    def open_cart(self) -> CartPage:
        self._header.click_cart()
        return CartPage(self._page)

    def open_category(self, category_name: str) -> ProductsPage:
        self._header.click_categories()
        self._header.select_category(category_name)
        return ProductsPage(self._page)

    def open_contact(self) -> ContactFormPage:
        self._header.click_contact()
        return ContactFormPage(self._page)

    def open_product_link(self, href: str) -> ProductDetailsPage:
        self._page.goto(href)
        return ProductDetailsPage(self._page)
