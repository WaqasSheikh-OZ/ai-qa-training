from playwright.sync_api import Locator, Page

from components.product_list_component import ProductListComponent, ProductListing
from components.products_sidebar_component import ProductsSidebarComponent
from pages.base_page import BasePage
from pages.product_details_page import ProductDetailsPage


class ProductsPage(BasePage):
    # centralized private locators; the product grid and sidebar own their own locators
    _PAGE_TITLE = '[data-test="page-title"]'

    def __init__(self, page: Page):
        super().__init__(page)
        self._page_title = page.locator(self._PAGE_TITLE)
        self.product_list = ProductListComponent(page)
        self.sidebar = ProductsSidebarComponent(page)

    def get_products_page_title(self) -> Locator:
        return self._page_title

    def get_product_cards(self) -> Locator:
        return self.product_list.get_product_cards()

    def get_product_name(self, index: int) -> Locator:
        # returns a locator for the product name at the given index so that playwright can retry assertions
        return self.product_list.get_product_name(index)

    def get_product_name_text(self, index: int) -> str:
        return self.product_list.get_product_name_text(index)

    def click_nth_product(self, index: int) -> ProductDetailsPage:
        self.product_list.click_nth_product(index)
        return ProductDetailsPage(self.page)

    def sort_by(self, option: str) -> None:
        self.sidebar.sort(option)
        self.product_list.wait_for_sorting_completed()

    def get_all_products(self) -> list[ProductListing]:
        return self.product_list.get_all_products()

    def get_subcategory_names(self, category: str) -> list[str]:
        return self.sidebar.get_subcategory_names(category)
