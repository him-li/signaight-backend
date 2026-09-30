# flake8: noqa
import pytest


@pytest.fixture
def profile_fb_page_altruism():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "save children"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_no_altruism():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "nothing"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_no_fb_page_name():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_id": "some id"
                }
            ]
        }
    }


@pytest.fixture
def profile_pages_empty():
    return {
        "interests": {
            "pages": [
            ]
        }
    }


@pytest.fixture
def profile_interests_empty():
    return {
        "interests": {
        }
    }


@pytest.fixture
def profile_interests_None():
    return {
        "interests": None
    }


@pytest.fixture
def profile_fb_page_supporting_israel():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "love Israel"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_not_supporting_israel():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "love birds"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_foodie():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "foodie"
                },
                {
                    "fb_page_name": "love food"
                },
                {
                    "fb_page_name": "love cooking and baking"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_not_foodie():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "adventure"
                },
                {
                    "fb_page_name": "love running"
                },
                {
                    "fb_page_name": "love cycling and swimming"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_jihadist():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "طاغوت"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_salafist():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "بدعة"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_jihadist_non_arabic_term():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "Taghut"
                }
            ]
        }
    }


@pytest.fixture
def profile_fb_page_salafist_non_arabic_term():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_name": "Jihad"
                },
                {
                    "fb_page_name": "Jihad"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_designated_group_a():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_id": "100077281504627",
                    "fb_page_name": "Shaykh Ahmad Mūsā Jibrīl NL",
                    "fb_page_url": "https://www.facebook.com/100077281504626"
                },
                {
                    "fb_page_id": "102472642072561",
                    "fb_page_name": "Shaykh Sulaymān bin Nāsir Al-‘Alwān",
                    "fb_page_url": "https://www.facebook.com/ShaykhSulaymanbinNasirAlAlwan"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_designated_group_b():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_id": "96390992174",
                    "fb_page_name": "Muslim Prisoner Support Group",
                    "fb_page_url": "https://www.facebook.com/groups/96390992174"
                },
                {
                    "fb_page_id": "100491549451484",
                    "fb_page_name": "DOAM - Documenting Oppression Against Muslims - Bangla",
                    "fb_page_url": "https://www.facebook.com/DOAMDocumentingOppressionAgainstMuslimsBangla"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_weapon_profile_photo():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_profile_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg"
                },
            ]
        }
    }


@pytest.fixture
def profile_fb_page_weapon_cover_photo():
    return {
        "interests": {
            "pages": [
                {
                    "fb_page_cover_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg"
                },
            ]
        }
    }
