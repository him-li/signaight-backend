import pytest
import time
import uuid

from core.models import PersonModel
from core.flows.interpol_search_enrich import interpol_search_flow
from core.config import settings


@pytest.mark.anyio
class TestInterpolSearchFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_interpol_search(self, editor):
        persons_list = [
            {
                'firstname': "Eugene",
                'lastname': "Palmer",
                'person_id': str(uuid.uuid4()),
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
            await interpol_search_flow([person], host=host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
