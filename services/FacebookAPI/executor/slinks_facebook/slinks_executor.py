import json
from jina import Executor
from typing import List
from glom import glom

from core.documents import SearchRequestDoc, SearchResponseDoc
from core.clients.social_links.facebook import api, SlinksFbSpecs


class SocialLinksFacebookAPI(Executor):

    async def _search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        docs = []
        try:
            response = await api.async_search.users(
                params={
                    "fullname": doc.name,
                    # "city": doc.city,
                    # "education": doc.education,
                    # "company": doc.work,
                    "limit": 10,
                }
            )
            response_results = json.loads(response.body)
        except Exception as e:
            print(e)
            return docs

        results = response_results.get("result")

        spec = SlinksFbSpecs.spec

        profiles = [profile for profile in results if len(results) <= 16 and
                    not None]

        for profile in profiles:
            mapped_profile = glom(profile, spec)

            mapped_profile["urn"] = doc.urn
            mapped_profile["resource"] = doc.resource
            mapped_profile["search_id"] = doc.search_id

            _doc = SearchResponseDoc(**mapped_profile)
            docs.append(_doc)

        return docs
