import pytest
import uuid
from beanie import Link
from faker import Faker
# from fastapi import FastAPI, Depends
# from httpx import AsyncClient
# from typing import Optional

# from fastapi_pagination import add_pagination
# from beanie import operators

# from core.fields import S3Path
from core.models import CandidateModel  # , Candidate
# from api.pagination import Page, Params, paginate

fake = Faker()


@pytest.fixture()
def candidate_data():
    return {
        'search_id': uuid.uuid4().hex,
        'searched_at': fake.date_time_this_decade().isoformat(),
        'source': "Facebook",
        'person': str(uuid.uuid4()),
        'profile_photo': "https://i.pravatar.cc/150?img=19",
        'personal_details': {
            'name': {
                'first_name': {
                    "f_name": fake.name()
                },
                'last_name': {
                    'l_name': fake.name()
                },
                'full_name': {
                    'full_name': fake.name()
                }
            },
            'email': {
                'email_address': [fake.email()]
            }
        }
    }


'''
def candidates_data():
    return [
        {
            'name': fake.name(),
            'search_id': uuid.uuid4().hex,
            'searched_at': fake.date_time_this_decade().isoformat(),
            'source': "Facebook",
            'person': str(uuid.uuid4()),
        },
        {
            'name': fake.name(),
            'search_id': uuid.uuid4().hex,
            'searched_at': fake.date_time_this_decade().isoformat(),
            'source': "Facebook",
            'person': str(uuid.uuid4()),
        },
    ]
'''

# To include test run in async mode use @pytest.mark.anyio decorator


@pytest.mark.anyio
class TestCandidateModel:

    # @pytest.mark.order() allow you to choose test priority.
    # Remember each test isolated in its own run
    @pytest.mark.order(1)
    async def test_actions_insert(self, candidate_data):
        candidate = CandidateModel(**candidate_data)
        await candidate.insert()
        assert candidate.personal_details.name.first_name.f_name == (
            candidate_data.get('personal_details').get(
                'name').get('first_name').get('f_name'))
        assert isinstance(candidate.person, Link)

    @pytest.mark.order(2)
    async def test_actions_delete(self, candidate_data):
        candidate = CandidateModel(**candidate_data)
        await candidate.insert()
        await candidate.delete()
