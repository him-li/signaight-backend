import json
from jina import Executor
from typing import List
from glom import glom

from core.documents import SearchRequestDoc, SearchResponseDoc
from core.clients.social_links.instagram import api, SlinksIgSpecs


class SocialLinksInstagramAPI(Executor):

    async def _search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        docs = []
        params = {"query": doc.name}
        try:
            response = await api.async_user.search(params=params)
            response_results = json.loads(response.body)
        except Exception as e:
            print(str(e))
            return docs

        results = response_results.get("result")

        spec = SlinksIgSpecs.spec

        for result in results:
            mapped_result = glom(result, spec)

            mapped_result["urn"] = doc.urn
            mapped_result["resource"] = doc.resource
            mapped_result["instagram_profile"]["instagram_id"] = format(
                str(mapped_result["instagram_profile"]["instagram_id"])
            )
            mapped_result["search_id"] = doc.search_id

            _doc = SearchResponseDoc(**mapped_result)
            docs.append(_doc)

        return docs
