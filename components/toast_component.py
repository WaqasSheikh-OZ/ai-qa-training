from playwright.sync_api import Locator, Page


class ToastComponent:
    _TOAST_MESSAGE = '#toast-container [role="alert"]'

    def __init__(self, page: Page) -> None:
        self._toast_messages = page.locator(self._TOAST_MESSAGE)

    def get_message(self, text: str) -> Locator:
        return self._toast_messages.filter(has_text=text)
