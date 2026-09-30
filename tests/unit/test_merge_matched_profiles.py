from core.utils.reassign_candidates_to_merged_person import merge_matched_profiles
from types import SimpleNamespace


class MockProfiles:
    def __init__(self, data):
        self.data = data

    def model_dump(self):
        return self.data


def person(profiles):
    return SimpleNamespace(
        network_signature=SimpleNamespace(
            matched_profiles=MockProfiles(profiles)
        )
    )


def test_merge_two_persons_same_platform():

    p1 = person({
        "facebook": {
            "candidates_count": 2,
            "primary_candidate": {
                "id1": {"full_name": "John"}
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 3,
            "primary_candidate": {
                "id2": {"full_name": "Mike"}
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    assert result["facebook"]["candidates_count"] == 5
    assert "id1" in result["facebook"]["primary_candidate"]
    assert "id2" in result["facebook"]["primary_candidate"]


def test_merge_multiple_platforms():

    p1 = person(
        {
            "facebook": {
                "candidates_count": 1,
                "primary_candidate": {"id1": {"profile_id": "1518788703"}},
            }
        }
    )

    p2 = person(
        {
            "instagram": {
                "candidates_count": 2,
                "primary_candidate": {"id2": {"profile_id": "1528788703"}},
            }
        }
    )

    result = merge_matched_profiles([p1, p2])

    assert result["facebook"]["candidates_count"] == 1
    assert result["instagram"]["candidates_count"] == 2
    assert result["instagram"]["primary_candidate"]["id2"] == {
        "profile_id": "1528788703"
    }


def test_skip_platform_without_primary_candidate():

    p1 = person({
        "facebook": {
            "candidates_count": 10
        }
    })
    p2 = person({
        "facebook": None
    })

    result = merge_matched_profiles([p1, p2])
    assert result == {}


def test_skip_person_without_network_signature():

    p1 = SimpleNamespace(network_signature=None)

    result = merge_matched_profiles([p1])

    assert result == {}


def test_merge_primary_candidates_dict():

    p1 = person({
        "linkedin": {
            "candidates_count": 1,
            "primary_candidate": {
                "id1": {"profile_id": "123"}
            }
        }
    })

    p2 = person({
        "linkedin": {
            "candidates_count": 1,
            "primary_candidate": {
                "id2": {"profile_id": "456"}
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["linkedin"]["primary_candidate"]

    assert len(primary) == 2
    assert primary["id1"]["profile_id"] == "123"
    assert primary["id2"]["profile_id"] == "456"


def test_deduplicate_same_profile_id_and_url():

    p1 = person({
        "facebook": {
            "candidates_count": 20,
            "primary_candidate": {
                "id1": {
                    "profile_id": "1518788703",
                    "profile_url": None,
                    "profile_username": None,
                    "full_name": "Hevzi Cuci",
                    "friends": None,
                }
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 20,
            "primary_candidate": {
                "id2": {
                    "profile_id": "1518788703",  # duplicate
                    "profile_url": ["https://www.facebook.com/hevzi.cuci"],
                    "profile_username": "hevzi.cuci",
                    "full_name": "Hevzi Cuci",
                    "friends": 711,
                }
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["facebook"]["primary_candidate"]

    # only ONE should remain
    assert len(primary) == 1

    candidate = next(iter(primary.values()))

    assert candidate["profile_id"] == "1518788703"
    assert candidate["full_name"] == "Hevzi Cuci"

def test_deduplicate_by_profile_url_only():

    p1 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id1": {
                    "profile_id": None,
                    "profile_url": ["https://facebook.com/test"],
                }
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id2": {
                    "profile_id": None,
                    "profile_url": ["https://facebook.com/test"],  # duplicate
                }
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["facebook"]["primary_candidate"]

    assert len(primary) == 1

def test_deduplicate_and_merge_candidate_data():

    p1 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id1": {
                    "profile_id": "123",
                    "friends": None,
                }
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id2": {
                    "profile_id": "123",
                    "friends": 711,
                }
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["facebook"]["primary_candidate"]

    assert len(primary) == 1

    candidate = next(iter(primary.values()))

    # merged value preserved
    assert candidate["friends"] == 711
    
def test_deduplicate_and_merge_candidate_data_profile_username():

    p1 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id1": {
                    "profile_id": "123",
                    "friends": None,
                    "profile_username": "TestName"
                }
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id2": {
                    "profile_id": "123",
                    "friends": 711,
                    "profile_username": None
                }
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["facebook"]["primary_candidate"]

    assert len(primary) == 1

    candidate = next(iter(primary.values()))

    # merged value preserved
    assert candidate["profile_username"] == "TestName"
    
def test_deduplicate_and_merge_candidate_data_profile_picture():

    p1 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id1": {
                    "profile_id": "123",
                    "friends": None,
                    "profile_picture": "https://test.com/picture.jpg"
                }
            }
        }
    })

    p2 = person({
        "facebook": {
            "candidates_count": 1,
            "primary_candidate": {
                "id2": {
                    "profile_id": "123",
                    "friends": 711,
                    "profile_picture": None
                }
            }
        }
    })

    result = merge_matched_profiles([p1, p2])

    primary = result["facebook"]["primary_candidate"]

    assert len(primary) == 1

    candidate = next(iter(primary.values()))

    # merged value preserved
    assert candidate["profile_picture"] == "https://test.com/picture.jpg"
