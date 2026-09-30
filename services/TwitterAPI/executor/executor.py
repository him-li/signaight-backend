import asyncio
from jina import Executor, requests
from docarray import DocList
from typing import Dict, List

from core.database import init_db
from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    EnrichRequestDoc,
    EnrichResponseDoc
)
from .vtrc_twitter.vtrc_executor import VetricTwitterAPI



class TwitterAPI(Executor):

    source = "twitter"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio loops which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    source = 'twitter'

    @requests(on="/search")
    async def search(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        resource_name = parameters.get(
            "name", parameters.get("kwargs", {}).get("name"))
        flow_step = parameters.get("flow_step", parameters.get(
            "kwargs", {}).get("flow_step"))
        if not resource_name and self.source in parameters.get("source", []):
            resource_name = "{}_{}".format(parameters.get("resource"),
                                           self.source)
        if not resource_name:
            return None

        _docs = []
        # NOTE: backward compatibility. should removed soon
        if flow_step == 'enrich':
            for doc in docs:
                if doc.source == self.source:
                    result_list = await self._enrich(doc)
                    if result_list:
                        _docs = _docs + result_list
            _docs = DocList[EnrichResponseDoc](_docs)
        else:
            for doc in docs:
                # TODO: turn back event notification
                # search = await SearchEventModel.get(doc.search_id)
                # search.status = "Started"
                # await search.save()
                result_list = await self._search(doc, resource_name)
                if result_list:
                    self.logger.debug(f"Found {len(result_list)} {self.source} candidates for {doc.name}")  # noqa
                    _docs = _docs + result_list
                else:
                    self.logger.debug(
                        f"No found {self.source} candidates for {doc.name}")

            _docs = DocList[SearchResponseDoc](_docs)
        return _docs

    async def _search(
        self, doc: SearchRequestDoc, resource_name: str
    ) -> List[SearchResponseDoc]:
        if doc.resource == "vetric" or resource_name == "vetric_twitter":
            vetric_api = VetricTwitterAPI()
            return await vetric_api.search(doc)

    @requests(on="/enrich")
    async def enrich(
        self,
        docs: DocList[EnrichRequestDoc],
        parameters: Dict,
        **kwards
    ) -> DocList[EnrichResponseDoc]:
        resource = parameters.get("resource")
        _docs = []
        for doc in docs:
            if not doc.source == self.source:
                continue
            doc.resource = resource
            if result_doc := await self._enrich(doc):
                _docs.append(result_doc)
        resp_docs = DocList[EnrichResponseDoc](_docs)
        return resp_docs

    async def _enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc | None:
        if doc.resource == "vetric":
            vetric_api = VetricTwitterAPI()
            return await vetric_api.enrich(doc)
