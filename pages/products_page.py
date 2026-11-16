from pages.base_page import BasePage
from playwright.sync_api import Locator, Page


class ProductsPage(BasePage):
    # Centralized selectors: stable hooks only, no dynamic-value prefix matching
    
    _PRODUCT_CARD = "a.card"
    _PRODUCT_NAME = '[data-test="product-name"]'
    _PAGE_TITLE = '[data-test="page-title"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self._product_cards = page.locator(self._PRODUCT_CARD)
        self._page_title = page.locator(self._PAGE_TITLE)

    def get_product_cards(self) -> Locator:
        return self._product_cards

    def get_product_name(self, index: int) -> Locator:
        # returns a locator for the product name at the given index so that playwright can retry assertions
        return self._product_cards.nth(index).locator(self._PRODUCT_NAME)

    def get_product_name_text(self, index: int) -> str:
        return self.get_product_name(index).inner_text()

    def get_products_page_title(self) -> Locator:
        return self._page_title
