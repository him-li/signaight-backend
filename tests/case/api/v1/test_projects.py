import pytest
from fastapi import status as http_status

from core.models import ProjectModel


@pytest.mark.anyio
class TestProjectEndpoints():

    endpoint = "/projects"

    @pytest.mark.xfail(reason="Acl do not work in tests properly")
    async def test_create_read_update_delete(
        self,
        test_client,
        access_token,
        project
    ) -> None:
        # create
        response = await test_client.post(
            self.endpoint,
            json=project,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        project_id = response_data.get('id')
        assert project_id is not None
        assert response_data.get('title') == project.get('title')

        # read
        response = await test_client.get(
            f"{self.endpoint}/{project_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == project_id
        assert response_data.get('title') == project.get('title')

        # update
        project['title'] = 'New title'
        response = await test_client.put(
            f"{self.endpoint}/{project_id}",
            json=project,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == project_id
        assert response_data.get('title') == project.get('title')

        # delete
        response = await test_client.delete(
            f"{self.endpoint}/{project_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_204_NO_CONTENT
        project = await ProjectModel.get(project_id)
        assert project is None

    @pytest.mark.xfail(reason="Acl do not work in tests properly")
    async def test_read_list_searched_filtered_ordered(
        self,
        test_client,
        access_token,
        projects
    ) -> None:
        projects_objects = []
        for project in projects:
            response = await test_client.post(
                self.endpoint,
                json=project,
                headers={
                    "Authorization": f'Bearer {access_token}'
                }
            )
            assert response.status_code == http_status.HTTP_201_CREATED
            projects_objects.append(ProjectModel(**response.json()))
        first_project_details = projects_objects[0]
        title = first_project_details.title
        project_ids = [str(project.id) for project in projects_objects]
        response = await test_client.get(
            self.endpoint,
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) == len(projects_objects)
        response_project_ids = [project.get('id') for project
                                in response_data.get('items', [])]
        assert response_project_ids[0] in project_ids
        assert response_project_ids.sort() == project_ids.sort()

        # sorting
        response = await test_client.get(
            self.endpoint,
            params={
                'search': title
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) > 0
        response_title_address = (response_data.get('items', [])[0]
                                  .get('title'))
        assert response_title_address == title

        # filtering
        response = await test_client.get(
            self.endpoint,
            params={
                'title': title,
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data.get('items', [])) > 0
        response_title = (response_data.get('items', [])[0]
                          .get('title'))
        assert response_title == title

        # ordering
        titles = ([project.title for project in projects_objects])
        titles.sort(reverse=True)
        response = await test_client.get(
            self.endpoint,
            params={
                'order_by': '-title'
            },
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        response_title = (response_data.get('items', [])[0]
                          .get('title'))
        assert response_title == titles[0]
        response_title = (response_data.get('items', [])[-1]
                          .get('title'))
        assert response_title == titles[-1]
