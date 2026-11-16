import re

from playwright.sync_api import expect
import pytest


@pytest.mark.assignment1
def test_browse_the_category(open_category):
    products_page = open_category("Hand Tools")
    expect(products_page.get_products_page_title()).to_have_text("Category: Hand Tools")
    product_cards = products_page.get_product_cards()
    expect(product_cards).not_to_have_count(0)

    for index in range(product_cards.count()):
        product_name = products_page.get_product_name(index)
        expect(product_name).to_have_count(1)
        expect(product_name).to_contain_text(re.compile(r"\S"))
