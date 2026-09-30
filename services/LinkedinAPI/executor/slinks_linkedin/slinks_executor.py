import json
from jina import Executor
from typing import List
from glom import glom

from core.documents import SearchRequestDoc, SearchResponseDoc
from core.clients.social_links.linkedin import api, SlinksLiSpecs


class SocialLinksLinkedinAPI(Executor):

    async def _search(
        self, doc: SearchRequestDoc, resource_name: str
    ) -> List[SearchResponseDoc]:
        docs = []

        email_params = {"query": doc.email_address}
        name_params = {"first_name": doc.f_name, "last_name": doc.l_name}

        try:
            if (
                doc.resource == "social_links_email"
                and resource_name == "slinks_linkedin_email"
            ):
                response = await api.async_search.email_to_profile(params=email_params)
            elif (
                doc.resource == "social_links_emailV2"
                and resource_name == "slinks_linkedin_emailV2"
            ):
                response = await api.async_search.lookup_by_email_v2(params=email_params)
            elif (
                doc.resource == "social_links_name"
                and resource_name == "slinks_linkedin_name"
            ):
                response = await api.async_search.search_people_new(params=name_params)
            response_results = json.loads(response.body)
        except Exception as e:
            print(str(e))
            return docs

        if response_results.get("result"):
            results = response_results.get("result")
        else:
            results = []

        if doc.resource == "social_links_email":
            spec = SlinksLiSpecs.email_spec
        elif doc.resource == "social_links_emailV2":
            spec = SlinksLiSpecs.email_v2_spec
        elif doc.resource == "social_links_name":
            spec = SlinksLiSpecs.name_spec

        for result in results:
            if doc.resource == "social_links_email":
                if result["linkedin_id"]:
                    mapped_result = glom(result, spec)

                    mapped_result["urn"] = doc.urn
                    mapped_result["resource"] = doc.resource
                    mapped_result["search_id"] = doc.search_id

                    (mapped_result["linkedin_profile"]
                     ["linkedin_email_address"]) = ([mapped_result
                                                     ["linkedin_profile"]
                                                     ["linkedin_email_address"
                                                      ]])

                    _doc = SearchResponseDoc(**mapped_result)
                    docs.append(_doc)
            else:
                mapped_result = glom(result, spec)

                mapped_result["urn"] = doc.urn
                mapped_result["resource"] = doc.resource

                _doc = SearchResponseDoc(**mapped_result)
                docs.append(_doc)
        return docs
