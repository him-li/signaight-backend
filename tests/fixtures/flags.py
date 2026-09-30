import pytest
import uuid


@pytest.fixture
def flags():
    flags = {
        "category": "str",
        "severity": 1.1,
        "person": format(str(uuid.uuid4()))
    }
    return flags
