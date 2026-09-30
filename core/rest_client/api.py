from simple_rest_client.api import API as OriginAPI

from .resource import Resource, AsyncResource


class API(OriginAPI):

    def set_headers(self, headers: dict) -> None:
        if not isinstance(headers, dict):
            return
        for key, value in headers.items():
            if value:
                self.headers[key] = value


class RedisCachedAPI(API):
    '''
        Usage example:
            from core.rest_client import Resource, RedisCachedAPI

            class GetBinResource(Resource):
                actions = {
                    "echo": {"method": "GET", "url": "/get"},
                }

            api = RedisCachedAPI(
                api_root_url='https://httpbin.org/get',  # base api url
                params={},  # default params
                timeout=100,  # default timeout in seconds
                append_slash=False,  # append slash to final url
                json_encode_body=True,  # encode body as json
                cache_default_ttl=31556952, # default cache ttl in seconds for 1 year
                cache_methods=('GET', 'POST') # methods to process for caching
            )
            api.add_resource(resource_name="getbin", resource_class=GetBinResource)

            #request with automatic detection for cached value, request will made only
            #if cache is empty
            response = api.getbin.echo()

            #request with ommiting cached response at any case. Useful to get fresh data
            #from source
            response = api.getbin.echo(headers={"cache-control": "no-cache"})
    '''

    def __init__(
        self,
        api_root_url=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=False,
        json_encode_body=False,
        ssl_verify=None,
        cache_default_ttl=5,
        cache_methods=('GET', 'POST'),
        cache_statuses=[200, 201, 202, 204, 301, 308],
        force_cache=True
    ):
        self.api_root_url = api_root_url
        self.params = params or {}
        self.headers = headers or {}
        self.timeout = timeout
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body
        self.ssl_verify = True if ssl_verify is None else ssl_verify
        self.cache_default_ttl = cache_default_ttl
        self.cache_methods = cache_methods
        self.cache_statuses = cache_statuses
        self.force_cache = force_cache
        self._resources = {}

    def add_resource(
        self,
        api_root_url=None,
        resource_name=None,
        resource_class=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=None,
        json_encode_body=None,
        ssl_verify=None,
        cache_default_ttl=None,
        cache_methods=None,
        cache_statuses=None,
        force_cache=None
    ):
        resource_class = resource_class or Resource or AsyncResource
        resource = resource_class(
            api_root_url=api_root_url if api_root_url is not None else self.api_root_url,
            resource_name=resource_name,
            params=params if params is not None else self.params,
            headers=headers if headers is not None else self.headers,
            timeout=timeout if timeout is not None else self.timeout,
            append_slash=append_slash if append_slash is not None else self.append_slash,
            json_encode_body=json_encode_body if json_encode_body is not None else self.json_encode_body,
            ssl_verify=ssl_verify if ssl_verify is not None else self.ssl_verify,
            default_ttl=cache_default_ttl if cache_default_ttl is not None else self.cache_default_ttl,
            cacheable_methods=cache_methods if cache_methods is not None else self.cache_methods,
            cacheable_status_codes=cache_statuses if cache_statuses is not None else self.cache_statuses,
            force_cache=True if force_cache is not None else self.force_cache
        )
        self._resources[resource_name] = resource
        resource_valid_name = self.correct_attribute_name(resource_name)
        setattr(self, resource_valid_name, resource)


class LongRedisCachedAPI(RedisCachedAPI):

    def __init__(
        self,
        api_root_url=None,
        params=None,
        headers=None,
        timeout=20,
        append_slash=False,
        json_encode_body=False,
        ssl_verify=None,
        cache_default_ttl=432000,
        cache_methods=('GET', 'POST'),
        cache_statuses=[200, 201, 202, 204, 301, 308],
        force_cache=True
    ):
        super().__init__(
            api_root_url,
            params,
            headers,
            timeout,
            append_slash,
            json_encode_body,
            ssl_verify,
            cache_default_ttl,
            cache_methods,
            cache_statuses,
            force_cache
        )
