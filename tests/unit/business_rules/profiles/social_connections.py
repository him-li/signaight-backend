# flake8: noqa
import pytest


@pytest.fixture
def two_fb_friends():
    return {
        "connections": {
            "friends": {
                "facebook": [
                    {
                        "facebook_user_id": "123456789",
                        "facebook_full_name": "John Doe"
                    },
                    {
                        "facebook_user_id": "987654321",
                        "facebook_full_name": "Jane Doe"
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_following_fb_page_designated_group_a():
    return {
        "connections": {
            "following": {
                "facebook": [
                    {
                        "facebook_user_id": "100077281504626",
                        "facebook_full_name": "Shaykh Ahmad Mūsā Jibrīl NL"
                    },
                    {
                        "facebook_user_id": "102472642072561",
                        "facebook_full_name": "Shaykh Sulaymān bin Nāsir Al-‘Alwān"
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_following_fb_page_designated_group_b():
    return {
        "connections": {
            "following": {
                "facebook": [
                    {
                        "facebook_user_id": "96390992174",
                        "facebook_full_name": "Muslim Prisoner Support Group"
                    },
                    {
                        "facebook_user_id": "100491549451484",
                        "facebook_full_name": "DOAM - Documenting Oppression Against Muslims - Bangla"
                    },
                ]
            },
        }
    }
