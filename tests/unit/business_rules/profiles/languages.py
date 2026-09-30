# flake8: noqa
import pytest
import pendulum


@pytest.fixture
def hebrew_native_speaker():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "fb_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "Native",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "Fluent",
                    },
                    {
                        "language_id": "bg",
                        "language": "Bulgarian",
                        "proficiency": "Fluent",
                    }
                ],
                "li_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "Professional or bilingual proficiency",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "Full professional proficiency",
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "Professional working proficiency",
                    }
                ]
            },
        }
    }


@pytest.fixture
def profile_with_linkedin_high_proficiency_languages():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "li_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "Native or bilingual proficiency",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "Full professional proficiency",
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "Professional working proficiency",
                    }
                ]
            },
        }
    }


@pytest.fixture
def profile_with_linkedin_2_high_proficiency_languages_1_low():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "li_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "Native or bilingual proficiency",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "Full professional proficiency",
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "limited proficiency",
                    }
                ]
            },
        }
    }


@pytest.fixture
def profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "li_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "Native or bilingual proficiency",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": None,
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "limited proficiency",
                    }
                ]
            },
        }
    }


@ pytest.fixture
def profile_with_xing_high_proficiency_languages():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "xing_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "first language",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "good",
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "fluent",
                    }
                ]
            },
        }
    }


@ pytest.fixture
def profile_with_xing_high_2_proficiency_languages_1_low():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "xing_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "first language",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": "good",
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "fair",
                    }
                ]
            },
        }
    }


@ pytest.fixture
def profile_with_xing_1_high_proficiency_language_1_low_1_no_prof():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "languages": {
                "xing_languages": [
                    {
                        "language_id": "he",
                        "language": "Hebrew",
                        "proficiency": "first language",
                    },
                    {
                        "language_id": "en",
                        "language": "English",
                        "proficiency": None,
                    },
                    {
                        "language_id": "es",
                        "language": "Spanish",
                        "proficiency": "fair",
                    }
                ]
            },
        }
    }
