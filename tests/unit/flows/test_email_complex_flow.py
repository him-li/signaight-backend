# flake8: noqa
import pytest
import time
from asyncio import sleep
from dotty_dictionary import dotty

from core.flows.complex_search import complex_search_flow
from core.models import ProjectModel, PersonModel


@pytest.fixture
def persons_list():
    return [
        # perfect match
        {
            'email': "denys.kyselov@gmail.com"
        },
        {
            'firstname': "Denys",
            'lastname': "Kyselov",
            'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
        },
    ]


@pytest.mark.anyio
class TestEmailComplexFlow:

    @pytest.mark.skip(
        reason="Flow take a lot of time to complete and for local use only now")
    async def test_email(self, editor, persons_list):
        ids = []
        persons = []

        project = ProjectModel(title='Test Project')
        await project.insert()
        for person_data in persons_list:
            person = dotty()
            if linkedin_profile_url := person_data.get('linkedin_profile_url'):
                person['network_signature.url'
                            '.linkedin_profile_url'] = linkedin_profile_url
            if first_name := person_data.get('firstname'):
                person['personal_details.name.first_name.f_name'] = first_name
            if last_name := person_data.get('lastname'):
                person['personal_details.name.last_name.l_name'] = last_name
            if first_name or last_name:
                person['personal_details.name.full_name.full_name'] = " ".join(
                                            [str(first_name), str(last_name)])
            if email := person_data.get('email'):
                person['personal_details.email.email_address'] = [email]
            person = PersonModel(project=project, **{
                **person.to_dict(),
                **{'last_edited_by': editor}
            })
            await person.insert()
            ids.append(person.id)
            persons.append(person)

        for person in persons:
            start_time = time.time()
            await complex_search_flow([person.id])
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))

        for person in persons:
            _person = await PersonModel.get(person.id)
            print(f"Person {_person.id} score: {_person.signaight_score}")            
        