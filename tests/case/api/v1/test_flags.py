import pytest
from fastapi import status as http_status


@pytest.mark.anyio
class TestFlagsEndpoints:

    endpoint = "/flags"

    @pytest.mark.xfail
    async def test_create_read_update(
        self,
        test_client,
        access_token,
        flags
    ) -> None:
        # create
        response = await test_client.post(
            self.endpoint,
            json={**flags},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        person_id = response_data.get("person").get("id")

        flag_id = response_data.get('id')
        assert flag_id is not None
        assert response_data.get('category') == flags.get(
            'category')

        # read
        response = await test_client.get(
            f"{self.endpoint}/{flag_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == flag_id

        # read_list
        response = await test_client.get(
            f"{self.endpoint}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data.get("items"), list)

        # read_person_flags
        response = await test_client.get(
            f"{self.endpoint}/by-person/{person_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data.get("items"), list)

        # update
        flags['category'] = "category"
        response = await test_client.put(
            f"{self.endpoint}/{flag_id}",
            json={**flags},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == flag_id
        assert response_data.get('category') == flags.get(
            'category')
