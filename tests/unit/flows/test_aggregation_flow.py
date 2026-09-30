import datetime
import pytest
import time
import uuid
from copy import deepcopy

from core.models import PersonModel, CandidateModel
from core.flows.aggregation import aggregation_flow


@pytest.mark.anyio
class TestInstagramEnrichFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_instagram_enrich(self, editor):
        persons_list = [
            # instagram, facebook
            {
                'firstname': "Elon",
                'lastname': "Musk",
                'source_id': "4474135174",
                'email': "elon.musk@gmail.com",
                'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
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
            #   'email': "anatkangel@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/anatkangel" # noqa
            # },
            # {
            #    'firstname': "Ronit",
            #    'lastname': "Kfir",
            #    'email': "ronitkfir@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/ronit-kfir-360b335" # noqa
            # }
            # instagram, facebook
            # {
            #    'firstname': "Nechama",
            #    'lastname': "Duek",
            #    'email': "nechamaduek@gmail.com",
            #    'linkedin_profile_url': "https://il.linkedin.com/in/nechama-duek-0ba79415a" # noqa
            # },
        ]

        person_ids = []
        candidate_ids = []
        persons = []
        candidates = []
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
            network_signature = {"network_signature": {
                    "url": {
                        "linkedin_profile_url": person_data.get(
                            'linkedin_profile_url')
                    },
                    "user_id": {
                        "instagram_user_id": person_data.get("source_id")
                    }
                }
            }
            candidate = deepcopy(person)
            candidate.update(**network_signature)
            if email := person_data.get('email'):
                person['personal_details']['email'] = {}
                person['personal_details']['email']['email_address'] = [email]

            person = PersonModel(**{
                **person,
                **{'last_edited_by': editor}
            })
            await person.insert()
            person_ids.append(person.id)
            persons.append(person)

            candidate["person"] = person.id
            candidate["search_id"] = str(uuid.uuid4())
            candidate["searched_at"] = str(datetime.datetime.now())
            candidate["source"] = "facebook"

            candidate = CandidateModel(**candidate)
            await candidate.insert()
            candidate_ids.append(candidate.id)
            candidates.append(candidate)

        for person in persons:
            candidate = find_candidate_by_person_id(candidates, person.id)
            start_time = time.time()
            await aggregation_flow(person.id, candidate.id)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))


def find_candidate_by_person_id(list, id_value):
    for item in list:
        if item.person.ref.id == id_value:
            return item
    return None
