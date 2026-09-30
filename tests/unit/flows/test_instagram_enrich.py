# flake8: noqa
import pytest
import time
import uuid

from core.models import PersonModel
from core.flows.instagram_enrich import instagram_enrich_flow
from core.config import settings


@pytest.mark.anyio
class TestInstagramEnrichFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_instagram_enrich(self, editor):
        persons_list = [
            # instagram, facebook
            {
                'firstname': "Christina",
                'lastname': "Horvath",
                'person_id': str(uuid.uuid4()),
                'source_id': "26974566094",
            },
            {
                'firstname': "Todo Dia",
                'lastname': "The Office",
                'person_id': str(uuid.uuid4()),
                'source_id': "63507700688",
            },
            {
                'firstname': "Dries",
                'lastname': "Peeters",
                'person_id': str(uuid.uuid4()),
                'source_id': "407610128",
            },
            # {
            #    'firstname': "Mali",
            #    'lastname': "Alcobi",
            #    'email': "mali@dynamix.co.il",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/malialcobi"
            # },
            # {
            #    'firstname': "Anat",
            #    'lastname': "Kerem Angel",
            #   'email': "anatkangel@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/anatkangel"
            # },
            # {
            #    'firstname': "Ronit",
            #    'lastname': "Kfir",
            #    'email': "ronitkfir@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/ronit-kfir-360b335"
            # }
            # instagram, facebook
            # {
            #    'firstname': "Nechama",
            #    'lastname': "Duek",
            #    'email': "nechamaduek@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/nechama-duek-0ba79415a"
            # },
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
                "network_signature": {
                    "user_id": {
                        "instagram_user_id": person_data.get("source_id")
                    }
                }
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

        for person in persons:
            start_time = time.time()
            await instagram_enrich_flow([person], host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
