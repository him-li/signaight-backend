import asyncio
import json
from tarfile import LENGTH_NAME
from langsearch.utils.parse_google_query import extract_google_query
from typing import Any, Optional, Set, Dict, List
from datetime import datetime
from glom import glom
from mergedeep import merge, Strategy


from langsearch.models.google_search_results import GoogleSearchResults
from langsearch.models.search_input import SearchInput
from langsearch.tools.google_search import get_urls_html_content_for_graph_tool
from langsearch.tools.google_urls_by_query import get_results_array_from_google_async
from langsearch.graph.prompts import (
    PERSON_SEARCH_QUERY_PROMPT,
    PERSON_SOCIAL_MEDIA_SEARCH_QUERY_PROMPT)

from core.clients.vetric.facebook import api as facebook_api, VtrcFbSpecs
from core.clients.vetric.instagram import api as instagram_api, VtrcIgSpecs
from core.clients.vetric.linkedin import api as linkedin_api, VtLISpecs
from core.dotty_dictionary import dotty
from core.logging import logger


async def search_google_by_query_set(
    query_set: set,
    **kwargs,
) -> tuple:
    """
    This function return list of google results search reults
    based on generate_person_search_query function

    """
    logger.info(
        f"Process {len(query_set)} queries with limit "
        f"{kwargs.get('limit', 50)} items per query"
    )
    google_search_results = GoogleSearchResults()
    await get_results_array_from_google_async(
        list(query_set),
        google_search_results,
        limit=kwargs.get("limit", 50))
    url_dict = {}
    for google_search_result in google_search_results.get_search_results():
        url_dict[extract_google_query(
            google_search_result.search_query)] = google_search_result.get_result_data_urls().copy()

    logger.info(
        "Under data extraction we will ommit "
        f"{len(kwargs.get('urls_exclude', []))} already processed urls"
    )
    # build flat list of urls with check of previous processing
    flat_array_of_urls_to_scrape = [item
        for sublist in [item for item in url_dict.values()]
            for item in sublist if item not in kwargs.get("urls_exclude", [])]

    scraped_content = await get_urls_html_content_for_graph_tool(
        flat_array_of_urls_to_scrape)
    return url_dict, scraped_content


def generate_search_queries(
    person_str: str,
    prompt: Any,
    previous_queries: Set[str] | None = None,
) -> str:
    """
    Generate Google search queries for a person, excluding previously run queries.

    Args:
        person: SearchInput object containing person details
        person_search_query_prompt: Template for generating queries
        previous_queries: Set of queries that have already been executed

    Returns:
        str: Formatted prompt with previous queries context
    """
    previous_queries = previous_queries or set()
    person = SearchInput(**json.loads(person_str))
    formatted_prompt = prompt.format(
        firstname=person.firstname,
        lastname=person.lastname,
        city=person.city,
        state=person.state,
        zip=person.zip,
        email=person.email,
        homephone=person.homephone,
        cellphone=person.cellphone,
        address=person.address,
        dob=person.dob,
        work=person.work,
        education=person.education,
        locations=person.locations,
        network_signature=person.network_signature,
        country=person.country,
        system_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        previous_queries=chr(10).join(f"- {query}" for query in previous_queries),
    )
    return formatted_prompt


def generate_sm_search_queries(
    person_str: str,
    social_media: str,
    prompt: Any,
    previous_queries: Set[str] | None = None,
) -> str:
    """
    Generate Social Media search queries for a person, excluding previously run queries.

    Args:
        person: SearchInput object containing person details
        person_search_query_prompt: Template for generating queries
        previous_queries: Set of queries that have already been executed

    Returns:
        str: Formatted prompt with previous queries context
    """
    previous_queries = previous_queries or set()
    person = SearchInput(**json.loads(person_str))
    formatted_prompt = prompt.format(
        firstname=person.firstname,
        lastname=person.lastname,
        city=person.city,
        state=person.state,
        zip=person.zip,
        email=person.email,
        homephone=person.homephone,
        cellphone=person.cellphone,
        address=person.address,
        dob=person.dob,
        work=person.work,
        education=person.education,
        locations=person.locations,
        country=person.country,
        network_signature=person.network_signature,
        system_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        social_media=social_media,
        previous_queries=chr(10).join(f"- {query}" for query in previous_queries),
    )
    return formatted_prompt


async def search_linkedin_by_query_set(query_set: Set) -> List[Dict]:
    results = {}
    num_results = 12
    search_tasks = []

    for query in query_set:
        search_tasks.append(linkedin_api.async_search.people(
            params={"keywords": query}))

    search_results = await asyncio.gather(*search_tasks)

    for search_res, query in zip(search_results, query_set):
        try:
            res_body = search_res.body
            spec = VtLISpecs.new_search_spec

            if mapped := glom(res_body, spec):
                results[query] = mapped

        except Exception as e:
            logger.error(f"Error during LinkedIn search: {e}")
            continue

        try:
            if not mapped:
                results.pop(query, None)
                continue
            overview_tasks = []

            for i, query_result in enumerate(mapped[:num_results]):
                result_dotty = dotty(query_result)
                user_id = result_dotty.get(
                    "network_signature.user_id.linkedin_user_id")[0]

                if not user_id:
                    logger.warning(
                        f"No LinkedIn user ID found for result in query '{query}'")
                    continue

                overview_tasks.append(
                    linkedin_api.async_profile.overview(user_id))

            overview_results = await asyncio.gather(*overview_tasks)

            for i, (overview_res, query_result) in enumerate(zip(overview_results, mapped[:num_results])):
                overview_body = overview_res.body
                mapped_overview = glom(overview_body, VtLISpecs.overview_spec)
                results[query][i] = merge(query_result,
                                          mapped_overview,
                                          strategy=Strategy.ADDITIVE
                                          )
        except Exception as e:
            # Log the error but continue with other profiles
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                logger.warning(
                    f"LinkedIn profile overview failed (status {e.response.status_code}) for query '{query}', result {i}: {error_msg[:200]}")
            else:
                logger.warning(
                    f"LinkedIn profile overview failed for query '{query}', result {i}: {error_msg[:200]}")
            continue
    if results:
        return [result for query_result in results.values()
                for result in query_result]
    else:
        return []


async def search_facebook_by_query_set(query_set: set) -> List[Dict]:
    # here we extract initial data for candidates for each query in set
    results = {}
    num_results = 4
    search_tasks = []
    for query in query_set:
        search_tasks.append(facebook_api.async_search.users(
            body={"typed_query": query, "transform": True}))
    search_results = await asyncio.gather(*search_tasks)
    for search_res, query in zip(search_results, query_set):
        try:
            res_body = search_res.body
            spec = VtrcFbSpecs.new_search_spec

            if mapped := glom(res_body, spec):
                results[query] = mapped

        except Exception as e:
            logger.error(f"Error during Facebook search: {e}")
            continue

        try:
            if not mapped:
                results.pop(query, None)
                continue

            about_tasks = []
            timeline_tasks = []

            for i, query_result in enumerate(mapped[:num_results]):
                result_dotty = dotty(query_result)
                user_id = result_dotty.get(
                    "network_signature.user_id.facebook_user_id")[0]
                about_tasks.append(facebook_api.async_profiles.about(user_id))
                timeline_tasks.append(
                    facebook_api.async_profiles.timeline(user_id))

            about_results = await asyncio.gather(*about_tasks)
            timeline_results = await asyncio.gather(*timeline_tasks)

            for i, (about_res, query_result) in enumerate(zip(about_results, mapped[:num_results])):
                about_body = about_res.body
                mapped_about = glom(
                    about_body, VtrcFbSpecs.about_spec_transform)
                results[query][i] = merge(query_result, mapped_about,
                                          strategy=Strategy.ADDITIVE)

            for i, (timeline_res, query_result) in enumerate(zip(timeline_results, mapped[:num_results])):
                timeline_body = timeline_res.body
                mapped_timeline = glom(
                    timeline_body, VtrcFbSpecs.new_timeline_spec)
                results[query][i] = merge(results[query][i], mapped_timeline,
                                          strategy=Strategy.ADDITIVE)
        except Exception as e:
            logger.error(f"Error preparing about call: {e}")

    if results:
        return [result for query_result in results.values()
                for result in query_result]
    else:
        return []


async def search_instagram_by_query_set(
        query_set: set) -> List[Dict]:
    # here we extract initial data for candidates for each query in set
    results = {}
    num_results = 4
    search_tasks = []
    for query in query_set:
        search_tasks.append(
            instagram_api.async_user.search(params={"q": query}))
    search_results = await asyncio.gather(*search_tasks)
    for search_res, query in zip(search_results, query_set):
        try:
            res_body = search_res.body
            spec = VtrcIgSpecs.new_search_spec

            if mapped := glom(res_body, spec):
                results[query] = mapped

        except Exception as e:
            logger.error(f"Error during Instagram search: {e}")
            continue

        try:
            if not mapped:
                results.pop(query, None)
                continue
            info_tasks = []
            for i, query_result in enumerate(mapped[:num_results]):

                result_dotty = dotty(query_result)
                user_id = int(result_dotty.get(
                    "network_signature.user_id.instagram_user_id")[0])
                info_tasks.append(
                    instagram_api.async_user.info(format(user_id)))

            info_results = await asyncio.gather(*info_tasks)

            for i, (info_res, query_result) in enumerate(zip(info_results, mapped[:num_results])):
                info_body = info_res.body
                mapped_info = glom(info_body, VtrcIgSpecs.info_spec)
                results[query][i] = merge(
                    query_result,
                    mapped_info,
                    strategy=Strategy.ADDITIVE
                )

        except Exception as e:
            logger.error(f"Error preparing Instagram info call: {e}")
            continue

    if results:

        return [result for query_result in results.values()
                for result in query_result]
    else:
        return []


__all__ = [
    "generate_search_queries",
    "search_google_by_query_set",
    "generate_sm_search_queries",
    "search_linkedin_by_query_set",
    "search_facebook_by_query_set",
    "search_instagram_by_query_set",
]
