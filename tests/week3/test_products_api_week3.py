from decimal import Decimal

from playwright.sync_api import expect
import pytest

from utilities.helpers import parse_price


@pytest.mark.assignment3
def test_products_api_returns_valid_products_matching_ui(products_api, navigation):
    response = products_api.get_products()

    assert response.status == 200
    assert "application/json" in response.headers["content-type"]

    body = response.json()
    assert isinstance(body["current_page"], int)
    assert isinstance(body["total"], int)
    assert isinstance(body["data"], list) and body["data"]

    for product in body["data"]:
        assert isinstance(product["id"], str)
        assert isinstance(product["name"], str) and product["name"]
        assert isinstance(product["price"], (int, float)) and not isinstance(product["price"], bool)
        assert isinstance(product["in_stock"], bool)

    api_product = body["data"][0]
    product_details_page = navigation.open_product_by_id(api_product["id"])

    expect(product_details_page.get_product_name()).to_have_text(api_product["name"])
    assert parse_price(product_details_page.get_unit_price_text()) == Decimal(str(api_product["price"]))
