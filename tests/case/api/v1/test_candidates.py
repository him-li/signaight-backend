import pytest
# import uuid
from fastapi import status as http_status

from core.models import PersonModel, CandidateModel


@pytest.mark.anyio
class TestPersonCandidateEndpoints:

    endpoint = "/persons/{}/candidates/"

    async def test_create_read_update_delete(
        self,
        test_client,
        access_token,
        person,
        editor,
        candidate,
    ) -> None:
        person = PersonModel(**{
            **person,
            **{'last_edited_by': editor}
        })
        person = await person.insert()
        # create
        response = await test_client.post(
            self.endpoint.format(person.id),
            json={**candidate},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        candidate_id = response_data.get('id')
        assert candidate_id is not None
        assert response_data.get('source') == candidate.get('source')
        assert response_data.get('resource') == candidate.get('resource')

        # read
        response = await test_client.get(
            f"{self.endpoint.format(person.id)}{candidate_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == candidate_id

        # update
        candidate['source'] = 'twitter'
        response = await test_client.put(
            f"{self.endpoint.format(person.id)}{candidate_id}",
            json={**candidate},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == candidate_id
        assert response_data.get('source') == candidate.get('source')

        # delete
        response = await test_client.delete(
            f"{self.endpoint.format(person.id)}{candidate_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_204_NO_CONTENT
        candidate = await CandidateModel.get(candidate_id)
        assert candidate is None

    async def test_read_list_searched_filtered_ordered(
        self,
        test_client,
        access_token,
        person,
        editor,
        candidates,
    ) -> None:
        person = PersonModel(**{
            **person,
            **{'last_edited_by': editor}
        })
        await person.insert()

        first_candidate_details = candidates[0].get('personal_details', {})
        f_name = (first_candidate_details.get('name', {})
                  .get('first_name', {}).get('f_name'))
        l_name = (first_candidate_details.get('name', {})
                  .get('last_name', {}).get('l_name'))
        source = candidates[0].get('source')
        resource = candidates[0].get('resource')

        candidates = [CandidateModel(**candidate, person=person)
                      for candidate in candidates]
        await CandidateModel.insert_many(candidates)
        candidate_ids = [str(candidate.id) for candidate in candidates]

        response = await test_client.get(
            self.endpoint.format(person.id),
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) == len(candidates)
        response_candidate_ids = [candidate.get('id') for candidate
                                  in response_data.get('items', [])]
        assert response_candidate_ids[0] in candidate_ids
        assert response_candidate_ids.sort() == candidate_ids.sort()

        # filtering
        response = await test_client.get(
            self.endpoint.format(person.id),
            params={
                'f_name': f_name,
                'l_name': l_name,
                'source': source,
                'resource': resource
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) > 0
        response_f_name = (response_data.get('items', [])[0]
                           .get('personal_details', {})
                           .get('name', {})
                           .get('first_name', {})
                           .get('f_name'))
        assert response_f_name == f_name
        response_l_name = (response_data.get('items', [])[0]
                           .get('personal_details', {})
                           .get('name', {})
                           .get('last_name', {})
                           .get('l_name'))
        assert response_l_name == l_name
        response_source = (response_data.get('items', [])[0]
                           .get('source'))
        assert response_source == source
        response_resource = (response_data.get('items', [])[0]
                             .get('resource'))
        assert response_resource == resource

        # ordering
        f_names = ([candidate.personal_details.name.first_name.f_name
                    for candidate in candidates])
        f_names.sort(reverse=True)
        response = await test_client.get(
            self.endpoint.format(person.id),
            params={
                'order_by': '-personal_details__name__first_name__f_name'
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        response_f_name = (response_data.get('items', [])[0]
                           .get('personal_details', {})
                           .get('name', {})
                           .get('first_name', {})
                           .get('f_name'))
        assert response_f_name == f_names[0]
        response_f_name = (response_data.get('items', [])[-1]
                           .get('personal_details', {})
                           .get('name', {})
                           .get('first_name', {})
                           .get('f_name'))
        assert response_f_name == f_names[-1]
