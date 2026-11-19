import re

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize("field", ["first-name", "last-name", "email", "subject", "message"])
def test_tc_16_empty_form_shows_error_for_each_field(navigation, field):
    contact = navigation.open_contact()
    contact.submit_incomplete()
    expect(contact.error(field)).to_be_visible()
    expect(contact.error(field)).to_contain_text(re.compile("required", re.IGNORECASE))
    field_box = contact.field(field).bounding_box()
    error_box = contact.error(field).bounding_box()
    assert field_box is not None and error_box is not None
    assert error_box["y"] >= field_box["y"] + field_box["height"]
    assert not contact.blocked_posts


def test_tc_17_contact_values_are_retained_without_sending(navigation):
    contact = navigation.open_contact()
    contact.fill_contact("Alex", "alex@example.com", "A sample message for this form.")
    contact.field("last-name").fill("Tester")
    contact.field("subject").select_option(label="Customer service")
    contact.field("first-name").focus()

    expect(contact.field("first-name")).to_have_value("Alex")
    expect(contact.field("last-name")).to_have_value("Tester")
    expect(contact.field("email")).to_have_value("alex@example.com")
    expect(contact.field("subject")).to_have_value("customer-service")
    expect(contact.field("message")).to_have_value("A sample message for this form.")


def test_tc_18_values_remain_after_incomplete_form_validation(navigation):
    contact = navigation.open_contact()
    contact.fill_contact("Alex", "alex@example.com", "A sample message for this form.")
    contact.submit_incomplete()

    expect(contact.field("first-name")).to_have_value("Alex")
    expect(contact.field("email")).to_have_value("alex@example.com")
    expect(contact.field("message")).to_have_value("A sample message for this form.")
    expect(contact.error("last-name")).to_be_visible()
    expect(contact.error("subject")).to_be_visible()
    assert not contact.blocked_posts
