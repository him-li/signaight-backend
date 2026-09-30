import pytest
from pydantic import ValidationError
from core.models.email import Email


def test_valid_email_data():
    valid_data = {
        "email_address": ["user1@example.com", "user2@example.org"],
        "fb_email_address": "facebook_user@example.com",
        "linkedin_email_address": "linkedin_user@example.com",
        "xing_business_email": "business@example.com",
        "xing_private_email": "private@example.com",
        "apple_email": "apple_user@example.com",
    }

    email_model = Email(**valid_data)

    assert email_model.fb_email_address == "facebook_user@example.com"
    assert "user1@example.com" in email_model.email_address
    assert isinstance(email_model.email_address, list)


@pytest.mark.xfail
def test_invalid_email_in_list():
    invalid_data = {
        "email_address": ["user1@example.com", "not-an-email"]
    }

    with pytest.raises(ValidationError) as exc_info:
        Email(**invalid_data)

    assert "1 validation error" in str(exc_info.value)
    assert "value is not a valid email address" in str(exc_info.value)


@pytest.mark.xfail
def test_invalid_single_email_field():
    invalid_data = {
        "fb_email_address": "not-an-email"
    }

    with pytest.raises(ValidationError) as exc_info:
        Email(**invalid_data)

    assert "fb_email_address" in str(exc_info.value)
    assert "value is not a valid email address" in str(exc_info.value)


def test_partial_email_fields_are_ignored():
    # These should not raise validation errors since they're just strings
    partial_data = {
        "fb_email_part": ["justname", "nodomain"],
        "paypal_email_part": ["paypaluser"]
    }

    email_model = Email(**partial_data)

    assert email_model.fb_email_part == ["justname", "nodomain"]
    assert email_model.paypal_email_part == ["paypaluser"]
