import asyncio
import pendulum
import sys
from jina import Executor, requests
from docarray import DocList
from typing import Dict

from core.database import init_db
from core.documents import (SearchRequestDoc,
                            SearchResponseDoc,
                            EnrichResponseDoc,
                            EnrichRequestDoc
                            )
from core.logging import logger
from core.models.utils import post_service_log
from .scrapers.xing import XingPlaywrightScenario
from .scrapers.eu_most_wanted import EUMostWantedPlaywrightScenario
from .scrapers.interpol import InterpolPlaywrightScenario
from .scrapers.google_search import GoogleSearchScrapePlaywrightScenario
from .config import settings



class WebScraper(Executor):

    search_sources = {
        "xing": {
            "class": XingPlaywrightScenario,
            "params": {
                "username": settings.XING_USERNAME,
                "password": settings.XING_PASSWORD,
            }
        },
        "eumw": EUMostWantedPlaywrightScenario,
        "interpol": InterpolPlaywrightScenario,
        "google": {
            "class": GoogleSearchScrapePlaywrightScenario,
            "params": {
                "serp_proxy_uri": settings.OXYLABS_SERP_PROXY_URI,
            }
        }
    }

    enrich_sources = {
        "xing": {
            "class": XingPlaywrightScenario,
            "params": {
                "username": settings.XING_USERNAME,
                "password": settings.XING_PASSWORD,
            }
        },
        "interpol": InterpolPlaywrightScenario,
        "google": {
            "class": GoogleSearchScrapePlaywrightScenario,
            "params": {
                "serp_proxy_uri": settings.OXYLABS_SERP_PROXY_URI,
            }
        }
    }

    google_default_search_fields = [
        ['f_name', 'l_name', 'work'],
        ['f_name', 'l_name', 'education'],
        ['f_name', 'l_name', 'bio'],
        ['f_name', 'l_name', 'email_address'],
    ]
    google_default_rare_name_fields = ['f_name', 'l_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio
        # loops which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    @requests(on="/search")
    async def search(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        *args,
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="WebScraper",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        sources = parameters.get(
            "source", parameters.get("kwargs", {}).get("sources", []))
        # enable all services if there is no any came from flow
        if not sources:
            sources = self.search_sources.keys()
        _docs = DocList[SearchResponseDoc]([])
        for doc in docs:
            self.logger.info(
                f"WebScraper /search id:{doc.search_id} urn:{doc.urn}")
            for source, scenario in self.search_sources.items():
                if source not in sources:
                    continue
                params = parameters.get(source, {})
                if isinstance(scenario, dict):
                    params = {
                        **scenario.get("params", {}),
                        **params
                    }
                    scenario = scenario.get("class")
                # continue loop if scenario does not set properly
                self.logger.info(f"WebScrapper {source}: search has been started"
                                 f" for search id {doc.search_id}")
                if not scenario:
                    continue
                try:
                    if source == 'google':
                        google_search_fields = parameters.get(
                            'google_search_fields', parameters.get(
                                'kwargs', {}).get('google_search_fields')
                        )
                        if not google_search_fields:
                            google_search_fields = (
                                self.google_default_search_fields)
                        google_rare_name_fields = parameters.get(
                            'google_rare_name_fields', parameters.get(
                                'kwargs', {}).get('google_rare_name_fields'))
                        if not google_rare_name_fields:
                            google_rare_name_fields = (
                                self.google_default_rare_name_fields)
                        if doc.is_rare_name:
                            google_search_fields.append(
                                self.google_default_rare_name_fields)
                        for search_field in google_search_fields:
                            result_list = await scenario.search(
                                doc=doc,
                                **params,
                                q=search_field)
                            if result_list:
                                self.logger.info(
                                    f"WebScrapper {source}: Found"
                                    f" {len(result_list)} {scenario} candidates"
                                    f" for search id {doc.search_id}")
                                _docs = _docs + result_list
                            else:
                                self.logger.debug(
                                    f"WebScrapper {source}: There no found "
                                    f"candidates with {scenario}"
                                    f" for search id {doc.search_id}")  # noqa
                    else:
                        result_list = await scenario.search(doc=doc, **params)
                        if result_list:
                            self.logger.info(
                                f"WebScrapper {source}: Found"
                                f" {len(result_list)} {scenario} candidates"
                                f" for search id {doc.search_id}")
                            _docs = _docs + result_list
                        else:
                            self.logger.debug(
                                        f"WebScrapper {source}: There no found"
                                        f" candidates with {scenario}"
                                        f" for search id {doc.search_id}")  # noqa
                except Exception as e:
                    self.logger.error(f"WebScrapper {source}: {str(e)}"
                                      f" for search id {doc.search_id}")
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="WebScrapper",
                        search_step="search",
                        message=(f"WebScrapper {source}: {str(e)}"
                                 f" for search id {doc.search_id}"),
                        docs_count=len(docs),
                        step_point="error"
                    )
                    continue
        if _docs:
            _docs = DocList[SearchResponseDoc](_docs)

        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    end_time = pendulum.now()
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="WebScraper",
                        search_step="search",
                        message="Finished",
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return _docs

    @requests(on="/enrich")
    async def enrich(
        self,
        docs: DocList[EnrichRequestDoc],
        parameters: Dict,
        *args,
        **kwargs
    ) -> DocList[EnrichResponseDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="WebScraper",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        # TODO: once stuck process bug is fixed, reenable function
        sources = parameters.get(
            "source", parameters.get("kwargs", {}).get("sources", []))
        # enable all services if there is no any came from flow
        _docs = DocList[EnrichResponseDoc]([])
        for doc in docs:
            self.logger.info(
                f"WebScraper /enrich id:{doc.search_id} urn:{doc.urn}")
            try:
                source = doc.source
            except Exception:
                continue
            if source not in sources:
                continue
            if not (scenario := self.enrich_sources.get(source)):
                continue
            params = parameters.get(source, {})
            if isinstance(scenario, dict):
                params = {
                    **scenario.get("params", {}),
                    **params
                }
                scenario = scenario.get("class")
            # continue loop if scenario does not set properly
            if not scenario:
                continue
            try:
                if response := await scenario.enrich(doc=doc, **params):
                    response['urn'] = doc.urn
                    response['source'] = source
                    _docs.append(EnrichResponseDoc(**response))
            except Exception as e:
                self.logger.info(e)
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="WebScrapper",
                    search_step="enrich",
                    message=(f"WebScrapper enrich error: {str(e)}"),
                    docs_count=len(docs),
                    step_point="error"
                )
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    end_time = pendulum.now()
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="WebScraper",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return _docs
