from playwright.sync_api import expect
import pytest


@pytest.mark.assignment2
def test_tc_01_search_button_and_enter_return_same_products(navigation, test_data):
    search_word = test_data["search"]["matching_word"]
    home_page = navigation.open_home()
    all_products = home_page.get_all_products()

    home_page.search(search_word)
    expect(home_page.product_list.get_search_result_count()).to_contain_text(search_word)
    button_results = home_page.get_all_products()

    home_page.clear_search()
    home_page.search(search_word, use_enter=True)
    expect(home_page.product_list.get_search_result_count()).to_contain_text(search_word)
    enter_results = home_page.get_all_products()

    assert 0 < len(button_results) < len(all_products)
    assert sorted(button_results) == sorted(enter_results)


@pytest.mark.assignment2
def test_tc_02_new_search_replaces_previous_results(navigation, test_data):
    first_word = test_data["search"]["matching_word"]
    second_word = test_data["search"]["second_matching_word"]
    home_page = navigation.open_home()

    home_page.search(first_word)
    first_results = home_page.get_all_products()
    home_page.search(second_word, use_enter=True)
    expect(home_page.product_list.get_search_result_count()).to_contain_text(second_word)
    second_results = home_page.get_all_products()

    assert len(second_results) > 0
    assert sorted(second_results) != sorted(first_results)
    assert all(second_word in product.name.lower() for product in second_results)


@pytest.mark.assignment2
def test_tc_03_unmatched_search_shows_no_products(navigation, test_data):
    home_page = navigation.open_home()

    home_page.search(test_data["search"]["unmatched_word"])

    expect(home_page.product_list.get_no_results_message()).to_contain_text("no products found")
    expect(home_page.product_list.get_product_cards()).to_have_count(0)


@pytest.mark.assignment2
def test_tc_04_clearing_a_search_restores_all_products(navigation, test_data):
    home_page = navigation.open_home()
    all_products = home_page.get_all_products()

    home_page.search(test_data["search"]["matching_word"])
    matching_products = home_page.get_all_products()
    assert 0 < len(matching_products) < len(all_products)

    home_page.clear_search()

    expect(home_page.sidebar.get_search_input()).to_have_value("")
    expect(home_page.product_list.get_search_result_count()).to_have_count(0)
    assert home_page.get_all_products() == all_products


@pytest.mark.assignment2
def test_tc_04b_clearing_a_search_returns_on_last_active_page(navigation, test_data):
    home_page = navigation.open_home()
    home_page.product_list.go_to_next_page()
    home_page.product_list.go_to_next_page()

    # expected active page number is page 3
    last_active_page = home_page.product_list.get_active_page_number()

    home_page.search(test_data["search"]["matching_word"])
    home_page.clear_search()

    expect(home_page.product_list.get_active_page()).to_have_text(last_active_page)


@pytest.mark.assignment2
def test_tc_05_clearing_an_unmatched_search_restores_all_products(navigation, test_data):
    home_page = navigation.open_home()
    all_products = home_page.get_all_products()

    home_page.search(test_data["search"]["unmatched_word"])
    expect(home_page.product_list.get_product_cards()).to_have_count(0)

    home_page.clear_search()

    expect(home_page.sidebar.get_search_input()).to_have_value("")
    expect(home_page.product_list.get_no_results_message()).to_have_count(0)
    assert home_page.get_all_products() == all_products
