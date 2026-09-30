import pytest
import random
from uuid import uuid4


@pytest.fixture
def source():
    return "facebook"


@pytest.fixture
def resource():
    return "vetric"


@pytest.fixture
def candidate(fake, source, resource):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    candidate = {
        'search_id': uuid4().hex,
        'searched_at': fake.date_time_this_decade().isoformat(),
        'source': source,
        'resource': resource,
        'primary': True,
        'profile_photo': "https://i.pravatar.cc/150?img={}".format(
            random.randint(1, 70)),
        'personal_details': {
            'name': {
                'first_name': {
                    'f_name': first_name,
                    f'{source}_f_name': first_name
                },
                'last_name': {
                    'l_name': last_name,
                    f'{source}_l_name': last_name
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
    return candidate


@pytest.fixture
def candidates(fake, source, resource):
    candidates = []
    for num in range(1, 4):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        candidates.append({
            'search_id': uuid4().hex,
            'searched_at': fake.date_time_this_decade().isoformat(),
            'source': source,
            'resource': resource,
            'profile_photo': "https://i.pravatar.cc/150?img={}".format(
                random.randint(1, 70)),
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
    return candidates
