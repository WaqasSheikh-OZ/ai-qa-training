from playwright.sync_api import Page, Locator, expect

class HeaderComponent:

    _NAVIGATION = "nav"
    _CART_ICON = '[data-test="nav-cart"]'
    _CART_COUNT = '[data-test="cart-quantity"]'
    _CATEGORIES_LINK = '[data-test="nav-categories"]'
    _CONTACT_LINK = '[data-test="nav-contact"]'

    def __init__(self, page: Page):
        self.page = page

        self._navigation = page.locator(self._NAVIGATION)
        self._cart_icon = page.locator(self._CART_ICON)
        self._cart_count = page.locator(self._CART_COUNT)
        self._categories_link = page.locator(self._CATEGORIES_LINK)
        self._contact_link = page.locator(self._CONTACT_LINK)

    def click_cart(self) -> None:
        expect(
            self._cart_icon,
            "Cannot open cart: the cart icon is not visible. "
            "Add at least one item to the cart before opening it.",
        ).to_be_visible()
        self._cart_icon.click()

    def get_cart_icon(self) -> Locator:
        return self._cart_icon

    def get_cart_count(self) -> Locator:
        return self._cart_count

    def get_cart_count_text(self) -> str:
        return self._cart_count.inner_text()

    def click_categories(self) -> None:
        self._categories_link.click()

    def select_category(self, category_name: str) -> None:
        self._navigation.get_by_role("link", name=category_name, exact=True).click()

    def click_contact(self) -> None:
        self._contact_link.click()

    