from playwright.sync_api import expect
import pytest

from utilities.test_data import load_csv_params


@pytest.mark.assignment3
@pytest.mark.parametrize("row", load_csv_params("tests/week3/data.csv"))
def test_typed_quantity_is_added_to_cart(navigation, row):
    product = row["product"]
    expected_quantity = row["expected_quantity"]

    product_details_page = navigation.open_home().search_and_open_product(product)
    product_details_page.add_to_cart(row["quantity_input"])

    expect(product_details_page.toast.get_message(row["expected_message"])).to_be_visible()
    expect(product_details_page.header.get_cart_count()).to_have_text(expected_quantity)

    cart_page = navigation.open_cart()
    expect(cart_page.get_cart_items()).to_have_count(1)
    expect(cart_page.get_quantity_input(product)).to_have_value(expected_quantity)
