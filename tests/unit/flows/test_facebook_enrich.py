# flake8: noqa
import pytest
import time
import uuid

from core.models import PersonModel
from core.flows.facebook_enrich import facebook_enrich_flow
from core.config import settings


@pytest.mark.anyio
class TestFacebookEnrichFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_facebook_enrich(self, editor):
        persons_list = [
            # instagram, facebook
            {
                'firstname': "Elon",
                'lastname': "Musk",
                'person_id': str(uuid.uuid4()),
                'source_id': "100014807225880",
                'email': "elon.musk@gmail.com",
                'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
            },
            {
                'firstname': "Abdullah",
                'lastname': "Al Mamun",
                'person_id': str(uuid.uuid4()),
                'source_id': "100002543960087",
                'email': "elon.musk@gmail.com",
                'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
            },
            {
                'firstname': "Hana",
                'lastname': "Rado",
                'person_id': str(uuid.uuid4()),
                'source_id': "701225128",
                'email': "hanarado@gmail.com",
                'linkedin_profile_url': "https://il.linkedin.com/in/radohana"
            },
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
                    "url": {
                        "linkedin_profile_url": person_data.get(
                            'linkedin_profile_url')
                    },
                    "user_id": {
                        "facebook_user_id": person_data.get("source_id")
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
            await facebook_enrich_flow([person], host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
