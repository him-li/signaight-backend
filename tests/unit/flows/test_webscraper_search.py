# flake8: noqa
import pytest
import time

from core.models import PersonModel, ProjectModel
from core.flows.webscraper_search import webscraper_search_flow
from core.config import settings


@pytest.mark.anyio
class TestEumwSearchFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_eumw_search(self, editor):
        persons_list = [
            # EU most wanted
             {
                'firstname': 'Martin',
                'lastname': '',
                'linkedin_profile_url': "https://www.linkedin.com/in/techrecruitersourcer/"
            },
            #  {
            #     'firstname': 'Rick',
            #     'lastname': 'Wessels',
            #     'linkedin_profile_url': "https://www.linkedin.com/in/techrecruitersourcer/"
            # },
        ]

        ids = []
        persons = []
        project = ProjectModel(title='project')

        await project.insert()
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
                    }
                },
                "project": project
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
            response = await webscraper_search_flow([person], "", host)
            end_time = time.time()
            print(response)

            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
