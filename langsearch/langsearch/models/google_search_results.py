import json
from pydantic import BaseModel, Field
from typing import Optional, Any, Self

__all__ = ["GoogleSearchResult", "GoogleSearchResults", "extract_organic_to_results"]


class ResultData(BaseModel):
    pos: int = 0
    url: str = "" # TODO: maybe change to AnyHttpUrl later
    desc: str = ""
    title: str = ""
    html: str = ""

    def __init__(self, data_dict:dict):
        super().__init__()
        self.pos = data_dict["pos"]
        self.url = data_dict["url"]
        self.title = data_dict["title"]
        self.desc = data_dict["desc"]
        self.pos = data_dict["pos"]


class GoogleSearchResult(BaseModel):
    search_query: str = ""
    search_location: str = ""
    result_data: dict =  {}

    def get_result_data_urls(self):
        return list(self.result_data.keys())

    @classmethod
    def from_oxylabs_response(cls, oxy_response: Any) -> Self | None:
        """
        Build a GoogleSearchResult from a `sub_entry` (dict or JSON string).

        Uses only:
          - sub_entry["search_information"]["geo_location"]
          - sub_entry["search_information"]["query"]
          - sub_entry["organic"] (or first organic entry if org_index not provided)

        org_index is the position (0-based) inside the organic list; pos field is 1-based.
        """
        # TODO: oxylabs response should checked first for right response!!!
        # a lot of errors came with empty responses
        if not isinstance(oxy_response.content, dict):
            return
        search_query = oxy_response.content["url"]
        #TODO: change this
        search_location = "United States"
        result_data_dict ={}
        organic = oxy_response.content["results"]["organic"]
        if isinstance(organic, list):
            for data in organic:
                data_dict = {}
                data_dict["url"] = data.get("url") or data.get("link") or data.get("href") or ""
                data_dict["title"] = data.get("title") or data.get("name") or ""
                data_dict["desc"] = data.get("description") or data.get("snippet") or data.get("content") or ""
                data_dict["pos"] = data.get("position") or data.get("pos") or (org_index + 1)
                result_data = ResultData(data_dict)
                result_data_dict[data_dict["url"]] = result_data
        return cls(
            search_query=search_query,
            search_location=search_location,
            result_data =  result_data_dict
        )

class GoogleSearchResults(BaseModel):
    search_results : list[GoogleSearchResult] =[]

    def add_google_google_search_result(self, google_search_result : GoogleSearchResult):
        self.search_results.append(google_search_result)

    def get_search_results(self):
        return self.search_results
