import pytest
import httpx
from fastapi import status as http_status

@pytest.mark.anyio
async def test_healthcheck(test_client) -> None:
    response = await test_client.get("/healthcheck")
    assert response.status_code == 200
    json = response.json()
    assert json.get('status') == 'OK'


@pytest.mark.anyio
class TestAuthenticated:

    async def test_missing_token(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/auth/authenticated")
        assert response.status_code == http_status.HTTP_401_UNAUTHORIZED

    async def test_expired_token(
        self,
        test_client: httpx.AsyncClient,
        generate_access_token
    ):
        access_token = generate_access_token(encrypt=False, exp=0)

        response = await test_client.get(
            "/auth/authenticated", headers={"Authorization":
                                            f"Bearer {access_token}"}
        )

        assert response.status_code == http_status.HTTP_401_UNAUTHORIZED

    async def test_valid_token(
        self,
        test_client: httpx.AsyncClient,
        generate_access_token,
        user_id: str
    ):
        access_token = generate_access_token(encrypt=False, scope="openid")

        response = await test_client.get(
            "/auth/authenticated", headers={"Authorization":
                                            f"Bearer {access_token}"}
        )

        assert response.status_code == http_status.HTTP_200_OK

        json = response.json()
        assert json == {
            "id": user_id,
            "scope": ["openid"],
            "permissions": [],
            "access_token": access_token,
        }

    @pytest.mark.skip(reason="Optional auth seems does not work properly")
    async def test_optional(
        self,
        test_client: httpx.AsyncClient,
        generate_access_token,
        user_id: str
    ):
        response = await test_client.get("/auth/authenticated-optional")
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json() is None

        expired_access_token = generate_access_token(
            encrypt=False, scope="openid", exp=0
        )
        response = await test_client.get(
            "/auth/authenticated-optional",
            headers={"Authorization": f"Bearer {expired_access_token}"},
        )
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json() is None

        access_token = generate_access_token(encrypt=False, scope="openid offline_access")
        response = await test_client.get(
            "/auth/authenticated-optional",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json() == {
            "id": user_id,
            "scope": ["openid", "offline_access"],
            "permissions": [],
            "access_token": access_token,
        }

    async def test_missing_scope(
        self, test_client: httpx.AsyncClient, generate_access_token
    ):
        access_token = generate_access_token(encrypt=False, scope="openid")

        response = await test_client.get(
            "/auth/authenticated-scope", headers={"Authorization":
                                                  f"Bearer {access_token}"}
        )

        assert response.status_code == http_status.HTTP_403_FORBIDDEN

    async def test_valid_scope(
        self,
        test_client: httpx.AsyncClient,
        generate_access_token,
        user_id: str
    ):
        access_token = generate_access_token(
            encrypt=False, scope="openid offline_access"
        )

        response = await test_client.get(
            "/auth/authenticated-scope", headers={"Authorization":
                                                  f"Bearer {access_token}"}
        )

        assert response.status_code == http_status.HTTP_200_OK

        json = response.json()
        assert json == {
            "id": user_id,
            "scope": ["openid", "offline_access"],
            "permissions": [],
            "access_token": access_token,
        }
