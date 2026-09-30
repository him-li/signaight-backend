import pytest
import time
import uuid

from core.models import PersonModel
from core.flows.grayfox_search import grayfox_search_flow
from core.config import settings


@pytest.mark.anyio
class TestGrayfoxFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_grayfox_search(self, editor):
        persons_list = [
            # instagram, facebook
            {
                'firstname': "Denys",
                'lastname': "Kyselov",
                'email': "denys.kyselov@gmail.com",
            },
            # {
            #    'firstname': "Mali",
            #    'lastname': "Alcobi",
            #    'email': "mali@dynamix.co.il",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/malialcobi" # noqa
            # },
            # {
            #    'firstname': "Anat",
            #    'lastname': "Kerem Angel",
            #    'email': "anatkangel@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/anatkangel" # noqa
            # },
            # {
            #    'firstname': "Ronit",
            #    'lastname': "Kfir",
            #    'email': "ronitkfir@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/ronit-kfir-360b335" # noqa
            # },
            # # instagram, facebook
            # {
            #    'firstname': "Nechama",
            #    'lastname': "Duek",
            #    'email': "nechamaduek@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/nechama-duek-0ba79415a" # noqa
            # }
        ]

        ids = []
        persons = []
        for person_data in persons_list:
            person = {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "f_name": person_data.get('firstname'),
                        },
                        "last_name": {
                            "l_name": person_data.get('lastname')
                        },
                        "full_name": {
                            "full_name": "{} {}".format(
                                person_data.get('firstname'),
                                person_data.get('lastname'))
                        }
                    },
                },
            }
            if email := person_data.get('email'):
                person['personal_details']['email'] = {}
                person['personal_details']['email']['email_address'] = [email]

            person = PersonModel(**{
                **person,
                **{'last_edited_by': editor}
            })
            await person.insert()
            ids.append(person.id)
            persons.append(person)

        host = (settings.JINA_REMOTE_FLOW_LINKEDIN
                if settings.JINA_REMOTE_FLOW_LINKEDIN else None)
        search_id = uuid.uuid4()

        for person in persons:
            start_time = time.time()
            await grayfox_search_flow(search_id, [person], host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
