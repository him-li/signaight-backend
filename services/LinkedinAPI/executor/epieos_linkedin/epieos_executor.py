from jina import Executor
from typing import List
from glom import glom

from core.documents import SearchRequestDoc, SearchResponseDoc
from core.clients.epieos.linkedin import api, EpieosLiSpecs


class EpieosLinkedinAPI(Executor):

    async def _search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        docs = []
        if doc.email_address is None or "@" not in doc.email_address:
            return
        body = {"query": doc.email_address, "modules": ["linkedin"]}

        try:
            response = await api.async_search.osinter(body=body)
            response_results = response.body
        except Exception as e:
            print(str(e))
            return docs

        if response_results is None:
            return
        if response_results.get("result"):
            results = response_results.get("result")
        else:
            results = {}

        if results["linkedin"]:
            mapped_result = glom(results, EpieosLiSpecs.email_spec)

            data = {}
            data["urn"] = doc.urn
            data["resource"] = doc.resource
            data["search_id"] = doc.search_id
            name = {
                "first_name": {
                    "f_name": doc.f_name,
                    "linkedin_f_name": mapped_result["linkedin_f_name"]
                },
                "last_name": {
                    "l_name": doc.l_name,
                    "linkedin_l_name": mapped_result["linkedin_l_name"]
                },
                "full_name": {
                    "full_name": doc.name,
                    "linkedin_full_name": (mapped_result["linkedin_f_name"] +
                                           " " +
                                           mapped_result["linkedin_l_name"])
                }
            }
            email = {
                "email_address": ([doc.email_address] if
                                  doc.email_address else None),
                "linkedin_email_address": mapped_result[
                    "linkedin_email_address"]
            }
            personal_details = {
                "name": name,
                "email": email,
                "location": mapped_result["location"],
                "visuals": mapped_result["visuals"],
            }
            if (personal_details.get("visuals").get("profile_photo").
                    get("linkedin_profile_picture")) is None:
                del (personal_details["visuals"]
                     ["profile_photo"]["linkedin_profile_picture"])
            data["personal_details"] = personal_details
            data["network_signature"] = mapped_result["network_signature"]
            data["biographic_details"] = mapped_result["biographic_details"]

            for education in (mapped_result
                              ["biographic_details"]
                              ["education"]["linkedin_schools"]):
                if education["period"] is not None:
                    start_year = education["period"].split(" - ")[0]
                    end_year = education["period"].split(" - ")[1]
                    education["start_month_year"] = (
                        start_year if start_year != "" else None
                    )
                    education["end_month_year"] = (end_year if end_year != ""
                                                   else None)
                    del education["period"]

            for position in (mapped_result
                             ["biographic_details"]["work"]
                             ["linkedin_work"]["positions"]):
                if position["period"] is not None:
                    start_year = position["period"].split(" - ")[0]
                    end_year = position["period"].split(" - ")[1]
                    position["start_month_year"] = (
                        start_year if start_year != "" else None
                    )
                    position["end_month_year"] = (end_year if end_year != ""
                                                  else None)
                    del position["period"]

            _doc = SearchResponseDoc(**data)
            docs.append(_doc)
        else:
            pass

        return docs
