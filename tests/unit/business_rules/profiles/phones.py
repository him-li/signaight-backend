import pytest


@pytest.fixture
def grayfox_with_phones_and_partially_data():
    return {
        "metadata": {
            "email": "anitaphome@yahoo.com",
            "fullname": "Anita Porter",
            "phone": "+1-507-398-7667",
            "username": "5072880549",
        },
        "partial_recovery": [
            {"source": "microsoft", "type": "phone", "value": "********49"}
        ],
        "phones": [
            {
                "name": "Anita Porter",
                "phone_number": "+15073987667",
                "source": "consumers",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+5073987667",
                "source": "verifications",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+15073989876",
                "source": "linkedin scrape 2021",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+15073987667",
                "source": "linkedin scrape 2021",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+17736756947",
                "source": "linkedin scrape 2021",
            },
            {
                "name": "Anita M Porter",
                "phone_number": "+15072880549",
                "source": "apollo.io",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+5072880549",
                "source": "luxottica",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+15073987667",
                "source": "data enrichment exposure from pdl customer",
            },
            {
                "name": "Anita Porter",
                "phone_number": "+5073989876",
                "source": "data enrichment exposure from pdl customer",
            },
        ],
    }
    
@pytest.fixture
def grayfox_without_phones_and_partially_data():
    return {
        "metadata": {
            "email": "anitaphome@yahoo.com",
            "fullname": "Anita Porter",
            "phone": "+1-507-398-7667",
            "username": "5072880549",
        },
        "partial_recovery": [],
        "phones": [],
    }


@pytest.fixture
def grayfox_without_metadata_phones():
    return {
        "metadata": {
            "email": "gensierra78@gmail.com",
            "fullname": "Genevieve  Sierra ",
            "phone": "+7869106068",
            "username": "gensierra78@gmail.com",
        },
        "partial_recovery": [
            {"source": "apple", "type": "phone", "value": "(***) ***-**68"},
            {"source": "microsoft", "type": "phone", "value": "********68"},
        ],
        "phones": [
            {
                "name": "Gen Sierra",
                "phone_number": "+7869106068",
                "source": "modern business solutions",
            },
            {
                "name": "Gen Sierra",
                "phone_number": "+7869106075",
                "source": "modern business solutions",
            }
        ],
    }
