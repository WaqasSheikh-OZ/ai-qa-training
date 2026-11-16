from pages.base_page import BasePage
from playwright.sync_api import Locator, Page


class CartPage(BasePage):
    # centerlize the locators and make them private
    _CART_TABLE = "table.table.table-hover"
    _CART_ROWS = "table.table.table-hover tbody tr"
    _PRODUCT_TITLE = '[data-test="product-title"]'
    _PRODUCT_QUANTITY = '[data-test="product-quantity"]'
    _PRODUCT_PRICE = '[data-test="product-price"]'
    _LINE_PRICE = '[data-test="line-price"]'
    _REMOVE_ITEM_BUTTON = "a.btn.btn-danger"

    def __init__(self, page: Page):
        super().__init__(page)
        self._cart_table = page.locator(self._CART_TABLE)
        self._cart_rows = page.locator(self._CART_ROWS)
        self._product_titles = page.locator(self._PRODUCT_TITLE)

    def get_cart_table(self) -> Locator:
        return self._cart_table

    def get_cart_rows(self) -> Locator:
        return self._cart_rows

    def get_cart_items_count(self) -> int:
        return self._cart_rows.count()

    def get_product_titles(self) -> Locator:
        return self._product_titles

    # index-based accessors
    def get_cart_items(self) -> Locator:
        return self._cart_rows

    def get_cart_item_name(self, index: int) -> Locator:
        return self._cart_rows.nth(index).locator(self._PRODUCT_TITLE)

    def get_cart_item_price(self, index: int) -> Locator:
        return self._cart_rows.nth(index).locator(self._PRODUCT_PRICE)

    def get_row_by_product_title(self, product_title: str) -> Locator:
        return self._cart_rows.filter(
            has=self.page.locator(self._PRODUCT_TITLE, has_text=product_title)
        )

    def get_product_title(self, product_title: str) -> Locator:
        return self.get_row_by_product_title(product_title).locator(self._PRODUCT_TITLE)

    def get_quantity_input(self, product_title: str) -> Locator:
        return self.get_row_by_product_title(product_title).locator(self._PRODUCT_QUANTITY)

    def set_quantity(self, product_title: str, quantity: int) -> None:
        quantity_input = self.get_quantity_input(product_title)
        quantity_input.fill(str(quantity))
        quantity_input.press("Enter")

    def get_product_price(self, product_title: str) -> Locator:
        return self.get_row_by_product_title(product_title).locator(self._PRODUCT_PRICE)

    def get_product_price_text(self, product_title: str) -> str:
        return self.get_product_price(product_title).inner_text()

    def get_line_price(self, product_title: str) -> Locator:
        return self.get_row_by_product_title(product_title).locator(self._LINE_PRICE)

    def get_line_price_text(self, product_title: str) -> str:
        return self.get_line_price(product_title).inner_text()

    def get_remove_item_button(self, product_title: str) -> Locator:
        return self.get_row_by_product_title(product_title).locator(self._REMOVE_ITEM_BUTTON)

    def remove_item(self, product_title: str) -> None:
        self.get_remove_item_button(product_title).click()
