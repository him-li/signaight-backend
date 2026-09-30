import pytest


@pytest.fixture
def alerts():
    alerts = {
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
        }
    }
    return alerts
