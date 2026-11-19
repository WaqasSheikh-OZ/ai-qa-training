import re

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage
import pytest


@pytest.mark.assignment1
def test_product_details(navigation):
    products_page = navigation.open_category("Hand Tools")
    product_cards = products_page.get_product_cards()
    
    expect(product_cards).not_to_have_count(0)
    expect(products_page.get_product_name(0)).to_contain_text(re.compile(r"\S"))
    first_product_name = products_page.get_product_name_text(0)
    product_details_page = products_page.click_nth_product(0)
    expect(product_details_page.get_product_name()).to_have_text(first_product_name)
    expect(product_details_page.get_unit_price()).not_to_be_empty()
    expect(product_details_page.get_add_to_cart_button()).to_be_visible()