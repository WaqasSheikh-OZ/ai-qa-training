from playwright.sync_api import Locator, Page, Route

from pages.base_page import BasePage


class ContactPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.blocked_posts = []

    def field(self, name: str) -> Locator:
        return self.page.locator(f'[data-test="{name}"]')

    def error(self, name: str) -> Locator:
        return self.page.locator(f'[data-test="{name}-error"]')

    def fill_contact(self, first_name: str, email: str, message: str) -> None:
        self.field("first-name").fill(first_name)
        self.field("email").fill(email)
        self.field("message").fill(message)

    def _block_posts(self, route: Route) -> None:
        if route.request.method == "POST":
            self.blocked_posts.append(route.request.url)
            route.abort()
        else:
            route.continue_()

    def submit_incomplete(self) -> None:
        fields = ("first-name", "last-name", "email", "subject", "message")
        if all(self.field(field).input_value().strip() for field in fields):
            raise ValueError("A completed contact form must never be submitted")
        self.page.route("**/*", self._block_posts)
        self.page.locator('[data-test="contact-submit"]').click()
