import pytest
import uuid


@pytest.fixture
def editor(fake):
    return {
        'id': uuid.uuid4(),
        'email': fake.email(),
        'firstname': fake.first_name(),
        'lastname': fake.last_name()
    }


@pytest.fixture
def person(fake):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    return {
        'personal_details': {
            'name': {
                'first_name': {
                    'f_name': first_name,
                },
                'last_name': {
                    'l_name': last_name
                },
                'full_name': {
                    'full_name': f'{first_name} {last_name}',
                }
            },
            'email': {
                'email_address': [email]
            }
        }
    }


@pytest.fixture
def persons(fake):
    persons = []
    for num in range(1, 10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        persons.append({
            'personal_details': {
                'name': {
                    'first_name': {
                        'f_name': first_name,
                    },
                    'last_name': {
                        'l_name': last_name
                    },
                    'full_name': {
                        'full_name': f'{first_name} {last_name}',
                    }
                },
                'email': {
                    'email_address': [email]
                }
            }
        })
    return persons


@pytest.fixture
def nodes_links():
    return {
        "config": {
            # nodeId
            'node_id': 'ident',
            'node_label': 'name',
            'node_val': 'value',
            'link_source': 'source',
            'link_target': 'target',
            'link_label': 'name',
        },
        "nodes": [
            {
                "ident": "richard-lee-jones-user",
                "name": "Richard Lee Jones",
                "value": "Richard Lee Jones",
                "icon": "user"
            },
            {
                "ident": "bristol,-uk-hometown",
                "name": "Bristol, UK",
                "value": "Bristol, UK",
                "icon": "hometown"
            }
        ],
        "links": [
            {
                "source": "richard-lee-jones-user",
                "target": "bristol,-uk-hometown",
                "name": "Lives in"
            },
            {
                "source": "person",
                "target": "social",
                "name": "Mentioned"
            }
        ]
    }


@pytest.fixture
def locations():
    return {
        "location": "Seoul",
        "hometown": {
            "fb_hometown": "Boston"
        },
        "instagram_location_name": "Taiwan",
        "check_ins": {
            "fb_check_ins": ["San Diego"]
        }
    }


@pytest.fixture
def description_bio_intro():
    return {
        "biographic_details": {
            "verified": False,
            "description_bio_intro": {
                "verified": False,
                "introduction": "Real estate agent",
                "linkedin_headline": None,
                "instagram_bio": None,
                "biography_with_entities": None,
                "instagram_bio_links": None,
                "instagram_fb_link_on_profile": None,
            },
            "volunteer_experience": None,
            "marital_status_relatives": None,
            "education": None,
            "work": None,
        }
    }

