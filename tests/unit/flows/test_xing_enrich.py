import pytest
import time
import uuid

from core.models import PersonModel
from core.flows.xing_enrich import xing_enrich_flow
from core.config import settings


@pytest.mark.anyio
class TestXingEnrichFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_xing_enrich(self, editor):
        persons_list = [
            # Work, School, Interests, Qualifications, Languages, Location, Skills # noqa
            {
                'firstname': "Katinka",
                'lastname': "Fekete",
                'person_id': str(uuid.uuid4()),
                'xing_profile_url': "https://www.xing.com/profile/Katinka_Fekete"  # noqa
            },
            # Profile about me, Contacts
            {
                'firstname': "Vincent",
                'lastname': "OberJung",
                'person_id': str(uuid.uuid4()),
                'xing_profile_url': "https://www.xing.com/profile/Vincent_OberJung"  # noqa
            },
            # # Business Address, email and phone
            {
                'firstname': "Jana",
                'lastname': "Huckenholz",
                'person_id': str(uuid.uuid4()),
                'xing_profile_url': "https://www.xing.com/profile/Jana_Huckenholz"  # noqa
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
                        "xing_profile_url": person_data.get(
                            'xing_profile_url')
                    },
                }
            }

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
            await xing_enrich_flow([person], host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            person = await PersonModel.get(person.id)
            assert person.personal_details.name.full_name.xing_full_name
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
