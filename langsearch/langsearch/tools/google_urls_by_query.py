import asyncio
import os
from langsearch.models.search_input import SearchInput
from datetime import datetime
from oxylabs import AsyncClient

from langsearch.config import settings
from langsearch.models.google_search_results import (GoogleSearchResults,
    GoogleSearchResult)


search = AsyncClient(
    username=settings.OXYLABS_SERP_PROXY_USERNAME,
    password=settings.OXYLABS_SERP_PROXY_PASSWORD
)


__all__ = ["search_person","get_results_array_from_google","get_results_array_from_google_async"]





def generate_person_search_query(input: SearchInput):
    """Generates 6 search query for a person based on their:
     1. first name, last name, and address.
     2. first name, last name, and cellphone.
     3. first name, last name, and homephone.
     4. first name, last name, ,address, country and state.
     5. first name, last name, and email.
     6.
     """
    query =[]
    # query.append( f"""{input.firstname} {input.lastname} {input.address}""")
    # query.append( f"""{input.firstname} {input.lastname} {input.cellphone}""")
    # query.append( f"""{input.firstname} {input.lastname} {input.homephone}""")
    # query.append( f"""{input.firstname} {input.lastname} {input.address}  {input.country}  {input.state}""")
    # query.append( f"""{input.firstname} {input.lastname} {input.dob}""")
    query.append( f"""{input.firstname} {input.lastname} {input.email}""")
    return query


# async def get_results_array_from_google(queries: list[str],google_search_results: GoogleSearchResults):
#     """Searches for a person using the Oxylabs search tool."""
#     responses = await asyncio.gather(*map(get_content_async,queries))
#     return extract_organic_arrays(responses,google_search_results)


async def get_results_array_from_google_async(
    queries: list[str],
    google_search_results: GoogleSearchResults,
    limit: int = 50
):
    finished_results = []
    tasks = []

    for query in queries:
        tasks.append(search.google.scrape_search(query,
            parse=True,
            timeout=40,
            poll_interval=3,
            pages=1,
            limit=limit,
            geo_location="United States"))

    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        finished_results.append(result)
    # responses = await get_content_async_new(queries)
    return extract_organic_arrays_new(finished_results, google_search_results)


def extract_organic_arrays_new(res_array: list,
        google_search_results: GoogleSearchResults) -> GoogleSearchResults:
    """Return a flattened list of all items found under the 'organic' key in res_array entries."""
    for res in res_array:
        for oxy_response in res.results:
            if oxy_response.status_code != 200:
                print(f"query {oxy_response.content.url} returned status "
                    f" {oxy_response.status_code}")
                continue
            if google_search_result := GoogleSearchResult.from_oxylabs_response(
                    oxy_response):
                google_search_results.add_google_google_search_result(
                    google_search_result)
    return google_search_results
