from playwright.sync_api import Locator, Page, expect


class ProductsSidebarComponent:
    # centralized private locators for the left sidebar on product listing pages
    _SIDEBAR = "#filters"
    _SEARCH_LABEL = "Search"
    _SEARCH_BUTTON_NAME = "Search"
    _SEARCH_RESET = '[data-test="search-reset"]'
    _SORT = '[data-test="sort"]'
    _CATEGORY_GROUP = "div.checkbox"
    _SUBCATEGORY_LABEL = "ul label"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._sidebar = page.locator(self._SIDEBAR)
        self._search_input = self._sidebar.get_by_label(self._SEARCH_LABEL, exact=True)
        self._search_button = self._sidebar.get_by_role(
            "button", name=self._SEARCH_BUTTON_NAME, exact=True
        )
        self._search_reset = self._sidebar.locator(self._SEARCH_RESET)
        self._sort = self._sidebar.locator(self._SORT)
        self._category_groups = self._sidebar.locator(self._CATEGORY_GROUP)

    def get_search_input(self) -> Locator:
        return self._search_input

    def search(self, word: str, *, use_enter: bool = False) -> None:
        self._search_input.fill(word)
        if use_enter:
            self._search_input.press("Enter")
        else:
            self._search_button.click()

    def clear_search(self) -> None:
        self._search_reset.click()

    def sort(self, option: str) -> None:
        self._sort.select_option(label=option)

    def get_subcategory_names(self, category: str) -> list[str]:
        group = self._category_groups.filter(
            has=self.page.get_by_role("checkbox", name=category, exact=True)
        )
        labels = group.locator(self._SUBCATEGORY_LABEL)
        expect(labels.first).to_be_visible()
        return [label.strip() for label in labels.all_text_contents()]
