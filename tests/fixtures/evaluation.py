import pytest


@pytest.fixture
def evaluation():
    evaluation = {
        "resilience": {
            "title": ["str"],
            "score": 10
        },
        "flexibility": {
            "title": ["str"],
            "score": 10
        },
        "work_under_pressure": {
            "title": ["str"],
            "score": 10
        },
        "curiosity": {
            "title": ["str"],
            "score": 10
        },
        "decision_making": {
            "title": ["str"],
            "score": 10
        },
        "courage": {
            "title": ["str"],
            "score": 10
        },
        "teamwork": {
            "title": ["str"],
            "score": 10
        },
        "moral_values": {
            "title": ["str"],
            "score": 10
        },
        "language_skills": {
            "title": ["str"],
            "score": 10
        },
        "interpersonal_skills": {
            "title": ["str"],
            "score": 10
        }
    }
    return evaluation
