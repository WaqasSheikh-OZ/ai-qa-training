from playwright.sync_api import Page
from components.header_component import HeaderComponent
from components.toast_component import ToastComponent

class BasePage:
    
    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = HeaderComponent(page)
        self.toast = ToastComponent(page)
        
