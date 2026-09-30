import pytest
import uuid
from beanie import Link
from faker import Faker

from core.models import EvaluationModel

fake = Faker()


@pytest.fixture()
def evaluation_data():
    return {
        "resilience": {
            "notes": ["str"],
            "score": 10
        },
        "flexibility": {
            "notes": ["str"],
            "score": 10
        },
        "work_under_pressure": {
            "notes": ["str"],
            "score": 10
        },
        "curiosity": {
            "notes": ["str"],
            "score": 10
        },
        "decision_making": {
            "notes": ["str"],
            "score": 10
        },
        "courage": {
            "notes": ["str"],
            "score": 10
        },
        "teamwork": {
            "notes": ["str"],
            "score": 10
        },
        "moral_values": {
            "notes": ["str"],
            "score": 10
        },
        "language_skills": {
            "notes": ["str"],
            "score": 10
        },
        "interpersonal_skills": {
            "notes": ["str"],
            "score": 10
        },
        "wisdom_common_sense": {
            "notes": ["str"],
            "score": 10
        },
        "person": uuid.uuid4()
    }


# To include test run in async mode use @pytest.mark.anyio decorator
@pytest.mark.anyio
class TestEvaluationModel:

    # @pytest.mark.order() allow you to choose test priority.
    # Remember each test isolated in its own run
    @pytest.mark.order(1)
    async def test_actions_insert(self, evaluation_data):
        evaluation = EvaluationModel(**evaluation_data)
        await evaluation.insert()
        assert evaluation.resilience.score == evaluation_data.get(
            'resilience').get('score')
        assert isinstance(evaluation.person, Link)

    @pytest.mark.order(2)
    async def test_actions_delete(self, evaluation_data):
        evaluation = EvaluationModel(**evaluation_data)
        await evaluation.insert()
        await evaluation.delete()
