import pytest


@pytest.fixture
def profile_with_criminal_records_eumw():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            'additional_details': {
                'eumw_details': {
                    'is_dangerous': True,
                    'ehtnic_origin': "African",
                    'date_published': "on September 27, 2022, last modified on February 2, 2023",  # noqa
                    'is_reward': True,
                    'crime': "Trafficking in human beings",
                    'info': "Unstructured info paragraph",
                }
            }
        }
    }


@pytest.fixture
def profile_with_criminal_records_interpol():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            'additional_details': {
                'interpol_details': {
                    'interpol_entity_id': '12345',
                    'arrest_warrants': [
                        {
                            'charge': "Fraud",
                            'issuing_country': "France",
                            'charge_translation': "Translation of charge"
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_without_criminal_records():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            'additional_details': {
                'eumw_details': None,
                'interpol_details': None,
            }
        }
    }
