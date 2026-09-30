from jina import Executor, requests
from docarray import DocList
from typing import Dict
from core.documents import SearchRequestDoc, EnrichRequestDoc

class SearchIn(Executor):

    @requests(on="/search")
    async def search_merger(
        self,
        docs: DocList[SearchRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchRequestDoc]:
        for doc in docs:
            self.logger.info(f"SearchIn /search id:{doc.search_id} urn:{doc.urn}")
        return docs

    @requests(on="/enrich")
    async def enrich_merger(
        self,
        docs: DocList[EnrichRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[EnrichRequestDoc]:
        for doc in docs:
            self.logger.info(f"SearchIn /search id:{doc.search_id} urn:{doc.urn}")
        return docs
