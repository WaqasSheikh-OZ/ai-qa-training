from pages.base_page import BasePage
from playwright.sync_api import Locator, Page

class ProductDetailsPage(BasePage):
    # centerlize the locators and make them private
    _PRODUCT_NAME = '[data-test="product-name"]'
    _PRODUCT_DESCRIPTION = '[data-test="product-description"]'
    _UNIT_PRICE = '[data-test="unit-price"]'
    _ADD_TO_CART_BUTTON = '[data-test="add-to-cart"]'


    def __init__(self, page: Page):
        super().__init__(page)
        self._product_name = page.locator(self._PRODUCT_NAME)
        self._product_description = page.locator(self._PRODUCT_DESCRIPTION)
        self._unit_price = page.locator(self._UNIT_PRICE)
        self._add_to_cart_button = page.locator(self._ADD_TO_CART_BUTTON)

    def get_product_name(self) -> Locator:
        return self._product_name

    def get_product_description(self) -> Locator:
        return self._product_description

    def get_unit_price(self) -> Locator:
        return self._unit_price

    def get_unit_price_text(self) -> str:
        return self.get_unit_price().inner_text()

    def get_add_to_cart_button(self) -> Locator:
        return self._add_to_cart_button

    def add_to_cart(self) -> None:
        self.get_add_to_cart_button().click()
