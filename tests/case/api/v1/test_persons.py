import copy
import pytest
import pandas
import uuid
import json
from deepdiff import DeepDiff
from fastapi import status as http_status

from core.models import ProjectModel, PersonModel
from core.models.geo_trace import GeoTrace
from api.v1.projects.schemas import PersonsLeaderboardInfo


@pytest.mark.anyio
class TestPersonsEndpoints():

    endpoint = "/persons"

    @pytest.mark.skip(reason="This test does not work with new linkedin flow")
    async def test_create_read_update_delete(
        self,
        test_client,
        access_token,
        project,
        person,
        nodes_links
    ) -> None:
        project = ProjectModel(**project)
        await project.insert()
        # create
        response = await test_client.post(
            self.endpoint,
            json={**person, **{'project_id': str(project.id)}},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        person_id = response_data.get('id')
        assert person_id is not None
        assert response_data.get('project', {}).get('title') == project.title
        # read
        response = await test_client.get(
            f"{self.endpoint}/{person_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == person_id
        assert response_data.get('project', {}).get('title') == project.title
        # update
        person['personal_details']['email']['email_address'].append(
            'jhon.doe@example.org')
        person_emails = (
            person.get('personal_details', {})
            .get('email', {})
            .get('email_address', []))
        response = await test_client.put(
            f"{self.endpoint}/{person_id}",
            json=person,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == person_id
        assert response_data.get('project', {}).get('title') == project.title
        response_email_address = (
            response_data.get('personal_details', {})
            .get('email', {})
            .get('email_address', []))
        assert response_email_address == person_emails
        assert 'jhon.doe@example.org' in response_email_address

        response = await test_client.delete(
            f"{self.endpoint}/{person_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_204_NO_CONTENT
        person = await PersonModel.get(person_id)
        assert person is None

    @pytest.mark.skip(reason="This test does not work with cerbos ACL")
    async def test_read_list_searched_filtered_ordered(
        self,
        test_client,
        access_token,
        persons
    ) -> None:
        first_user_details = persons[0].get('personal_details', {})
        email = first_user_details.get('email').get('email_address', [])
        f_name = (first_user_details.get('name', {})
                  .get('first_name', {}).get('f_name'))
        persons = [PersonModel(**person) for person in persons]
        await PersonModel.insert_many(persons)
        person_ids = [str(person.id) for person in persons]
        response = await test_client.get(
            self.endpoint,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) == len(persons)
        response_person_ids = [person.get('id') for person
                               in response_data.get('items', [])]
        assert response_person_ids[0] in person_ids
        assert response_person_ids.sort() == person_ids.sort()

        # sorting
        response = await test_client.get(
            self.endpoint,
            params={
                'search': email
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) > 0
        response_email_address = (
            response_data.get('items', [])[0]
            .get('personal_details', {})
            .get('email', {})
            .get('email_address', []))
        assert response_email_address == email

        # filtering
        response = await test_client.get(
            self.endpoint,
            params={
                'email_address': email,
                'f_name__in': f_name
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) > 0
        response_f_name = (
            response_data.get('items', [])[0]
            .get('personal_details', {})
            .get('name', {})
            .get('first_name', {})
            .get('f_name'))
        assert response_f_name == f_name

        # ordering
        f_names = ([person.personal_details.name.first_name.f_name
                    for person in persons])
        f_names.sort(reverse=True)
        response = await test_client.get(
            self.endpoint,
            params={
                'order_by': '-personal_details__name__first_name__f_name'
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        response_f_name = (
            response_data.get('items', [])[0]
            .get('personal_details', {})
            .get('name', {})
            .get('first_name', {})
            .get('f_name'))
        assert response_f_name == f_names[0]
        response_f_name = (
            response_data.get('items', [])[-1]
            .get('personal_details', {})
            .get('name', {})
            .get('first_name', {})
            .get('f_name'))
        assert response_f_name == f_names[-1]

    @pytest.mark.skip(reason="This test does not work with new linkedin flow")
    async def test_create_update_geotrace(
        self,
        test_client,
        access_token,
        person,
        locations
    ) -> None:
        person["personal_details"]["location"] = locations

        create = await test_client.post(
            self.endpoint,
            json=person,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert create.status_code == http_status.HTTP_201_CREATED
        create_data = create.json()
        person_id = create_data.get("id")
        assert create_data.get("geo_trace") is not None
        geo_trace = GeoTrace(**create_data.get("geo_trace"))
        assert isinstance(geo_trace, GeoTrace)
        geo_trace_features = geo_trace.features
        create_locations = copy.deepcopy(locations)
        if create_locations.get('check_ins') is not None:
            check_ins = create_locations.get('check_ins').get("fb_check_ins")
            check_ins_dict = {f"check_in_{checkin}": checkin for checkin in
                              check_ins}
            create_locations.update(**check_ins_dict)
            create_locations.pop("check_ins")
        [create_locations] = pandas.json_normalize(
            create_locations, sep=".").to_dict(
            orient='records')
        create_locations_len = len(create_locations.keys())
        assert len(geo_trace_features) == create_locations_len

        update_locations = {**locations,
                            "current_city": {"fb_current_city": "Santiago"}}
        person_update = person
        person_update["personal_details"]["location"] = update_locations
        update = await test_client.put(
            f"{self.endpoint}/{person_id}",
            json=person_update,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert update.status_code == http_status.HTTP_200_OK
        update_data = update.json()
        update_geo_trace = GeoTrace(**update_data.get("geo_trace"))
        assert isinstance(geo_trace, GeoTrace)
        update_geo_trace_features = update_geo_trace.features
        if update_locations.get('check_ins') is not None:
            check_ins = update_locations.get('check_ins').get("fb_check_ins")
            check_ins_dict = {f"check_in_{checkin}": checkin for checkin in
                              check_ins}
            update_locations.update(**check_ins_dict)
            update_locations.pop("check_ins")
        [update_locations] = pandas.json_normalize(
            update_locations, sep=".").to_dict(
            orient='records')
        update_locations_len = len(update_locations.keys())
        assert len(update_geo_trace_features) == update_locations_len

    async def test_read_leaderboard_info(
            self,
            test_client,
            access_token,
            person,
            editor,
            project
    ) -> None:
        project = ProjectModel(**project)
        await project.insert()
        # create
        person = PersonModel(**{
            **person,
            **{
                'project': str(project.id),
                'last_edited_by': editor
            }
        })
        person = await person.insert()
        person = person.model_dump()
        person_id = person.get('id')
        assert person_id is not None
        # read
        response = await test_client.get(
            f"{self.endpoint}/by-project/{project.id}/leaderboard-info",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        response_info = PersonsLeaderboardInfo(**response_data)
        assert isinstance(response_info, PersonsLeaderboardInfo)

    @pytest.mark.skip(reason="This test does not work with new linkedin flow")
    async def test_person_patch(
            self,
            test_client,
            access_token,
            person,
            description_bio_intro
    ) -> None:
        create = await test_client.post(
            self.endpoint,
            json=person,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        create_data = create.json()
        person_id = create_data.get("id")

        patch_person = {**description_bio_intro}
        patch = await test_client.patch(
            f"{self.endpoint}/{person_id}",
            json=patch_person,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        patch_data = patch.json()

        assert not DeepDiff(patch_data,
                            {**create_data, **description_bio_intro})

    async def test_audit_log(
            self,
            test_client,
            access_token,
            person,
            editor
    ) -> None:
        person = PersonModel(**{
            **person,
            **{'last_edited_by': editor}
        })
        person = await person.insert()
        person_id = person.model_dump().get("id")

        history = await test_client.get(
            f"{self.endpoint}/{person_id}/history",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        history_data = history.json()
        assert history_data is not None
        assert history_data.get("size") > 0
        assert history_data.get("items") is not None
