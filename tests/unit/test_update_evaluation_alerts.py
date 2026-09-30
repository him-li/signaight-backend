import pytest
from core.rules.person.utils import (
    update_evaluation_factors, update_heuristics_score)
from core.models import EvaluationModel, AlertsModel, PersonModel
from core.models.evaluation import EvaluationFactor


def test_update_evaluation_factors_dict_decreasing_score():
    self_key = {
        "factors": [
            {"title": "Factor 1", "score": 10,
             "description": "some description"},
            {"title": "Factor 2", "score": 20,
             "description": "some description"}
        ],
        "score": 20
    }
    factor = {"title": "Factor 1", "score": 15}

    updated_key = update_evaluation_factors(self_key, factor)

    assert (updated_key.factors == [
        EvaluationFactor(**{"title": "Factor 2", "score": 20,
                         "description": "some description"}),
        EvaluationFactor(**{"title": "Factor 1", "score": 15,
                         "description": "some description"})
    ])
    assert updated_key.score == 20


def test_update_evaluation_factors_dict_increasing_score():
    self_key = {
        "factors": [
            {"title": "Factor 1", "score": 10,
             "description": "some description"},
            {"title": "Factor 2", "score": 20,
             "description": "some description"}
        ],
        "score": 20
    }
    factor = {"title": "Factor 1", "score": 30,
              "description": "some description"}

    updated_key = update_evaluation_factors(self_key, factor)

    assert (updated_key.factors == [
        EvaluationFactor(**{"title": "Factor 2", "score": 20,
                         "description": "some description"}),
        EvaluationFactor(**{"title": "Factor 1", "score": 30,
                         "description": "some description"})
    ])
    assert updated_key.score == 30


def test_update_evaluation_factors_dict_increasing_score_add_factor():
    self_key = {
        "factors": [
            {"title": "Factor 1", "score": 10,
             "description": "some description"},
            {"title": "Factor 2", "score": 20,
             "description": "some description"}
        ],
        "score": 20
    }
    factor = {"title": "Factor 3", "score": 30}

    updated_key = update_evaluation_factors(self_key, factor)

    assert (updated_key.factors == [
        EvaluationFactor(**{"title": "Factor 1", "score": 10,
                         "description": "some description"}),
        EvaluationFactor(**{"title": "Factor 2", "score": 20,
                         "description": "some description"}),
        EvaluationFactor(**{"title": "Factor 3", "score": 30,
                         "description": "some description"}),
    ])
    assert updated_key.score == 30


@pytest.mark.anyio
async def test_update_evaluation_factors_object(person,  editor):
    factor_1 = {"title": "Factor 1", "score": 10,
                "description": "some description"}
    factor_2 = {"title": "Factor 2", "score": 20,
                "description": "some description"}

    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()

    evaluation = EvaluationModel(person=person)
    evaluation.courage = update_evaluation_factors(
        evaluation.courage, factor_1)
    await evaluation.insert()

    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    evaluation.courage = update_evaluation_factors(
        evaluation.courage, factor_2)
    await evaluation.save()

    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage.score == 20
    assert len(evaluation.courage.factors) == 2

    factor_1_update = {"title": "Factor 1", "score": 5}
    evaluation.courage = update_evaluation_factors(
        evaluation.courage, factor_1_update)
    await evaluation.save()

    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage.score == 20
    assert len(evaluation.courage.factors) == 2


def test_update_heuristics_score_dict_decreasing_score():

    heuristic = {
        "heuristics": [{
            "title": ("Criminal Records"),
            "description": ("has criminal records"),
            "score": 20
        }],

    }
    update = {"title": "Factor 1", "score": 15,
              "description": "some description"}
    updated_key = update_heuristics_score(heuristic, update)

    assert updated_key.score == 20
    assert len(updated_key.heuristics) == 2


def test_update_heuristics_score_dict_increasing_score():

    heuristic = {
        "heuristics": [{
            "title": ("Criminal Records"),
            "description": ("has criminal records"),
            "score": 20
        }],

    }
    update = {"title": "Factor 1", "score": 25,
              "description": "some description"}
    updated_key = update_heuristics_score(heuristic, update)

    assert updated_key.score == 25
    assert len(updated_key.heuristics) == 2


def test_update_heuristics_score_dict_initial_score():

    heuristic = {}
    update = {"title": "Factor 1", "score": 25,
              "description": "some description"}
    updated_key = update_heuristics_score(heuristic, update)

    assert updated_key.score == 25
    assert len(updated_key.heuristics) == 1


@pytest.mark.anyio
async def test_update_heuristics_score_object(person,  editor):
    heuristic_1 = {"title": ("Heuristic 1"),
                   "description": ("Heuristic 1 desc"),
                   "score": 20}
    heuristic_2 = {"title": "Heuristic 2",
                   "description": ("Heuristic 2 desc"),
                   "score": 10}

    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()

    alert = AlertsModel(person=person)
    alert.criminal_records = update_heuristics_score(
        alert.criminal_records, heuristic_1)
    await alert.insert()

    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)

    alert.criminal_records = update_heuristics_score(
        alert.criminal_records, heuristic_2)
    await alert.save()

    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records.score == 20
    assert len(alert.criminal_records.heuristics) == 2

    heuristic_1_update = {"title": ("Heuristic 1"),
                          "description": ("Heuristic 1 update desc"),
                          "score": 30}
    alert.criminal_records = update_heuristics_score(
        alert.criminal_records, heuristic_1_update)
    await alert.save()

    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records.score == 30
    assert len(alert.criminal_records.heuristics) == 2
