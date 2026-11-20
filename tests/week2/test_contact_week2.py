import re

from playwright.sync_api import expect
import pytest

# Never press Send on a completed contact form: it sends a real message.
# Every test below leaves at least one required field empty before pressing Send.

REQUIRED = re.compile("required", re.IGNORECASE)


@pytest.mark.assignment2
@pytest.mark.parametrize("missing_field", ["first_name", "last_name", "email", "subject", "message"])
def test_tc_15_each_contact_field_is_required(navigation, test_data, missing_field):
    contact_page = navigation.open_contact()

    contact_page.fill_form(test_data["contact"], omit=(missing_field,))
    contact_page.submit_incomplete()

    expect(contact_page.get_error(missing_field)).to_be_visible()
    expect(contact_page.get_error(missing_field)).to_contain_text(REQUIRED)


@pytest.mark.assignment2
@pytest.mark.parametrize("field", ["first_name", "last_name", "email", "subject", "message"])
def test_tc_16_empty_form_shows_message_under_each_field(navigation, field):
    contact_page = navigation.open_contact()

    contact_page.submit_incomplete()

    expect(contact_page.get_error(field)).to_have_count(1)
    expect(contact_page.get_error(field)).to_contain_text(REQUIRED)
    assert contact_page.is_error_below_field(field)


@pytest.mark.assignment2
def test_tc_17_form_keeps_typed_and_chosen_values(navigation, test_data):
    contact = test_data["contact"]
    contact_page = navigation.open_contact()

    contact_page.fill_form(contact)
    contact_page.move_focus_to("first_name")

    for field in ("first_name", "last_name", "email", "message"):
        expect(contact_page.get_field(field)).to_have_value(contact[field])
    expect(contact_page.get_selected_subject()).to_have_text(contact["subject"])


@pytest.mark.assignment2
def test_tc_18_form_keeps_values_after_incomplete_send(navigation, test_data):
    contact = test_data["contact"]
    contact_page = navigation.open_contact()

    contact_page.fill_form(contact, omit=("last_name", "subject"))
    contact_page.submit_incomplete()

    for field in ("first_name", "email", "message"):
        expect(contact_page.get_field(field)).to_have_value(contact[field])
    expect(contact_page.get_error("last_name")).to_be_visible()
    expect(contact_page.get_error("subject")).to_be_visible()
