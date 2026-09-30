import pytest
from fastapi import status as http_status


@pytest.mark.anyio
class TestAlertsEndpoints:

    endpoint = "/alerts"

    @pytest.mark.skip(reason="require valid person in database")
    async def test_create_read_update(
        self,
        test_client,
        access_token,
        alerts
    ) -> None:
        # create
        response = await test_client.post(
            self.endpoint,
            json={**alerts},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        response_data = response.json()
        person_id = response_data.get("person").get("id")

        alert_id = response_data.get('id')
        assert alert_id is not None
        assert response_data.get('strong_affinity_with_israel') == alerts.get(
            'strong_affinity_with_israel')

        # read
        response = await test_client.get(
            f"{self.endpoint}/{alert_id}",
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == alert_id

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

        # read_person_alerts
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
        alerts['strong_affinity_with_israel']['score'] = 11
        response = await test_client.put(
            f"{self.endpoint}/{alert_id}",
            json={**alerts},
            headers={
                "Authorization": f'Bearer {access_token}'
            }
        )
        assert response.status_code == http_status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get('id') == alert_id
        assert response_data.get('strong_affinity_with_israel') == alerts.get(
            'strong_affinity_with_israel')
