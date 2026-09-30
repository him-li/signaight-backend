import pytest

from core.utils.get_names_list import (
    extract_name,
    get_names_list,
    name_resolution,
)


@pytest.fixture()
def person_with_name(person):
    person["personal_details"] = {
        "name": {
            "verified": False,
            "first_name": {
                "f_name": "Tamar",
                "gravatar_f_name": "tamar",
                "linkedin_f_name": "Tamar",
                "microsoft_f_name": "tamar fruma hirshfeld",
                "yelp_f_name": "Tamar Fruma",
            },
            "last_name": {
                "gravatar_l_name": "gershoni",
                "l_name": "Hirshfeld Gershoni",
                "linkedin_l_name": "Hirshfeld Gershoni",
                "microsoft_l_name": "gershoni",
                "yelp_l_name": "H.",
            },
            "full_name": {"full_name": "Tamar gershoni"},
        },
        "email": {
            "email_address": ['itamara2000@gmail.com']
        }
    }
    person['id'] = 'rundom_id'
    return person


@pytest.mark.anyio
async def test_name_resolution(person_with_name):
    name = await name_resolution(person_with_name)
    assert "Hirshfeld" in name
    assert "Tamar" in name

def test_extract_markdown_name():
    response = "**Test Mutayn**"
    assert extract_name(response) == "Test Mutayn"


def test_extract_plain_name():
    response = "Tamar Test"
    assert extract_name(response) == "Tamar Test"


def test_extract_name_from_sentence():
    response = "The best guess is Tamar Test based on available information."
    assert extract_name(response) == "Tamar Test"


def test_ignore_explanation_text():
    response = (
        'Given the single name variant "None None" and no additional information '
        "from the email, the best choice is None None."
    )
    assert extract_name(response) is None


def test_ignore_none_name():
    response = "None None"
    assert extract_name(response) is None


def test_ignore_empty_string():
    response = ""
    assert extract_name(response) is None


def test_ignore_random_sentence():
    response = "This email does not provide enough information to determine the name."
    assert extract_name(response) is None


def test_extract_three_word_name():
    response = "he best name is Juan Carlos Rodriguez"
    assert extract_name(response) == "Juan Carlos Rodriguez"


def test_extract_name_from_full_name():
    person = {
        "personal_details": {
            "name": {
                "full_name": {
                    "linkedin_full_name": "John Smith"
                }
            }
        },
        "network_signature": {}
    }

    assert get_names_list(person) == ["John Smith"]


def test_extract_name_from_first_last():
    person = {
        "personal_details": {
            "name": {
                "first_name": {"linkedin_first_name": "John"},
                "last_name": {"linkedin_last_name": "Smith"},
            }
        },
        "network_signature": None
    }

    assert get_names_list(person) == ["John Smith"]


def test_extract_from_matched_profiles_full_name():
    person = {
        "personal_details": {"name": {}},
        "network_signature": {
            "matched_profiles": {
                "facebook": {
                    "primary_candidate": {
                        "id1": {
                            "full_name": "Abdulkadir Eidleh",
                            "f_name": None,
                            "l_name": None
                        }
                    }
                }
            }
        }
    }

    assert get_names_list(person) == ["Abdulkadir Eidleh"]


def test_extract_from_matched_profiles_first_last():
    person = {
        "personal_details": {"name": None},
        "network_signature": {
            "matched_profiles": {
                "microsoft": {
                    "primary_candidate": {
                        "id1": {
                            "f_name": "Abdulkadir",
                            "l_name": "Eidleh",
                            "full_name": None
                        }
                    }
                }
            }
        }
    }

    assert get_names_list(person) == ["Abdulkadir Eidleh"]


def test_remove_duplicates():
    person = {
        "personal_details": {
            "name": {
                "full_name": {
                    "linkedin_full_name": "Abdulkadir Eidleh"
                }
            }
        },
        "network_signature": {
            "matched_profiles": {
                "facebook": {
                    "primary_candidate": {
                        "id1": {
                            "full_name": "Abdulkadir Eidleh"
                        }
                    }
                }
            }
        }
    }

    assert get_names_list(person) == ["Abdulkadir Eidleh"]


def test_ignore_none_values():
    person = {
        "personal_details": {
            "name": {
                "full_name": {"linkedin_full_name": None}
            }
        },
        "network_signature": {
            "matched_profiles": {
                "facebook": {
                    "primary_candidate": {
                        "id1": {
                            "full_name": None,
                            "f_name": None,
                            "l_name": None
                        }
                    }
                }
            }
        }
    }

    assert get_names_list(person) == []


def test_ignore_invalid_names():
    person = {
        "personal_details": {
            "name": {
                "full_name": {"linkedin_full_name": "None None"}
            }
        },
        "network_signature": {}
    }

    assert get_names_list(person) == []


def test_multiple_names_sources():
    person = {
        "personal_details": {
            "name": {
                "full_name": {"linkedin_full_name": "John Smith"}
            }
        },
        "network_signature": {
            "matched_profiles": {
                "facebook": {
                    "primary_candidate": {
                        "id1": {"full_name": "John Smith"}
                    }
                },
                "microsoft": {
                    "primary_candidate": {
                        "id2": {"f_name": "John", "l_name": "Smith"}
                    }
                }
            }
        }
    }

    assert get_names_list(person) == ["John Smith"]
    
def test_multiple_names_sources_with_different_names():
    person = {
        "personal_details": {
            "name": {
                "full_name": {"linkedin_full_name": "John Smith"}
            }
        },
        "network_signature": {
            "matched_profiles": {
                "facebook": {
                    "primary_candidate": {
                        "id1": {"full_name": "John Doe"}
                    }
                },
                "microsoft": {
                    "primary_candidate": {
                        "id2": {"f_name": "John", "l_name": "Smith"}
                    }
                }
            }
        }
    }

    assert get_names_list(person) == ["John Doe", "John Smith"]
