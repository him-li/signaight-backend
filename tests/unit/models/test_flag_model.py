import pytest
import uuid
from beanie import Link
from faker import Faker

from core.models import FlagModel, Flag

fake = Faker()


@pytest.fixture()
def flag_data():
    return {
        "watchlist_countries": {
            "category": "str",
            "severity": 1.1,
            "sub_categories": []
        },
        "person": uuid.uuid4()
    }


# To include test run in async mode use @pytest.mark.anyio decorator


@pytest.mark.anyio
class TestFlagModel:

    # @pytest.mark.order() allow you to choose test priority.
    # Remember each test isolated in its own run
    @pytest.mark.order(1)
    async def test_actions_insert(self, flag_data):
        flag = FlagModel(**flag_data)
        await flag.insert()
        assert isinstance(flag.watchlist_countries, Flag)
        assert isinstance(flag.person, Link)

    @pytest.mark.order(2)
    async def test_actions_delete(self, flag_data):
        flag = FlagModel(**flag_data)
        await flag.insert()
        await flag.delete()
