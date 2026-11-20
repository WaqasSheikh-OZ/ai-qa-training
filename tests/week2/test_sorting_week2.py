from playwright.sync_api import expect
import pytest

from utilities.helpers import parse_price


@pytest.mark.assignment2
def test_tc_06_all_products_sorted_by_price_high_to_low(navigation, test_data):
    home_page = navigation.open_home()
    all_products = home_page.get_all_products()

    home_page.sort_by(test_data["sorting"]["price_high_to_low"])
    sorted_products = home_page.get_all_products()

    prices = [parse_price(product.price) for product in sorted_products]
    assert set(sorted_products) == set(all_products)
    assert len(sorted_products) == len(all_products)
    assert prices == sorted(prices, reverse=True)


@pytest.mark.assignment2
def test_tc_07_all_products_sorted_by_name_z_to_a(navigation, test_data):
    home_page = navigation.open_home()
    all_products = home_page.get_all_products()

    home_page.sort_by(test_data["sorting"]["name_z_to_a"])
    sorted_products = home_page.get_all_products()

    names = [product.name for product in sorted_products]
    assert set(sorted_products) == set(all_products)
    assert len(sorted_products) == len(all_products)
    assert names == sorted(names, key=str.casefold, reverse=True)


@pytest.mark.assignment2
def test_tc_08_power_tools_sorted_by_price_stay_in_category(navigation, test_data):
    category = test_data["sorting"]["category"]
    products_page = navigation.open_category(category)
    expect(products_page.get_products_page_title()).to_contain_text(category)
    power_tool_types = products_page.get_subcategory_names(category)
    category_products = products_page.get_all_products()

    products_page.sort_by(test_data["sorting"]["price_high_to_low"])
    sorted_products = products_page.get_all_products()

    expect(products_page.get_products_page_title()).to_contain_text(category)
    prices = [parse_price(product.price) for product in sorted_products]
    assert set(sorted_products) == set(category_products)
    assert prices == sorted(prices, reverse=True)

    for product in sorted_products:
        product_details_page = navigation.open_product_link(product.href)
        assert product_details_page.get_category_text() in power_tool_types
