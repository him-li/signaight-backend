from core.utils import update_nested_dict
from deepdiff import DeepDiff

d = {
    "list": ["element1"],
    "dict": {
        "change": "change",
        "initial_none": None,
        "final_none": "Not None",
    },
}

u = {
    "list": ["element2"],
    "dict": {
        "change": "changed something",
        "initial_none": "Not None",
        "final_none": None,
        "new_nested_key": "something"
    },
    "new_key": 123
}

expected_result = {
    "list": ["element1", "element2"],
    "dict": {
        "change": "changed something",
        "initial_none": "Not None",
        "final_none": "Not None",
        "new_nested_key": "something"
    },
    "new_key": 123
}


def test_update_nested_dict():
    update_result = update_nested_dict(d, u)
    assert not DeepDiff(update_result, expected_result)
