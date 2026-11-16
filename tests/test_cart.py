import re

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage
from pages.cart_page import CartPage
import pytest

@pytest.mark.assignment1
def test_add_product_to_cart(open_category):
    products_page = open_category("Hand Tools")
    product_cards = products_page.get_product_cards()
    
    expect(product_cards).not_to_have_count(0)
    expect(products_page.get_product_name(0)).to_contain_text(re.compile(r"\S"))

    first_product_name = products_page.get_product_name_text(0)
    product_cards.nth(0).click()
    product_details_page = ProductDetailsPage(products_page.page)

    expect(product_details_page.get_product_name()).to_have_text(first_product_name)
    expect(product_details_page.get_unit_price()).not_to_be_empty()
    expect(product_details_page.get_add_to_cart_button()).to_be_visible()

    first_product_price = product_details_page.get_unit_price_text()
    product_details_page.add_to_cart()

    expect(product_details_page.header.get_cart_count()).to_have_text("1")
    
    product_details_page.header.click_cart()
    cart_page = CartPage(product_details_page.page)

    expect(cart_page.get_cart_items()).to_have_count(1)
    expect(cart_page.get_cart_item_name(0)).to_have_text(first_product_name)
    expect(cart_page.get_cart_item_price(0)).to_have_text(f"${first_product_price}")
    
    