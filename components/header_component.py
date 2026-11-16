from playwright.sync_api import Page, Locator


class HeaderComponent:

    _CART_ICON = '[data-test="nav-cart"]'
    _CART_COUNT = '[data-test="cart-quantity"]'
    _CATEGORIES_LINK = '[data-test="nav-categories"]'

    def __init__(self, page: Page):
        self.page = page

        self._cart_icon = page.locator(self._CART_ICON)
        self._cart_count = page.locator(self._CART_COUNT)
        self.categories_link = page.locator(self._CATEGORIES_LINK)

    def click_cart(self):
        self._cart_icon.click()

    def get_cart_count(self) -> Locator:
        return self._cart_count

    def get_cart_count_text(self) -> str:
        return self._cart_count.inner_text()

    def click_categories(self):
        self.categories_link.click()

    def select_category(self, category_name: str):
        self.page.get_by_text(category_name,exact=True).click()

    