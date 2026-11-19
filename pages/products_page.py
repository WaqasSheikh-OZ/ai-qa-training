from collections.abc import Callable

from pages.base_page import BasePage
from playwright.sync_api import Locator, Page, expect
from pages.product_details_page import ProductDetailsPage


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

    def click_nth_product(self, index: int) -> Page:
        self._product_cards.nth(index).click()
        return ProductDetailsPage(self.page)

    def _wait_for_product_action(self, action: Callable[[], object]) -> None:
        with self.page.expect_response(
            lambda response: response.url.split("?")[0].endswith(
                ("/products", "/products/search")
            )
        ) as response_info:
            action()
        response = response_info.value
        assert response.ok, f"Product request failed: {response.status}"
        products = response.json()["data"]
        expect(self._product_cards).to_have_count(len(products))
        if products:
            expect(self._product_cards.first).to_have_attribute(
                "href", f"/product/{products[0]['id']}"
            )
            expect(self._product_cards.locator(self._PRODUCT_NAME)).to_have_text(
                [product["name"] for product in products]
            )
        else:
            expect(self.page.locator('[data-test="no-results"]')).to_be_visible()

    def search(self, word: str, use_enter: bool = False) -> None:
        search_box = self.page.locator('[data-test="search-query"]')
        search_box.fill(word)
        if use_enter:
            self._wait_for_product_action(lambda: search_box.press("Enter"))
        else:
            self._wait_for_product_action(
                lambda: self.page.locator('[data-test="search-submit"]').click()
            )

    def clear_search(self) -> None:
        self._wait_for_product_action(
            lambda: self.page.locator('[data-test="search-reset"]').click()
        )

    def sort_by_price_high_to_low(self) -> None:
        self._wait_for_product_action(
            lambda: self.page.locator('[data-test="sort"]').select_option(
                label="Price (High - Low)"
            )
        )

    def get_all_products(self) -> list[tuple[str, str, str]]:
        self._product_cards.first.wait_for()
        products = []
        while True:
            for card in self._product_cards.all():
                href = card.get_attribute("href")
                assert href is not None, "Product card has no link"
                products.append(
                    (
                        href,
                        card.locator(self._PRODUCT_NAME).inner_text().strip(),
                        card.locator('[data-test="product-price"]').inner_text().strip(),
                    )
                )
            next_button = self.page.locator('[data-test="pagination-next"]')
            if not next_button.count() or "disabled" in (
                next_button.locator("..").get_attribute("class") or ""
            ).split():
                return products
            self._wait_for_product_action(next_button.click)

    def open_product(self, name: str) -> ProductDetailsPage:
        self._product_cards.filter(
            has=self.page.get_by_role("heading", name=name, exact=True)
        ).click()
        return ProductDetailsPage(self.page)
