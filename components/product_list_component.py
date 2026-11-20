import re
from typing import NamedTuple

from playwright.sync_api import Locator, Page, expect


class ProductListing(NamedTuple):
    href: str
    name: str
    price: str


class ProductListComponent:
    # centralized private locators for the product grid shared by home and category pages
    _PRODUCT_CARD = "a.card"
    _PRODUCT_NAME = '[data-test="product-name"]'
    _PRODUCT_PRICE = '[data-test="product-price"]'
    _ECO_BADGE = '[data-test="eco-badge"]'
    _SEARCH_RESULT_COUNT = '[data-test="search-result-count"]'
    _SEARCH_COMPLETED = '[data-test="search_completed"]'
    _SORTING_COMPLETED = '[data-test="sorting_completed"]'
    _NO_RESULTS = '[data-test="no-results"]'
    _NEXT_PAGE = '[data-test="pagination-next"]'
    _DISABLED_NEXT_PAGE = 'li.disabled > [data-test="pagination-next"]'
    _ACTIVE_PAGE = "ul.pagination li.active"
    _FIRST_PAGE_BUTTON_NAME = "Page-1"
    _HREF = "href"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._product_cards = page.locator(self._PRODUCT_CARD)
        self._product_names = page.locator(self._PRODUCT_NAME)
        self._search_result_count = page.locator(self._SEARCH_RESULT_COUNT)
        self._search_completed = page.locator(self._SEARCH_COMPLETED)
        self._sorting_completed = page.locator(self._SORTING_COMPLETED)
        self._no_results = page.locator(self._NO_RESULTS)
        self._next_page = page.locator(self._NEXT_PAGE)
        self._disabled_next_page = page.locator(self._DISABLED_NEXT_PAGE)
        self._active_page = page.locator(self._ACTIVE_PAGE)
        self._first_page_button = page.get_by_role(
            "button", name=self._FIRST_PAGE_BUTTON_NAME, exact=True
        )

    def get_product_cards(self) -> Locator:
        return self._product_cards

    def get_product_card(self, name: str) -> Locator:
        exact_name = re.compile(rf"^\s*{re.escape(name)}\s*$")
        return self._product_cards.filter(
            has=self._product_names.filter(has_text=exact_name)
        )

    def get_product_name(self, index: int) -> Locator:
        return self._product_cards.nth(index).locator(self._PRODUCT_NAME)

    def get_product_name_text(self, index: int) -> str:
        return self.get_product_name(index).inner_text()

    def get_product_prices(self) -> Locator:
        return self._product_cards.locator(self._PRODUCT_PRICE)

    def get_eco_badge(self, name: str) -> Locator:
        return self.get_product_card(name).locator(self._ECO_BADGE)

    def click_nth_product(self, index: int) -> None:
        self._product_cards.nth(index).click()

    def click_product(self, name: str) -> None:
        self.get_product_card(name).click()

    def get_search_result_count(self) -> Locator:
        return self._search_result_count

    def get_no_results_message(self) -> Locator:
        return self._no_results

    def get_active_page(self) -> Locator:
        return self._active_page

    def get_active_page_number(self) -> str:
            return self._active_page.inner_text()

    def get_first_product_href(self) -> str | None:
        if self._product_cards.count() == 0:
            return None
        return self._product_cards.first.get_attribute(self._HREF)

    def wait_for_products_loaded(self) -> None:
        expect(self._product_cards.first).to_be_visible()

    def wait_for_search_completed(self) -> None:
        expect(self._search_completed).to_be_attached()

    def wait_for_sorting_completed(self) -> None:
        expect(self._sorting_completed).to_be_attached()

    def wait_for_listing_change(self, previous_first_href: str | None) -> None:
        # reset and pagination expose no completion marker, so wait for the grid itself to change
        first_card = self._product_cards.first
        if previous_first_href is None:
            expect(first_card).to_be_visible()
        else:
            expect(first_card).not_to_have_attribute(self._HREF, previous_first_href)

    def has_next_page(self) -> bool:
        return self._next_page.count() > 0 and self._disabled_next_page.count() == 0

    def go_to_next_page(self) -> None:
        previous_first_href = self.get_first_product_href()
        self._next_page.click()
        self.wait_for_listing_change(previous_first_href)

    def go_to_last_page(self) -> None:
        self.wait_for_products_loaded()
        while self.has_next_page():
            self.go_to_next_page()

    def get_all_products(self) -> list[ProductListing]:
        """Collect every product across all pages, starting from and returning to page 1."""
        self.wait_for_products_loaded()
        first_page_href = self.get_first_product_href()
        products = self._read_visible_products()
        while self.has_next_page():
            self.go_to_next_page()
            products.extend(self._read_visible_products())
        if first_page_href and self.get_first_product_href() != first_page_href:
            self._first_page_button.click()
            expect(self._product_cards.first).to_have_attribute(self._HREF, first_page_href)
        return products

    def _read_visible_products(self) -> list[ProductListing]:
        products = []
        for card in self._product_cards.all():
            href = card.get_attribute(self._HREF)
            if href is None:
                raise ValueError("A product card has no link")
            products.append(
                ProductListing(
                    href,
                    card.locator(self._PRODUCT_NAME).inner_text().strip(),
                    card.locator(self._PRODUCT_PRICE).inner_text().strip(),
                )
            )
        return products
