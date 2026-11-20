from playwright.sync_api import Locator, Page, Route

from pages.base_page import BasePage


class ContactFormPage(BasePage):
    # centerlize the locators and make them private
    _FIRST_NAME = '[data-test="first-name"]'
    _LAST_NAME = '[data-test="last-name"]'
    _EMAIL = '[data-test="email"]'
    _SUBJECT = '[data-test="subject"]'
    _MESSAGE = '[data-test="message"]'
    _FIRST_NAME_ERROR = '[data-test="first-name-error"]'
    _LAST_NAME_ERROR = '[data-test="last-name-error"]'
    _EMAIL_ERROR = '[data-test="email-error"]'
    _SUBJECT_ERROR = '[data-test="subject-error"]'
    _MESSAGE_ERROR = '[data-test="message-error"]'
    _SELECTED_SUBJECT = '[data-test="subject"] option:checked'
    _SEND_BUTTON_NAME = "Send"
    _ALL_URLS = "**/*"
    _READ_ONLY_METHODS = ("GET", "HEAD")

    _FIELDS = {
        "first_name": _FIRST_NAME,
        "last_name": _LAST_NAME,
        "email": _EMAIL,
        "subject": _SUBJECT,
        "message": _MESSAGE,
    }
    _ERRORS = {
        "first_name": _FIRST_NAME_ERROR,
        "last_name": _LAST_NAME_ERROR,
        "email": _EMAIL_ERROR,
        "subject": _SUBJECT_ERROR,
        "message": _MESSAGE_ERROR,
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._selected_subject = page.locator(self._SELECTED_SUBJECT)
        self._send_button = page.get_by_role("button", name=self._SEND_BUTTON_NAME, exact=True)
        self._outgoing_writes_blocked = False

    def get_field(self, field: str) -> Locator:
        return self.page.locator(self._FIELDS[field])

    def get_error(self, field: str) -> Locator:
        return self.page.locator(self._ERRORS[field])

    def get_selected_subject(self) -> Locator:
        return self._selected_subject

    def fill_form(self, data: dict[str, str], omit: tuple[str, ...] = ()) -> None:
        for field, value in data.items():
            if field in omit:
                continue
            if field == "subject":
                self.get_field(field).select_option(label=value)
            else:
                self.get_field(field).fill(value)

    def move_focus_to(self, field: str) -> None:
        self.get_field(field).focus()

    def submit_incomplete(self) -> None:
        """Press Send only while a required field is empty; a completed form reaches a real inbox."""
        if all(self.get_field(field).input_value().strip() for field in self._FIELDS):
            raise ValueError("Never press Send on a completed contact form")
        self._block_outgoing_writes()
        self._send_button.click()

    def is_error_below_field(self, field: str) -> bool:
        field_box = self.get_field(field).bounding_box()
        error_box = self.get_error(field).bounding_box()
        if field_box is None or error_box is None:
            return False
        return error_box["y"] >= field_box["y"] + field_box["height"]

    def _block_outgoing_writes(self) -> None:
        if self._outgoing_writes_blocked:
            return

        def abort_writes(route: Route) -> None:
            if route.request.method in self._READ_ONLY_METHODS:
                route.continue_()
            else:
                route.abort()

        self.page.route(self._ALL_URLS, abort_writes)
        self._outgoing_writes_blocked = True
