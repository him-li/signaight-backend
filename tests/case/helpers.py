from fastapi import status as http_status


class EndpointsMixin:

    endpoint = None

    async def test_create(self, test_client, data):
        response = await test_client.post(
            f"/api/v1/{self.endpoint}",
            data=data
            )
        assert response.status_code == http_status.HTTP_201_CREATED
        return response

    async def test_read(self, test_client) -> dict:
        pass

    async def test_read_list(self, test_client) -> None:
        pass

    async def test_update(self, test_client, data) -> None:
        pass

    async def test_delete(self, test_client) -> None:
        pass
