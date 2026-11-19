from playwright.sync_api import Page
from pages.products_page import ProductsPage


class HomePage(ProductsPage):

    def __init__(self, page: Page):
        super().__init__(page)

        
