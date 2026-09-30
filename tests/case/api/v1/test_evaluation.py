import pytest
from fastapi import status as http_status


@pytest.mark.anyio
class TestEvaluationEndpoints:

    endpoint = "/evaluation"

    @pytest.mark.skip(reason="require valid person in database")
    async def test_create_read_update(
        self,
        test_client,
        access_token,
        evaluation
    ) -> None:
        # create
        response = await test_client.post(
            self.endpoint,
            json={**evaluation},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        person_id = response_data.get("person").get("id")

        evaluation_id = response_data.get('id')
        assert evaluation_id is not None
        assert response_data.get('resilience') == evaluation.get(
            'resilience')

        # read
        response = await test_client.get(
            f"{self.endpoint}/{evaluation_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == evaluation_id

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

        # read_person_evaluations
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
        evaluation['resilience']['score'] = 11
        response = await test_client.put(
            f"{self.endpoint}/{evaluation_id}",
            json={**evaluation},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == evaluation_id
        assert response_data.get('resilience') == evaluation.get(
            'resilience')
