import pytest
import uuid

# from fastapi_pagination import add_pagination
from core.dotty_dictionary import dotty
from core.models import PersonModel


@pytest.mark.anyio
class TestPersonModel:
    async def test_actions_insert(self, person, editor):
        person_data = dotty(person)
        person = PersonModel(**{
            **person_data,
            **{'last_edited_by': editor}
        })
        person = await person.insert()
        assert person.get_editor()
        assert person.personal_details

    async def test_actions_save_changes(self, person, editor):
        person_data = dotty(person)
        person = PersonModel(**{
            **person_data,
            **{'last_edited_by': editor}
        })
        await person.insert()
        assert person.personal_details.name.first_name.f_name == person_data.get('personal_details.name.first_name.f_name') # noqa
        assert person.get_editor()

        person.personal_details.name.first_name.f_name = "Jhon"
        person.personal_details.name.last_name.l_name = "Doe"
        await person.save_changes()
        person_data = dotty(person.model_dump())
        assert person_data.get("personal_details.name.first_name.f_name") == "Jhon" # noqa
        assert person_data.get("personal_details.name.last_name.l_name") == "Doe" # noqa

        person.personal_details.name.first_name.f_name = "Jhon1"
        person.personal_details.name.last_name.l_name = "Doe1"
        await person.save_changes()
        person_data = dotty(person.model_dump())
        assert person_data.get("personal_details.name.first_name.f_name") == "Jhon1" # noqa
        assert person_data.get("personal_details.name.last_name.l_name") == "Doe1"  # noqa

    async def test_actions_replace(self, person, editor):
        person_data = dotty(person)
        person = PersonModel(**{
            **person_data,
            **{'last_edited_by': editor}
        })
        await person.insert()
        assert person.personal_details.name.first_name.f_name == person_data.get('personal_details.name.first_name.f_name') # noqa

        person.personal_details.name.first_name.f_name = "Jhon"
        person.personal_details.name.last_name.l_name = "Doe"
        person.set_editor(
            id=uuid.uuid4(),
            email="j.doe@domain.tld",
            firstname="Jhon",
            lastname="Doe"
        )
        replaced_person = await person.replace()

        assert replaced_person.personal_details.name.first_name.f_name == "Jhon" # noqa
