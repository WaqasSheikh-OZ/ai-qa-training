from playwright.sync_api import expect


def test_tc_01_search_button_and_enter_return_same_products(navigation):
    products = navigation.open_home()
    full_list = products.get_all_products()
    expected = {href for href, name, _ in full_list if "hammer" in name.lower()}
    assert 1 < len(expected) < len(full_list)

    products.search("hammer")
    button_results = {href for href, _, _ in products.get_all_products()}
    assert button_results == expected

    products.clear_search()
    products.search("hammer", use_enter=True)
    enter_results = {href for href, _, _ in products.get_all_products()}
    assert enter_results == expected
    assert enter_results == button_results


def test_tc_03_unmatched_search_shows_no_products(navigation):
    products = navigation.open_home()
    products.search("zzzzqwerty-no-such-product")
    expect(products.get_product_cards()).to_have_count(0)
    expect(products.page.locator('[data-test="no-results"]')).to_contain_text(
        "no products"
    )
