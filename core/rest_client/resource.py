import json
import httpx
import hishel
import httpcore

from simple_rest_client.resource import (
    Resource as OriginResource,
    AsyncResource as OriginAsyncResource,
)
from types import MethodType

from core.redis import get_redis_client
from .cache import get_advanced_cache_key
from .models import Request
from .request import make_drill_request, make_async_drill_request


class Resource(OriginResource):
    """Modified simple_rest_client Resource to support caching features on top
    of httpx library

    Arguments:
        default_ttl: int - default cache ttl in seconds. Default: 5 seconds
        namespace: str - Cahe namespace. Default: 'external-requests'
        cacheable_methods: tuple, list - HTTP methods for cache.
                            Default: ('GET',)

    """

    def __init__(self, *args, **kwargs):
        default_ttl = int(kwargs.pop("default_ttl", 5))
        cacheable_methods = kwargs.pop("cacheable_methods", ("GET",))
        cacheable_status_codes = kwargs.pop("cacheable_status_codes", [200, 301, 308])
        force_cache = kwargs.pop("force_cache", True)
        super().__init__(*args, **kwargs)
        redis_client = get_redis_client()
        if redis_client:
            storage = hishel.RedisStorage(client=redis_client, ttl=default_ttl)
            controller = hishel.Controller(
                cacheable_methods=cacheable_methods,
                cacheable_status_codes=cacheable_status_codes,
                force_cache=force_cache,
                key_generator=get_advanced_cache_key,
            )
            self.client = hishel.CacheClient(storage=storage, controller=controller)
        else:
            self.client = httpx.Client(verify=self.ssl_verify)

        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        def action_method(
            self,
            *args,
            body=None,
            data=None,
            params=None,
            headers=None,
            action_name=action_name,
            **kwargs,
        ):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            request_headers = headers or {}
            request_params = params or {}
            request_params.update(self.params)
            request_headers.update(self.headers)
            # TODO: maybe find better solution with form-data
            if data and isinstance(data, dict):
                body = "&".join(f"{key}={value}" for key, value in data.items())
                request_headers["Content-Type"] = "application/x-www-form-urlencoded"
            request = Request(
                url=url,
                method=method,
                params=request_params,
                body=body,
                headers=request_headers,
                timeout=self.timeout,
                kwargs=kwargs,
            )
            return make_drill_request(self.client, request)

        setattr(self, action_name, MethodType(action_method, self))


class AsyncResource(OriginAsyncResource):
    """Modified simple_rest_client Resource to support caching features on top
    of httpx library

    Arguments:
        default_ttl: int - default cache ttl in seconds. Default: 5 seconds
        namespace: str - Cahe namespace. Default: 'external-requests'
        cacheable_methods: tuple, list - HTTP methods for cache.
                            Default: ('GET',)
    """

    def __init__(self, *args, **kwargs):
        default_ttl = int(kwargs.pop("default_ttl", 5))
        cacheable_methods = kwargs.pop("cacheable_methods", ("GET",))
        cacheable_status_codes = kwargs.pop("cacheable_status_codes", [200, 301, 308])
        force_cache = kwargs.pop("force_cache", True)
        super().__init__(*args, **kwargs)
        self.redis_client = get_redis_client(async_mode=True)
        if self.redis_client:
            storage = hishel.AsyncRedisStorage(
                client=self.redis_client, ttl=default_ttl
            )
            controller = hishel.Controller(
                cacheable_methods=cacheable_methods,
                cacheable_status_codes=cacheable_status_codes,
                force_cache=force_cache,
                key_generator=get_advanced_cache_key,
            )
            self.client = hishel.AsyncCacheClient(
                storage=storage, controller=controller
            )

        else:
            self.client = httpx.AsyncClient(verify=self.ssl_verify)

        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        async def action_method(
            self,
            *args,
            body=None,
            data=None,
            params=None,
            headers=None,
            action_name=action_name,
            **kwargs,
        ):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            request_headers = headers or {}
            request_params = params or {}
            request_params.update(self.params)
            request_headers.update(self.headers)
            # TODO: maybe find better solution with form-data
            if data and isinstance(data, dict):
                body = "&".join(f"{key}={value}" for key, value in data.items())
                request_headers["Content-Type"] = "application/x-www-form-urlencoded"
            delete_cache = False
            if kwargs.get("no_cache"):
                delete_cache = True
            kwargs.pop("no_cache", None)
            request = Request(
                url=url,
                method=method,
                params=request_params,
                body=body,
                headers=request_headers,
                timeout=self.timeout,
                kwargs=kwargs,
            )
            if delete_cache:
                try:
                    cache_request = httpcore.Request(
                        method=method.upper().encode(),
                        url=url.encode() if isinstance(url, str) else url,
                    )
                    cache_key = get_advanced_cache_key(cache_request, f"b'{json.dumps(body)}'" if body else None)
                    cache_key = cache_key[:110]
                    async def delete_by_prefix(prefix: str):
                        pattern = f"{prefix}*"
                        keys = await self.redis_client.keys(pattern)
                        if keys:
                            await self.redis_client.delete(*keys)
                        return len(keys)
                    result = await delete_by_prefix(cache_key)
                    print("Deleted cache result:", result, cache_key)
                except Exception as e:
                    print("Error deleting cache:", e)
            return await make_async_drill_request(self.client, request)

        setattr(self, action_name, MethodType(action_method, self))
