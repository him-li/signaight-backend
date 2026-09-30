import json
import pytest
import redis
import time

from asyncio import sleep
from core.config import settings
from core.rest_client import (
    Resource,
    AsyncResource,
    RedisCachedAPI,
    LongRedisCachedAPI
)


class VetricSearchResource(Resource):
    actions = {
        "users": {"method": "POST", "url": "search/users"},
    }


class VetricProfilesResource(Resource):
    actions = {
        "about": {"method": "GET", "url": "profiles/{}/about"},
    }


class AsyncVetricSearchResource(AsyncResource):
    actions = {
        "users": {"method": "POST", "url": "search/users"},
    }


class AsyncVetricProfilesResource(AsyncResource):
    actions = {
        "about": {"method": "GET", "url": "profiles/{}/about"},
    }

class GrayfoxSearchResource(AsyncResource):
    actions = {
        "submit": {"method": "POST", "url": "/api"},
        "get": {"method": "GET", "url": "/api"},
    }


@pytest.fixture
def redis_cached_rest_client_vetric():
    api = RedisCachedAPI(
        api_root_url='https://api.vetric.io/facebook/v1/',  # base api url
        params={},  # default params
        headers={
            'x-api-key': settings.VETRIC_FACEBOOK_API_KEY
        },  # default headers
        timeout=100,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
        cache_default_ttl=432000,  # default cache ttl in seconds
        cache_methods=('GET', 'POST')  # methods to process for caching
    )
    api.add_resource(resource_name="search", resource_class=VetricSearchResource)
    api.add_resource(resource_name='profiles', resource_class=VetricProfilesResource)
    return api

@pytest.fixture
def redis_cached_async_rest_client_vetric():
    api = RedisCachedAPI(
        api_root_url='https://api.vetric.io/facebook/v1/',  # base api url
        params={},  # default params
        headers={
            'x-api-key': settings.VETRIC_FACEBOOK_API_KEY
        },  # default headers
        timeout=100,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
        cache_default_ttl=432000,  # default cache ttl in seconds
        cache_methods=('GET', 'POST')  # methods to process for caching
    )
    api.add_resource(resource_name="search", resource_class=AsyncVetricSearchResource)
    api.add_resource(resource_name='profiles', resource_class=AsyncVetricProfilesResource)
    return api


@pytest.fixture
def redis_cached_async_rest_client_grayfox():
    api = LongRedisCachedAPI(
        api_root_url='https://eye-6adaad69fa3d.profileintel.com',  # base api url
        params={},  # default params
        headers={
            'x-api-key': settings.GRAYFOX_API_KEY
        },  # default headers
        timeout=100,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
    )

    # add users resource
    api.add_resource(resource_name='search', resource_class=GrayfoxSearchResource)
    return api

@pytest.mark.anyio
@pytest.mark.skip(reason="Vetric respond with 403 error. Review required")
async def test_cached_external_api_get(redis_cached_rest_client_vetric, fake):
    body = {
        "typed_query": f'{fake.first_name()} {fake.last_name()}'
    }
    for i in range(10):
        t1 = time.perf_counter(), time.process_time()
        response = redis_cached_rest_client_vetric.search.users(body=body)
        t2 = time.perf_counter(), time.process_time()
        interval = t2[0] - t1[0]
        # print(f" Real time: {interval:.2f} seconds")
        if i == 0:
            cold_request_time = interval
        else:
            assert cold_request_time > interval

    body = {
        "typed_query": f'{fake.first_name()} {fake.last_name()}'
    }
    for i in range(10):
        t1 = time.perf_counter(), time.process_time()
        response = redis_cached_rest_client_vetric.search.users(body=body)
        t2 = time.perf_counter(), time.process_time()
        interval = t2[0] - t1[0]
        # print(f" Real time: {interval:.2f} seconds")
        if i == 0:
            cold_request_time = interval
        else:
            assert cold_request_time > interval

    #fb_id = '100000927166631'
    #t1 = time.perf_counter(), time.process_time()
    #response = redis_cached_rest_client.profiles.about(fb_id) # noqa
    #t2 = time.perf_counter(), time.process_time()
    #print(f" Real time: {t2[0] - t1[0]:.2f} seconds")

@pytest.mark.anyio
@pytest.mark.skip(reason="Vetric respond with 403 error. Review required")
async def test_async_cached_external_api_get(redis_cached_async_rest_client_vetric, fake):
    body = {
        "typed_query": f'{fake.first_name()} {fake.last_name()}'
    }
    for i in range(10):
        t1 = time.perf_counter(), time.process_time()
        response = await redis_cached_async_rest_client_vetric.search.users(body=body)
        t2 = time.perf_counter(), time.process_time()
        interval = t2[0] - t1[0]
        # print(f" Real time: {interval:.2f} seconds")
        if i == 0:
            cold_request_time = interval
        else:
            assert cold_request_time > interval

    body = {
        "typed_query": f'{fake.first_name()} {fake.last_name()}'
    }
    for i in range(10):
        t1 = time.perf_counter(), time.process_time()
        response = await redis_cached_async_rest_client_vetric.search.users(body=body)
        t2 = time.perf_counter(), time.process_time()
        interval = t2[0] - t1[0]
        # print(f" Real time: {interval:.2f} seconds")
        if i == 0:
            cold_request_time = interval
        else:
            assert cold_request_time > interval

    #fb_id = '100000927166631'
    #t1 = time.perf_counter(), time.process_time()
    #response = redis_cached_async_rest_client.profiles.about(fb_id) # noqa
    #t2 = time.perf_counter(), time.process_time()
    #print(f" Real time: {t2[0] - t1[0]:.2f} seconds")

@pytest.mark.anyio
@pytest.mark.skip(reason="this test coul earn too much credits")
async def test_async_cached_external_api_post_form(redis_cached_async_rest_client_grayfox, fake):
    data = {
        "type": 'email',
        "query": fake.email()
    }
    for i in range(10):
        t1 = time.perf_counter(), time.process_time()
        response = await redis_cached_async_rest_client_grayfox.search.submit(data=data)
        t2 = time.perf_counter(), time.process_time()
        interval = round((t2[0] - t1[0]), 8)
        print(f" Real time: {interval:.2f} seconds")
        if i == 0:
            cold_request_time = interval
        else:
            assert cold_request_time > interval
