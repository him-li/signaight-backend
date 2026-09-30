# flake8: noqa
import pytest


@pytest.fixture
def profile_with_goodreads_duolingo_user_id():
    return {
        "network_signature": {
            "user_id": {
                "goodreads_user_id": ["12345678"],
                "duolingo_user_id": ["12345678"]
            }
        }
    }


@pytest.fixture
def profile_with_goodreads_duolingo_matched_profiles():
    return {
        "network_signature": {
            "matched_profiles": {
                "goodreads": {"primary_candidate": {"12345678": {}}},
                "duolingo": {"primary_candidate": {"12345678": {}}},
            }
        }
    }


@pytest.fixture
def profile_with_goodreads_duolingo_url():
    return {
        "network_signature": {
            "url": {
                "duolingo_profile_url": ["http://.../"],
                "goodreads_profile_url": ["http://.../"]
            }
        }
    }


@pytest.fixture
def profile_with_goodreads_duolingo():
    return {
        "network_signature": {
            "user_id": {
                "goodreads_user_id": ["12345678"],
                "duolingo_user_id": ["12345678"]
            },
            "matched_profiles": {
                "goodreads": {"primary_candidate": {"12345678": {}}},
                "duolingo": {"primary_candidate": {"12345678": {}}},
            },
            "url": {
                "duolingo_profile_url": ["http://.../"],
                "goodreads_profile_url": ["http://.../"]
            }
        }
    }


@pytest.fixture
def profile_with_facebook_instagram():
    return {
        "network_signature": {
            "user_id": {
                "facebook_user_id": ["12345678"],
                "instagram_user_id": ["12345678"]
            },
            "matched_profiles": {
                "facebook": {"primary_candidate": {"12345678": {}}},
                "instagram": {"primary_candidate": {"12345678": {}}},
            },
            "url": {
                "facebook_profile_url": ["http://.../"],
                "instagram_profile_url": ["http://.../"]
            }
        }
    }


@pytest.fixture
def profile_with_eumw_matched_profiles():
    return {
        "network_signature": {
            "matched_profiles": {
                "eumw": {"primary_candidate": {"12345678": {}}},
            },
        }
    }


@pytest.fixture
def profile_with_interpol_matched_profiles():
    return {
        "network_signature": {
            "matched_profiles": {
                "interpol": {"primary_candidate": {"12345678": {}}},
            },
        }
    }


@pytest.fixture
def profile_with_interpol_eumw_matched_profiles():
    return {
        "network_signature": {
            "matched_profiles": {
                "interpol": {"primary_candidate": {"12345678": {}}},
                "eumw": {"primary_candidate": {"12345678": {}}},
            },
        }
    }
