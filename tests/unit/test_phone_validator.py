from core.models.phone import Phone


def test_valid_multiple_phones_in_model():
    phone_data = {
        "phones": ["+14155552671", "+447911123456"],
        "fb_phone": "+4915123456789",
        "linkedin_phone_numbers": ["+33612345678", "+39061234567"],
    }
    phone_model = Phone(**phone_data)
    assert phone_model.phones[0] == "+14155552671"
    assert phone_model.fb_phone == "+4915123456789"
    assert phone_model.linkedin_phone_numbers[1] == "+39061234567"


def test_fb_phones_accepts_list():
    phone_data = {
        "fb_phones": ["+14155552671", "+14844760263"]
    }
    phone_model = Phone(**phone_data)
    assert len(phone_model.fb_phones) == 2
    assert phone_model.fb_phones[1] == "+14844760263"


def test_fb_phone_accepts_single_and_list():
    single_data = {"fb_phone": "+14155552671"}
    list_data = {"fb_phone": ["+14155552671", "+14844760263"]}

    single_model = Phone(**single_data)
    list_model = Phone(**list_data)

    assert single_model.fb_phone == "+14155552671"
    assert list_model.fb_phone[1] == "+14844760263"
