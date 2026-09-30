import pytest
import uuid
from beanie import Link
from faker import Faker

from core.models import AlertsModel

fake = Faker()


@pytest.fixture()
def alerts_data():
    return {
        "strong_affinity_with_israel": {
            "heuristics": [{
                "title": "str",
                "description": "str",
                "score": 10
            }],
            "score": 10
        },
        "occupational_instability": {
            "heuristics": [{
                "title": "str",
                "description": "str",
                "score": 10
            }],
            "score": 10
        },
        "person": uuid.uuid4()
    }


# To include test run in async mode use @pytest.mark.anyio decorator


@pytest.mark.anyio
class TestAlertsModel:

    # @pytest.mark.order() allow you to choose test priority.
    # Remember each test isolated in its own run
    @pytest.mark.order(1)
    async def test_actions_insert(self, alerts_data):
        alerts = AlertsModel(**alerts_data)
        await alerts.insert()
        assert alerts.strong_affinity_with_israel.score == alerts_data.get(
            'strong_affinity_with_israel').get('score')
        assert isinstance(alerts.person, Link)

    @pytest.mark.order(2)
    async def test_actions_delete(self, alerts_data):
        alerts = AlertsModel(**alerts_data)
        await alerts.insert()
        await alerts.delete()
