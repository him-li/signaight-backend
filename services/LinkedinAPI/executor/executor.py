import pendulum
import asyncio
from jina import Executor, requests
from docarray import DocList
from typing import Dict, List

from core.documents import (SearchRequestDoc,
                            SearchResponseDoc,
                            EnrichRequestDoc,
                            EnrichResponseDoc)
from core.database import init_db
from core.models import SearchEventModel
from core.logging import logger
from core.models.utils import post_service_log

from .slinks_linkedin.slinks_executor import SocialLinksLinkedinAPI
from .epieos_linkedin.epieos_executor import EpieosLinkedinAPI
from .vtrc_linkedin.vtrc_executor import VetricLinkedinAPI



class LinkedinAPI(Executor):

    source = "linkedin"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio loops which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    @requests(on="/search")
    async def search(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        _docs = []
        resource_name = parameters.get("resource")
        if not resource_name and self.source in parameters.get("source", []):
            resource_name = "{}_{}".format(
                parameters.get("resource"), self.source)
        if not resource_name:
            return DocList[SearchResponseDoc]()

        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="LinkedinAPI",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")

        for doc in docs:
            self.logger.info(f"LinkedinAPI /search "
                             f"id:{doc.search_id} urn:{doc.urn}")
            attempt = 1
            while _docs == [] and attempt <= 6:
                attempt += 1
                try:
                    result_list = await self._search(doc, resource_name)
                    if isinstance(result_list, list):
                        _docs = _docs + result_list
                except Exception as e:
                    logger.info(e)
                    search = await SearchEventModel.get(doc.search_id)
                    search.retries += 1
                    search.status = "Started"
                    await search.save()

                    result_list = await self._search(doc, resource_name)
                    if isinstance(result_list, list):
                        _docs = _docs + result_list
            else:
                pass
        for _doc in _docs:
            _doc.source = self.source
        end_time = pendulum.now()
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="LinkedinAPI",
                        search_step="search",
                        message="Finished in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return DocList[SearchResponseDoc](_docs)

    async def _search(
        self, doc: SearchRequestDoc, resource_name: str
    ) -> List[SearchResponseDoc]:
        if ("social_links" in doc.resource and
                "slinks_linkedin" in resource_name):
            slinks_api = SocialLinksLinkedinAPI(doc)
            return await slinks_api._search(doc, resource_name)
        if doc.resource == "epieos" and resource_name == "epieos_linkedin":
            epieos_api = EpieosLinkedinAPI(doc)
            return await epieos_api._search(doc)
        if doc.resource == "vetric" or resource_name == "vetric_linkedin":
            vetric_api = VetricLinkedinAPI()
            return await vetric_api.search(doc)

    @requests(on="/enrich")
    async def enrich(
        self,
        docs: DocList[EnrichRequestDoc],
        parameters: Dict,
        **kwards
    ) -> DocList[EnrichResponseDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="LinkedinAPI",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        _docs = DocList[EnrichResponseDoc]()
        resource = parameters.get('resource', [])
        if isinstance(resource, str):
            resource = [resource]

        for doc in docs:
            self.logger.info(f"LinkedinAPI /enrich "
                             f"id:{doc.search_id} urn:{doc.urn}")
            if doc.resource == "vetric" or "vetric" in resource:
                if result_doc := await self._enrich(doc):
                    result_doc.search_id = doc.search_id
                    result_doc.source = self.source
                    _docs.append(result_doc)
        end_time = pendulum.now()
        for i, doc in enumerate(_docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="LinkedinAPI",
                        search_step="enrich",
                        message="Finished in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(_docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return _docs

    async def _enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc:
        vetric_api = VetricLinkedinAPI()
        return await vetric_api.enrich(doc)
