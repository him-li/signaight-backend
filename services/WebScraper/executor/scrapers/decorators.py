import json
import hashlib
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from pydantic import AnyHttpUrl
from pydantic_core import Url
from typing import Union

# if run as internal part of flow in threaded mode
from ..config import settings

redis_cache_client = None
try:
    from core.redis import get_redis_client
    if settings.REDIS_URI:
        redis_cache_client = get_redis_client(async_mode=True)
except Exception:
    pass

# NOTE: currently stable tests supported only with firefox
def async_playwright_run(
    engine: str = "firefox",
    proxy_uri: Union[AnyHttpUrl, str, None] = settings.OXYLABS_PROXY_URI,
    user_agent: str = None,
    timezone: str = settings.XING_USER_TIMEZONE,
    locale: str = 'en-US',
    timeout: int | float | None = 600
):
    def decorator(func):
        async def wrapper(cls, *args, **kwargs):
            async with async_playwright() as playwright:
                if not user_agent:
                    match engine:
                        case "chrome", "chromium":
                            _user_agent = (
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                                " (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                            )
                        case "firefox":
                            _user_agent = ("Mozilla/5.0 (X11; Linux x86_64; rv:10.0)"
                                "Gecko/20100101 Firefox/10.0")
                        case "webkit":
                            _user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1")
                        case _:
                            _user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0)"
                                "Gecko/20100101 Firefox/40.0")
                else:
                    _user_agent = user_agent
                if engine == 'chrome':
                    instance = getattr(playwright, 'chromium')
                else:
                    instance = getattr(playwright, engine)
                browser = await instance.connect(
                    str(settings.PLAYWRIGHT_BROWSER_SERVER),
                    timeout=30000
                )
                context_args = {
                    'viewport': {'width': 1600, 'height': 1200},
                    'user_agent': _user_agent,
                    'locale': locale,
                    'accept_downloads': False,
                    'bypass_csp': True,
                    'ignore_https_errors': True,
                    # 'timezone_id': timezone,
                    # 'geolocation': {"latitude": 50.4500336,
                    #                 "longitude": 30.5241361},
                    # 'permissions': ["geolocation"],
                }
                # Add proxy if have credentials
                if proxy := proxy_uri:
                    # NOTE: AnyHttpUrl is type, but variable is always
                    # Url object
                    if not isinstance(proxy, Url):
                        proxy = AnyHttpUrl(proxy)
                    context_args['proxy'] = {
                        'server': (
                            f"{proxy.scheme}://{proxy.host}:{proxy.port}"
                            if proxy.port else f"{proxy.scheme}://{proxy.host}"
                        ),
                        'bypass': ("google.com, .google.com, .gstatic.com,"
                                   " .googletagmanager.com, .doubleclick.net,"
                                   " .spoteffects.net"),
                        'username': proxy.username,
                        'password': proxy.password,
                    }
                # restore storage_state here in new_context with redis
                # or local state
                # https://playwright.dev/python/docs/api/class-browser#browser-new-context-option-storage-state
                cache_key = None
                if (username := kwargs.get('username')) and (
                        password := kwargs.get('password')):
                    # TODO: maybe add proxy data to footprint
                    footprint = f"{username}-{password}"
                    if proxy:
                        footprint = f"{footprint}-{proxy}"
                    cache_key = "scraping-session-{}-{}".format(
                        cls.__name__, hashlib.sha256(
                            footprint.encode()).hexdigest())
                if cache_key:
                    if redis_cache_client:
                        if (storage_state := await redis_cache_client.get(
                                cache_key)):
                            context_args['storage_state'] = json.loads(
                                storage_state)
                    else:
                        state_file = Path(f'/tmp/{cache_key}.json')
                        if state_file.exists():
                            context_args['storage_state'] = state_file

                context = await browser.new_context(**context_args)
                context.set_default_navigation_timeout(30000)
                context.set_default_timeout(60000)

                # Do all stuff here
                try:
                    response = await asyncio.wait_for(
                        func(cls, context, *args, **kwargs),
                        timeout=timeout
                    )
                except asyncio.TimeoutError:
                    print(f"Function '{func.__name__}' timed out after {timeout} seconds")
                    return []  # or raise custom exception
                #response = await func(cls, context, *args, **kwargs)

                # save storage state after process here with redis
                # or local state
                # https://playwright.dev/python/docs/api/class-browser#browser-new-context-option-storage-state
                if cache_key:
                    if redis_cache_client:
                        if storage_state := await context.storage_state():
                            context_args[
                                'storage_state'] = await (
                                    redis_cache_client.set(
                                        cache_key,
                                        json.dumps(storage_state)))
                    else:
                        await context.storage_state(
                            path=f"/tmp/{cache_key}.json")
                await context.close()
                await browser.close()
            return response
        return wrapper
    return decorator
