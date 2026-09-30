import asyncio
import hishel
import re
import uuid
import random
import os
from glom import glom, Coalesce
from collections import defaultdict
from pydantic import AnyHttpUrl
from parsel import Selector
from typing import List
from urllib.parse import (quote, urlparse,
                          urlunparse, parse_qs, urlsplit)

from .decorators import async_playwright_run
from core.clients.ds_app import api as ds_app_api
from core.dbclient import client
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
    EnrichResponseDoc
)
from core.logging import logger
from core.models import PersonModel, WebSearch, WebSearchModel
from core.utils import parse_urn, build_person_urn

# NOTE: how it works???
from .helpers.websites_helper import WEBSITES

web_search_spec = {
    'url_path': Coalesce('source', default=None),
    'content': Coalesce('content', default=None),
    'images': Coalesce('images', default=None),
}


class GoogleSearchScrapePlaywrightScenario:

    allowed_exts = ['txt', 'htm', 'html', 'asp', 'aspx', 'php']

    @classmethod
    async def search(
        cls,
        doc: SearchRequestDoc,
        *args,
        **kwargs
    ) -> None:
        proxy_api_key = kwargs.get('proxy_api_key')
        if not proxy_api_key:
            print("There is no scrape.do proxy api key defined")
            return None
        try:
            person_id = parse_urn(doc.urn)
            person_id = uuid.UUID(person_id)
        except Exception:
            return None
        person = await PersonModel.get(person_id)
        pages = int(kwargs.get('pages', 2))
        # TODO: implement query fields support
        # query_fields = parameters.get('query_fields', ['f_name'])  # noqa
        query = doc.name
        if not query or not person:
            return None

        results = []
        for page in range(1, pages+1):
            print(f"SERP for: {doc.name} page {page}")
            results.extend(await cls._search_scrape(query,
                                                    proxy_api_key, page=page))

        if results:
            sources = []
            web_searches = []
            try:
                for i, result in enumerate(results):
                    source_path = urlparse(result.source).path
                    ext = os.path.splitext(source_path)[1]
                    # check for the same source and prevent appear it in list
                    # and everything is binary file should dropped
                    if (not result.source in sources
                        and not cls._is_profile_url(str(result.source))
                            and (not ext or ext.lstrip('.').lower() in cls.allowed_exts)):
                        web_searches.append(WebSearchModel(
                            **{
                                **result.model_dump(),
                                **{
                                    'person': person,
                                    'search_id': doc.search_id
                                }
                            }))
                        sources.append(result.source)
                if web_searches:
                    async with client.start_session() as session:
                        async with await session.start_transaction():
                            await WebSearchModel.insert_many(web_searches,
                                                             session=session)
            except Exception as e:
                print(
                    f"Unable to save WebSearch entities in database: {str(e)}")
        print(f"SERP for {doc.name} finished")
        return None

    @classmethod
    @async_playwright_run()
    async def enrich(
        cls,
        context,
        doc: EnrichRequestDoc,
        *args,
        **kwargs
    ) -> List[EnrichResponseDoc]:

        page = await context.new_page()
        web_searches = WebSearchModel.find(
            WebSearchModel.search_id == doc.search_id
        )
        logger.info(f"Postprocess: {kwargs.get('postprocess', False)}")
        if not kwargs.get('postprocess', False):
            async for web_search in web_searches:
                try:
                    url = AnyHttpUrl(web_search.source)
                except Exception as e:
                    logger.info(e)
                logger.info(f"Processing: {str(url)}")
                main_content, image_urls = None, None
                try:
                    if any((web := website) in url.host for website
                           in WEBSITES.keys()):
                        main_content, image_urls = await WEBSITES[web](
                            url=str(url))
                    else:
                        main_content, image_urls = await cls._scrape_website(
                            page, str(url))
                    if main_content:
                        web_search.content = str(main_content)
                    else:
                        web_search.content = ""
                    web_search.images = []
                    if image_urls:
                        web_search.images = [
                            image for image in image_urls
                            if (image and (image.startswith('http://')
                                           or image.startswith('https://')
                                           or image.startswith('s3://')))]
                    web_search = await web_search.save()
                except Exception as e:
                    # TODO: maybe track failed to get pages with special flag in db here
                    logger.info(e)
        else:
            try:
                # Prepare the web_searches for the ds app
                print("in post process")
                web_searches_list = []
                web_searches = await web_searches.to_list()
                for i, web_search in enumerate(web_searches):
                    if not web_search.content or not web_search.images:
                        del web_searches[i]
                        continue
                    _web_search = web_search.model_dump(mode='json')
                    # TODO: add sanitizing here
                    _web_search = glom(_web_search, web_search_spec)
                    web_searches_list.append(_web_search)
                try:
                    person_id = parse_urn(doc.urn)
                    person_id = uuid.UUID(person_id)
                except Exception:
                    return None
                person = await PersonModel.get(person_id)

                body = {
                    "web_searches": web_searches_list,
                    "person": person.model_dump(mode='json'),
                }

                body['hash'] = str(body)

                response = await (
                    ds_app_api.async_ds_request.search_engine_matching(
                        body=body,
                        headers={
                            'x-remote-context': build_person_urn(person.id)}
                    ))
                response_body = response.body
                matches = response_body['matches']
                for is_match, web_search in zip(matches, web_searches):
                    web_search.is_match = is_match['is_match']
                    try:
                        await web_search.save()
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))

        return None

    @classmethod
    async def _search_scrape(cls, query: str, proxy_api_key: str, page=1):
        """scrape search results for a given keyword"""
        # retrieve the SERP
        url = (f"https://www.google.com/search?hl=en&q={quote(query)}"
                    + (f"&start={10*(page-1)}" if page > 1 else ""))  # noqa
        results = defaultdict(list)
        proxyModeURL = f"http://{proxy_api_key}:@proxy.scrape.do:8080"
        async_client = hishel.AsyncCacheClient(
            headers={
                # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",  # noqa
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",  # noqa
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",  # noqa
                # TODO: maybe find way to decode compressed pages
                # "Accept-Encoding": "gzip, deflate, br",
                "Accept-Encoding": "identity",
                "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
                "Upgrade-Insecure-Requests": "1",
            },
            proxies={
                "all://": proxyModeURL,
            },
            timeout=60,  # timeout is important for this value
            follow_redirects=True,
            verify=False,
            http2=True,  # use HTTP/2
        )
        async with async_client as ac:
            try:
                response = await ac.get(url)
            except Exception as e:
                logger.info(e)
            # TODO: maybe better check for status response
            # assert response.status_code==200, f"failed status_code={response.status_code}"  # noqa

            for _ in range(5):
                if response.status_code != 200:
                    await asyncio.sleep(random.randint(1, 5))
                    try:
                        response = await ac.get(url)
                    except Exception as e:
                        logger.info(e)
                else:
                    break

            if not response:
                raise Exception(f"request to {url} failed without responding")

            if response.status_code != 200:
                raise Exception(f"failed status_code={response.status_code}")

            # parse SERP for search result data
            selector = Selector(response.text)

            search = cls._search_results_parse(selector)

            if search:
                return search

            return []

    @classmethod
    def _search_results_parse(cls, selector: Selector):
        """Parse search results from Google search page"""
        results = []

        # Multiple XPath options for result containers
        container_xpaths = [
            "//div[@class='g']",
            "//div[contains(@class, 'yuRUbf')]",
            "//div[@data-sokoban-container]",
        ]

        for xpath in container_xpaths:
            containers = selector.xpath(xpath)
            if containers:
                break
        else:
            return results

        for container in containers:
            try:
                # Title extraction
                title_xpaths = [
                    ".//h3[contains(@class, 'r')]/a//text()",
                    ".//h3//text()",
                    ".//div[contains(@class, 'vvjwJb')]//text()",
                    ".//h3/div/text()",
                ]
                title = None
                for xpath in title_xpaths:
                    title = "".join(container.xpath(xpath).getall()).strip()
                    if title:
                        break

                # URL extraction
                url_xpaths = [
                    ".//div[@class='r']/a/@href",
                    ".//div[contains(@class, 'yuRUbf')]//a/@href",
                    ".//a/@href"
                ]
                url = None
                for xpath in url_xpaths:
                    url = container.xpath(xpath).get()
                    if url:
                        url = cls._extract_valid_url(url)
                        break

                # Preview extraction
                preview_xpaths = [
                    ".//div[@data-sncf='1']//text()",
                    ".//div[@class='s']//text()",
                    ".//div[contains(@class, 'VwiC3b')]//text()",
                    ".//div[contains(@class, 'IsZvec')]//text()",
                    "./div[2]//text()",
                ]

                preview = None
                for xpath in preview_xpaths:
                    preview_parts = container.xpath(xpath).getall()
                    preview = ' '.join([part.strip()
                                       for part in preview_parts if
                                       part.strip()])
                    if preview:
                        break

                if not preview:
                    # If all else fails, get all text that's not in the title
                    all_text = ' '.join(container.xpath(".//text()").getall())
                    title_text = ' '.join(
                        container.xpath(".//h3//text()").getall())
                    preview = all_text.replace(title_text, '').strip()

                if title and url:
                    results.append(WebSearch(title=title,
                                             source=url, preview=preview))

            except Exception as e:
                print(f"Error parsing search result: {str(e)}")

        return results

    @classmethod
    def _extract_valid_url(cls, url):

        if url.startswith("/url?"):
            # Parse the URL to get the actual URL
            parsed_url = parse_qs(urlsplit(url).query)
            valid_url = parsed_url.get('url', [None])[0]
            parsed = urlparse(valid_url)
            if all([parsed.scheme, parsed.netloc]):
                return valid_url

        parsed = urlparse(url)

        if all([parsed.scheme, parsed.netloc]):
            return url

        return None

    @classmethod
    async def _scrape_website(cls, page, url):
        await page.goto(url)
        await page.wait_for_load_state()
        await asyncio.sleep(2)

        parsed_url = urlparse(url)
        html = await page.content()
        selector = Selector(html)

        # TODO: Figure out how to remove irrelevant images
        image_urls = selector.xpath("//img/@src").getall()
        for i, img_url in enumerate(image_urls):
            if img_url:
                if not img_url.startswith('http'):
                    image_urls[i] = urlunparse(
                        ("http", parsed_url.netloc, img_url, "", "", ""))

        selector = Selector(selector.xpath("//body").get())
        selector = cls._remove_junk_parsel(selector)
        main_content = cls._extract_main_content(selector)

        # Filtering links by simple regex to decrease images list based on extension
        positive_pattern = re.compile(
            "(jpe?g|png|gif|webp)", flags=re.IGNORECASE)
        negative_pattern = re.compile(
            "(icon|flag|logo|base64|spacer)", flags=re.IGNORECASE)
        image_urls = [img for img in image_urls
                      if img and re.search(positive_pattern, img)
                      and not re.search(negative_pattern, img)]

        return main_content, image_urls

    @classmethod
    def _remove_junk_parsel(cls, selector):
        # Remove unwanted tags using XPath
        for tag in ['script', 'style', 'header', 'footer', 'nav', 'aside',
                    'noscript', 'svg', 'a', 'link']:
            selector.xpath(f'//{tag}').drop()
        return selector

    @classmethod
    def _extract_main_content(cls, selector):
        body_text = "".join(selector.xpath('.//text()').getall())
        # Replace sequence of spaces containing newlines with a single newline
        body_text = re.sub(r'\s*\n\s*', '\n', body_text)
        # Replace sequences of whitespace without newlines with a single space
        body_text = re.sub(r'[^\S\n]+', ' ', body_text)

        return body_text or "Main content not found."

    @classmethod
    def _convert_uuids_to_strings(cls, obj):
        if isinstance(obj, dict):
            return {k: cls.convert_uuids_to_strings(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls.convert_uuids_to_strings(item) for item in obj]
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return str(obj)

    @classmethod
    def _is_profile_url(cls, url):
        profile_url_patterns = {
            'facebook_profile': re.compile(
                r'^https://(www|m)\.facebook\.com/[^/]+/?(\?.+)?$'),
            'instagram_profile': re.compile(
                r'^https://www\.instagram\.com/[^/]+/?(\?.+)?$'),
            'linkedin_profile': re.compile(
                r'^https://([a-z]{2,3}\.)?linkedin\.com/in/[^/]+(/[a-z]{2})?/?(\?.+)?$'),
            'twitter_profile': re.compile(
                r'^https://(www\.)?(twitter|x|mobile\.twitter)\.com/[^/]+/?$'),
            'xing_profile': re.compile(
                r'^https://www\.xing\.com/profile/[^/]+/?$')
        }

        for platform, pattern in profile_url_patterns.items():
            if pattern.match(url):
                return True
        return False
