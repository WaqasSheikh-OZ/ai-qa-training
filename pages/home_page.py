from playwright.sync_api import Page

from components.product_list_component import ProductListComponent, ProductListing
from components.products_sidebar_component import ProductsSidebarComponent
from pages.base_page import BasePage
from pages.product_details_page import ProductDetailsPage


class HomePage(BasePage):
    # composes the shared product grid and sidebar instead of inheriting from ProductsPage

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_list = ProductListComponent(page)
        self.sidebar = ProductsSidebarComponent(page)

    def wait_for_page_loaded(self) -> None:
        # searching before the initial catalog arrives lets the late catalog overwrite the results
        self.product_list.wait_for_products_loaded()

    def search(self, word: str, *, use_enter: bool = False) -> None:
        self.sidebar.search(word, use_enter=use_enter)
        self.product_list.wait_for_search_completed()

    def clear_search(self) -> None:
        previous_first_href = self.product_list.get_first_product_href()
        self.sidebar.clear_search()
        self.product_list.wait_for_listing_change(previous_first_href)

    def sort_by(self, option: str) -> None:
        self.sidebar.sort(option)
        self.product_list.wait_for_sorting_completed()

    def get_all_products(self) -> list[ProductListing]:
        return self.product_list.get_all_products()

    def open_product(self, name: str) -> ProductDetailsPage:
        self.product_list.click_product(name)
        return ProductDetailsPage(self.page)

    def search_and_open_product(self, name: str) -> ProductDetailsPage:
        self.search(name)
        return self.open_product(name)
