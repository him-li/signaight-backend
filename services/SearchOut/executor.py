from jina import Executor, requests
from docarray import DocList

from core.documents import SearchResponseDoc


class SearchOut(Executor):

    @requests
    async def search_to_enrich(
        self,
        docs: DocList[SearchResponseDoc],
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        return docs
