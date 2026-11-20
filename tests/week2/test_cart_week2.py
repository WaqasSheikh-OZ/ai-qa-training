from playwright.sync_api import expect
import pytest

from utilities.helpers import format_price, parse_price


@pytest.mark.assignment2
def test_tc_09_typed_quantity_is_shown_in_cart(navigation, test_data):
    product = test_data["products"]["non_eco"]
    quantity = test_data["cart"]["typed_quantity"]

    product_details_page = navigation.open_home().search_and_open_product(product)
    product_details_page.add_to_cart(quantity)
    expect(product_details_page.header.get_cart_count()).to_have_text(str(quantity))

    cart_page = navigation.open_cart()
    expect(cart_page.get_cart_items()).to_have_count(1)
    expect(cart_page.get_quantity_input(product)).to_have_value(str(quantity))


@pytest.mark.assignment2
def test_tc_10_changing_cart_quantity_updates_prices_and_icon(navigation, test_data):
    product = test_data["products"]["non_eco"]
    new_quantity = test_data["cart"]["typed_quantity"]

    product_details_page = navigation.open_home().search_and_open_product(product)
    unit_price = parse_price(product_details_page.get_unit_price_text())
    product_details_page.add_to_cart()
    expect(product_details_page.header.get_cart_count()).to_have_text("1")

    cart_page = navigation.open_cart()
    cart_page.set_quantity(product, new_quantity)

    expect(cart_page.get_quantity_input(product)).to_have_value(str(new_quantity))
    expect(cart_page.get_line_price(product)).to_have_text(format_price(unit_price * new_quantity))
    expect(cart_page.get_cart_total()).to_have_text(format_price(unit_price * new_quantity))
    expect(cart_page.header.get_cart_count()).to_have_text(str(new_quantity))


@pytest.mark.assignment2
def test_tc_11_changing_one_of_two_cart_lines(navigation, test_data):
    first_product = test_data["products"]["non_eco"]
    second_product = test_data["products"]["second_non_eco"]
    new_quantity = test_data["cart"]["updated_quantity"]

    first_details_page = navigation.open_home().search_and_open_product(first_product)
    first_price = parse_price(first_details_page.get_unit_price_text())
    first_details_page.add_to_cart()
    expect(first_details_page.header.get_cart_count()).to_have_text("1")

    second_details_page = navigation.open_home().search_and_open_product(second_product)
    second_price = parse_price(second_details_page.get_unit_price_text())
    second_details_page.add_to_cart()
    expect(second_details_page.header.get_cart_count()).to_have_text("2")

    cart_page = navigation.open_cart()
    expect(cart_page.get_cart_items()).to_have_count(2)
    cart_page.set_quantity(first_product, new_quantity)

    expect(cart_page.get_quantity_input(first_product)).to_have_value(str(new_quantity))
    expect(cart_page.get_quantity_input(second_product)).to_have_value("1")
    expect(cart_page.get_line_price(first_product)).to_have_text(format_price(first_price * new_quantity))
    expect(cart_page.get_line_price(second_product)).to_have_text(format_price(second_price))
    expect(cart_page.get_cart_total()).to_have_text(format_price(first_price * new_quantity + second_price))
    expect(cart_page.header.get_cart_count()).to_have_text(str(new_quantity + 1))


@pytest.mark.assignment2
def test_tc_12_eco_line_price_is_correct_and_total_is_discounted(navigation, test_data):
    product = test_data["products"]["eco"]
    quantity = test_data["cart"]["eco_quantity"]

    home_page = navigation.open_home()
    home_page.search(product)
    expect(home_page.product_list.get_eco_badge(product)).to_be_visible()
    product_details_page = home_page.open_product(product)
    unit_price = parse_price(product_details_page.get_unit_price_text())
    product_details_page.add_to_cart(quantity)
    expect(product_details_page.header.get_cart_count()).to_have_text(str(quantity))

    cart_page = navigation.open_cart()
    expected_line_price = unit_price * quantity

    expect(cart_page.get_line_price(product)).to_have_text(format_price(expected_line_price))
    assert parse_price(cart_page.get_cart_total_text()) < expected_line_price


@pytest.mark.assignment2
def test_tc_13_removing_the_last_item_shows_empty_cart(navigation, test_data):
    product = test_data["products"]["non_eco"]

    product_details_page = navigation.open_home().search_and_open_product(product)
    product_details_page.add_to_cart()
    expect(product_details_page.header.get_cart_count()).to_have_text("1")

    cart_page = navigation.open_cart()
    cart_page.remove_item(product)

    expect(cart_page.get_cart_items()).to_have_count(0)
    expect(cart_page.get_empty_message()).to_be_visible()


@pytest.mark.assignment2
def test_tc_14_removing_one_item_keeps_the_other(navigation, test_data):
    removed_product = test_data["products"]["non_eco"]
    kept_product = test_data["products"]["second_non_eco"]

    removed_details_page = navigation.open_home().search_and_open_product(removed_product)
    removed_details_page.add_to_cart()
    expect(removed_details_page.header.get_cart_count()).to_have_text("1")

    kept_details_page = navigation.open_home().search_and_open_product(kept_product)
    kept_price = parse_price(kept_details_page.get_unit_price_text())
    kept_details_page.add_to_cart()
    expect(kept_details_page.header.get_cart_count()).to_have_text("2")

    cart_page = navigation.open_cart()
    cart_page.remove_item(removed_product)

    expect(cart_page.get_cart_items()).to_have_count(1)
    expect(cart_page.get_product_title(kept_product)).to_be_visible()
    expect(cart_page.get_quantity_input(kept_product)).to_have_value("1")
    expect(cart_page.get_line_price(kept_product)).to_have_text(format_price(kept_price))


@pytest.mark.assignment2
def test_tc_19_out_of_stock_product_cannot_be_added(navigation, test_data):
    product_details_page = navigation.open_home().search_and_open_product(
        test_data["products"]["out_of_stock"]
    )

    expect(product_details_page.get_add_to_cart_button()).to_be_disabled()
    expect(product_details_page.header.get_cart_icon()).to_have_count(0)
