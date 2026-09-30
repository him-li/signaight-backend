# flake8: noqa
import pytest

from core.rules.person.person_ruleset import person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635


@pytest.fixture
def project(fake):
    date = fake.date_time_this_decade().isoformat()
    return {
        'title': fake.text(200),
        'created_at': date,
        'updated_at': date,
        'user_id': fake.uuid4(),
        'person_ruleset': person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635
    }


@pytest.fixture
def projects(fake):
    projects = []
    for num in range(1, 4):
        date = fake.date_time_this_decade().isoformat()
        projects.append({
            'title': fake.text(200),
            'created_at': date,
            'updated_at': date,
            'user_id': fake.uuid4()
        })
    return projects
