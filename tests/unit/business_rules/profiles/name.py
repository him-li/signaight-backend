import pytest


@pytest.fixture
def profile_with_full_name():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
        }
    }


@pytest.fixture
def profile_without_full_name():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "Johnatan"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": None},
            },
        }
    }


@pytest.fixture
def profile_without_name():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": None},
                "last_name": {"l_name": None},
                "full_name": {"full_name": None},
            },
        }
    }
