from decimal import Decimal

from playwright.sync_api import expect

from components.header_component import HeaderComponent


def money(text):
    return Decimal(text.strip().replace("$", "").replace(",", ""))


def add_named_product(navigation, name):
    products = navigation.open_home()
    products.search(name)
    details = products.open_product(name)
    expect(details.get_add_to_cart_button()).to_be_enabled()
    unit_price = money(details.get_unit_price_text())
    details.add_to_cart()
    return unit_price


def test_tc_09_typed_product_quantity_appears_in_cart(navigation, page):
    products = navigation.open_home()
    products.search("Hammer")
    details = products.open_product("Hammer")
    expect(details.get_add_to_cart_button()).to_be_enabled()
    details.set_quantity(3)
    details.add_to_cart()
    expect(HeaderComponent(page).get_cart_count()).to_have_text("3")

    cart = navigation.open_cart()
    expect(cart.get_quantity_input("Hammer")).to_have_value("3")


def test_tc_11_update_one_of_two_non_eco_cart_lines(navigation, page):
    first_price = add_named_product(navigation, "Hammer")
    expect(HeaderComponent(page).get_cart_count()).to_have_text("1")
    second_price = add_named_product(navigation, "Combination Pliers")
    expect(HeaderComponent(page).get_cart_count()).to_have_text("2")

    cart = navigation.open_cart()
    expect(cart.get_cart_items()).to_have_count(2)
    cart.set_quantity("Hammer", 2)

    expect(cart.get_quantity_input("Hammer")).to_have_value("2")
    expect(cart.get_quantity_input("Combination Pliers")).to_have_value("1")
    expect(cart.get_line_price("Hammer")).to_have_text(f"${first_price * 2:.2f}")
    expect(cart.get_line_price("Combination Pliers")).to_have_text(f"${second_price:.2f}")
    expect(cart.get_cart_total()).to_have_text(f"${first_price * 2 + second_price:.2f}")
    expect(HeaderComponent(page).get_cart_count()).to_have_text("3")
