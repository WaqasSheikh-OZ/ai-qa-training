from decimal import Decimal

from playwright.sync_api import expect


def prices_in_order(products):
    return [Decimal(price.replace("$", "").replace(",", "")) for _, _, price in products]


def test_tc_06_all_products_sorted_by_descending_price(navigation):
    products = navigation.open_home()
    original = products.get_all_products()
    products.sort_by_price_high_to_low()
    sorted_products = products.get_all_products()

    assert len(sorted_products) == len(original)
    assert {item[0] for item in sorted_products} == {item[0] for item in original}
    prices = prices_in_order(sorted_products)
    assert len(set(prices)) > 1
    assert prices == sorted(prices, reverse=True)


def test_tc_08_power_tools_sorted_by_descending_price(navigation):
    products = navigation.open_category("Power Tools")
    expect(products.get_products_page_title()).to_contain_text("Power Tools")
    original = products.get_all_products()
    products.sort_by_price_high_to_low()
    expect(products.get_products_page_title()).to_contain_text("Power Tools")
    sorted_products = products.get_all_products()

    assert len(sorted_products) == len(original)
    assert {item[0] for item in sorted_products} == {item[0] for item in original}
    prices = prices_in_order(sorted_products)
    assert len(set(prices)) > 1
    assert prices == sorted(prices, reverse=True)
