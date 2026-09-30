import pytest
import uuid
import respx

from os import path
from httpx import AsyncClient, Response
from typing import Iterator, Generator, Callable, List
from jwcrypto import jwk, jwt
from datetime import datetime, timezone

from core.config import settings
from api.app import app


@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'


@pytest.fixture()
async def test_client() -> Iterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac


@pytest.fixture(scope="session")
def keys() -> jwk.JWKSet:
    with open(
        path.join(path.dirname(__file__), "jwks.json"), "r"
            ) as jwks_file:
        return jwk.JWKSet.from_json(jwks_file.read())


@pytest.fixture(scope="session")
def signature_key(keys: jwk.JWKSet) -> jwk.JWK:
    return keys.get_key("local-auth-tests-sig")


@pytest.fixture(scope="session")
def encryption_key(keys: jwk.JWKSet) -> jwk.JWK:
    return keys.get_key("local-auth-tests-enc")


@pytest.fixture(scope="session")
def user_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def generate_token(
    signature_key: jwk.JWK,
    encryption_key: jwk.JWK,
    user_id: str
        ):
    def _generate_token(encrypt: bool, **kwargs) -> str:
        iat = int(datetime.now(timezone.utc).timestamp())
        exp = iat + 3600

        claims = {
            "sub": user_id,
            "id": user_id,
            "email": "admin@signaight.ai",
            "iss": "http://localhost",
            "aud": ["CLIENT_ID"],
            "exp": exp,
            "iat": iat,
            "azp": "CLIENT_ID",
            **kwargs,
        }

        signed_token = jwt.JWT(header={"alg": "RS256"}, claims=claims)
        signed_token.make_signed_token(signature_key)

        if encrypt:
            encrypted_token = jwt.JWT(
                header={"alg": "RSA-OAEP-256", "enc": "A256CBC-HS512"},
                claims=signed_token.serialize(),
            )
            encrypted_token.make_encrypted_token(encryption_key)
            return encrypted_token.serialize()

        return signed_token.serialize()

    return _generate_token


@pytest.fixture(scope="session")
def generate_access_token(generate_token: Callable[..., str]):
    def _generate_access_token(
        encrypt: bool,
        *,
        scope: str = "",
        permissions: List[str] = [],
        **kwargs
    ) -> str:
        return generate_token(
            encrypt=encrypt, scope=scope, permissions=permissions, **kwargs
        )
    return _generate_access_token


@pytest.fixture(scope="session")
def access_token(generate_access_token: Callable[..., str]) -> str:
    return generate_access_token(encrypt=False)


@pytest.fixture(scope="session")
def signed_id_token(generate_token: Callable[..., str]) -> str:
    return generate_token(encrypt=False)


@pytest.fixture(scope="session")
def encrypted_id_token(generate_token: Callable[..., str]) -> str:
    return generate_token(encrypt=True)


@pytest.fixture(scope="module", autouse=True)
async def mock_api_requests(
    signature_key: jwk.JWK,
    user_id: uuid.UUID
) -> Generator[respx.MockRouter, None, None]:
    HOSTNAME = "https://localhost"

    with respx.mock(
        assert_all_mocked=True,
        assert_all_called=False
    ) as respx_mock:
        openid_configuration_route = (respx_mock.
                                      get("/.well-known/openid-configuration")
                                      )
        openid_configuration_route.return_value = Response(
            200,
            json={
                "issuer": f"{HOSTNAME}",
                "authorization_endpoint": f"{HOSTNAME}/authorize",
                "token_endpoint": f"{HOSTNAME}/token",
                "userinfo_endpoint": f"{HOSTNAME}/userinfo",
                "jwks_uri": f"{HOSTNAME}/.well-known/jwks.json",
            },
        )

        jwks_route = respx_mock.get("/.well-known/jwks.json")
        jwks_route.return_value = Response(
            200,
            json={"keys":
                  [signature_key.export(private_key=False, as_dict=True)]}
        )

        jwks_route = respx_mock.get("/userinfo")
        jwks_route.return_value = Response(
            200,
            json={"sub": str(uuid.uuid4()),
                  "email": "email@mock.com",
                  "fields": {
                  "firstname": "John",
                  "lastname": "Doe"}
                  }
        )

        mapbox_routes = ["Rome", "Paris", "Seoul", "Houston", "San Diego", "Taiwan", "Boston", "Santiago"] # noqa

        for route in mapbox_routes:
            mapbox_route = respx_mock.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{route}.json?access_token={settings.NEXT_PUBLIC_MAPBOX_TOKEN}") # noqa
            mapbox_route.return_value = Response(
                200,
                json={"type":"FeatureCollection","query":["rome"],"features":[{"id":"place.47384688","type":"Feature","place_type":["place"],"relevance":1,"properties":{"mapbox_id":"dXJuOm1ieHBsYzpBdE1JY0E","wikidata":"Q220"},"text":"Roma","place_name":"Roma, Rome, Italy","matching_text":"Rome","matching_place_name":"Rome, Rome, Italy","bbox":[12.2236583,41.6353959,12.855839,42.140969],"center":[12.482932,41.89332],"geometry":{"type":"Point","coordinates":[12.482932,41.89332]},"context":[{"id":"region.762992","mapbox_id":"dXJuOm1ieHBsYzpDNlJ3","wikidata":"Q18288160","short_code":"IT-RM","text":"Rome"},{"id":"country.8816","mapbox_id":"dXJuOm1ieHBsYzpJbkE","wikidata":"Q38","short_code":"it","text":"Italy"}]},{"id":"region.762992","type":"Feature","place_type":["region"],"relevance":1,"properties":{"mapbox_id":"dXJuOm1ieHBsYzpDNlJ3","wikidata":"Q18288160","short_code":"IT-RM"},"text":"Rome","place_name":"Rome, Italy","bbox":[11.6247992,41.3260059,13.296274,42.296014],"center":[12.4829321,41.8933203],"geometry":{"type":"Point","coordinates":[12.4829321,41.8933203]},"context":[{"id":"country.8816","mapbox_id":"dXJuOm1ieHBsYzpJbkE","wikidata":"Q38","short_code":"it","text":"Italy"}]},{"id":"place.282945772","type":"Feature","place_type":["place"],"relevance":1,"properties":{"mapbox_id":"dXJuOm1ieHBsYzpFTjFvN0E","wikidata":"Q6580"},"text":"Rome","place_name":"Rome, Georgia, United States","bbox":[-85.462207,34.132568,-85.015193,34.432181],"center":[-85.164673,34.257038],"geometry":{"type":"Point","coordinates":[-85.164673,34.257038]},"context":[{"id":"district.7702252","mapbox_id":"dXJuOm1ieHBsYzpkWWJz","wikidata":"Q486389","text":"Floyd County"},{"id":"region.173292","mapbox_id":"dXJuOm1ieHBsYzpBcVRz","wikidata":"Q1428","short_code":"US-GA","text":"Georgia"},{"id":"country.8940","mapbox_id":"dXJuOm1ieHBsYzpJdXc","wikidata":"Q30","short_code":"us","text":"United States"}]},{"id":"place.283052268","type":"Feature","place_type":["place"],"relevance":1,"properties":{"mapbox_id":"dXJuOm1ieHBsYzpFTjhJN0E","wikidata":"Q1012403"},"text":"Romeoville","place_name":"Romeoville, Illinois, United States","bbox":[-88.163508,41.591193,-88.048309,41.679895],"center":[-88.089506,41.647531],"geometry":{"type":"Point","coordinates":[-88.089506,41.647531]},"context":[{"id":"district.25069292","mapbox_id":"dXJuOm1ieHBsYzpBWDZHN0E","wikidata":"Q483942","text":"Will County"},{"id":"region.17644","mapbox_id":"dXJuOm1ieHBsYzpST3c","wikidata":"Q1204","short_code":"US-IL","text":"Illinois"},{"id":"country.8940","mapbox_id":"dXJuOm1ieHBsYzpJdXc","wikidata":"Q30","short_code":"us","text":"United States"}]},{"id":"place.282978540","type":"Feature","place_type":["place"],"relevance":1,"properties":{"mapbox_id":"dXJuOm1ieHBsYzpFTjNvN0E","wikidata":"Q6586"},"text":"Rome","place_name":"Rome, New York, United States","bbox":[-75.645465,43.107306,-75.304278,43.300875],"center":[-75.45573,43.212847],"geometry":{"type":"Point","coordinates":[-75.45573,43.212847]},"context":[{"id":"district.17491692","mapbox_id":"dXJuOm1ieHBsYzpBUXJtN0E","wikidata":"Q115043","text":"Oneida County"},{"id":"region.107756","mapbox_id":"dXJuOm1ieHBsYzpBYVRz","wikidata":"Q1384","short_code":"US-NY","text":"New York"},{"id":"country.8940","mapbox_id":"dXJuOm1ieHBsYzpJdXc","wikidata":"Q30","short_code":"us","text":"United States"}]}],"attribution":"NOTICE: © 2023 Mapbox and its suppliers. All rights reserved. Use of this data is subject to the Mapbox Terms of Service (https://www.mapbox.com/about/maps/). This response and the information it contains may not be retained. POI(s) provided by Foursquare."} # noqa
            )

        yield respx_mock
