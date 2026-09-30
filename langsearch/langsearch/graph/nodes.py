"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""
import asyncio
import csv
import re
import json
import logging
import pandas as pd
from datetime import UTC, datetime
from typing import List, Literal, cast
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langgraph.types import Command
from langgraph.runtime import Runtime
from pylitmus import create_engine, Rule, Severity, DecisionTier

from langsearch.config import settings
from langsearch.utils.merge_results import merge_extracted_candidates
from langsearch.utils.normalize_query import normalize_query
from langsearch.utils.normalize_result import normalize_result
from langsearch.tools.queries import (
    generate_search_queries,
    search_google_by_query_set,
    generate_sm_search_queries,
    search_linkedin_by_query_set,
    search_facebook_by_query_set,
    search_instagram_by_query_set
)
from langsearch.utils.get_result_messages import get_result_messages_by_source
from langsearch.models.matcher_results import ExtractedCandidate, UnifiedPerson, ValueRanking
from langsearch.tools.google_search import extract_body_content
from langsearch.utils.google_gemini import load_gemini_chat_model
from .context import Context
from .state import State, dict_query_reducer


logger = logging.getLogger(__name__)


# from data_model.search_queries import StructuredResponse
# Define the function that calls the model
MATCH_OPTIONS = ["confirmed_match", "likely_match", "unclear", "not_match"]
N_IMAGES = 3

model = load_gemini_chat_model()


async def start_flow_operator(
    state: State, runtime: Runtime[Context], config: RunnableConfig
) -> Command:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    logger.info("STATE: start_flow_operator - STARTED")

    # Extract flows behavior config
    # flow_config = config.get('configurable', {}).get('flows',
    #     {}).get(state.flow, {})

    state_input_str = ", ".join(
        [f"{f}='{v}'" for f, v
            in state.input.model_dump(mode='json', exclude_unset=True,
            exclude_none=True).items()]
    )

    person_images = []
    if state.unified_person.images.image:
        person_images = [im.value for im
            in state.unified_person.images.image[:N_IMAGES] if im]
    if state.input.photo:
        # NOTE: state.input.photo is list + deduplicate urls
        person_images = list(set(state.input.photo + person_images))


    update = {
        "images": person_images,
        "messages": [
            ("user", f"You are a helpful assistant that will help me to find information about a person with the following details: {state_input_str}")
        ]
    }

    if runtime.context.iteration_number == 0:
        unified_person = state.unified_person.copy()

        if state.input.firstname:
            unified_person.f_name.f_name.append(ValueRanking(value=state.input.firstname, default=True, probability=1.0, ranking=0, count=1))
        if state.input.lastname:
            unified_person.l_name.l_name.append(ValueRanking(value=state.input.lastname, default=True, probability=1.0, ranking=0, count=1))
        if state.input.email:
            unified_person.email_address.email_address.append(ValueRanking(value=state.input.email, default=True, probability=1.0, ranking=0, count=1))

        update["unified_person"] = unified_person


    logger.info("STATE: start_flow_operator - ENDED, going to: "
                "generate_search_queries_router")
    return Command(
        goto="generate_search_queries_router", 
        update=update,
    )



async def generate_search_queries_router(
    state: State, runtime: Runtime[Context]
) -> List[Command]:
    logger.info("STATE: generate_search_queries_router - STARTED")
    logger.info("STATE: generate_search_queries_router - ENDED, "
                "going to: generate_search_queries_google_operator, "
                "generate_search_queries_social_media_operator")
    return [
        Command(goto="generate_search_queries_google_operator"),
        Command(goto="generate_search_queries_social_media_operator")
    ]


async def generate_search_queries_google_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    logger.info("STATE: generate_search_queries_google_operator - STARTED")
    new_prompt = generate_search_queries(
        person_str=runtime.context.person_str_json,
        prompt=runtime.context.person_search_query_prompt,
        previous_queries=state.previous_queries.get("google", {}),
    )

    messages = [HumanMessage(content=new_prompt)]
    response = await model.ainvoke([SystemMessage(content=state.person_query), *messages])
    messages.append(response)
    # WARNING: Due to different version of libs respond data could different
    try:
        current_queries = set(query for query in response.content.splitlines())
    except Exception:
        current_queries = set(query for query
                            in response.content[0].get("text", "").splitlines())
    # no more new data - finish

    if len(current_queries) == 0:
        logger.info("STATE: generate_search_queries_google_operator - ENDED, "
                    " going to: merge_search_queries_synthesizer_router "
                    "(no queries generated)")
        return Command(goto="merge_search_queries_synthesizer_router")

    # update state
    previous_queries = dict_query_reducer(
        state.previous_queries,
        {'google': current_queries}
    )
    current_queries = {'google': current_queries}

    logger.info("STATE: generate_search_queries_google_operator - ENDED, "
                f"going to: merge_search_queries_synthesizer_router (generated {len(current_queries)} queries)")
    return Command(
        # The next node(s) to go to
        goto="merge_search_queries_synthesizer_router",
        # The update to apply to the state
        update={
            "messages": messages,
            "current_queries": current_queries,
            "previous_queries": previous_queries

        }
    )


async def generate_search_queries_social_media_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    social_media_platforms = ["linkedin", "facebook", "instagram"]
    logger.info("STATE: generate_search_queries_social_media_operator - "
                "STARTED")
    queries = {}
    tasks = []
    messages = []

    for platform in social_media_platforms:
        new_prompt = generate_sm_search_queries(
            # TODO: note race conditions!!
            person_str=runtime.context.person_str_json,
            social_media=platform,
            prompt=runtime.context.person_social_media_search_query_prompt,
            previous_queries=state.previous_queries.get(platform, {}),
        )
        # model_w_structured_response = model.with_structured_output(StructuredResponse)
        message = HumanMessage(content=new_prompt)
        tasks.append(model.ainvoke([SystemMessage(content=state.person_query), message]))
        messages.append(message)

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    all_previous_queries = {}

    for response, platform in zip(responses, social_media_platforms):
        try:
            current_queries = set(query for query in response.content.splitlines())
            queries.setdefault(platform, current_queries)
        except Exception:
            current_queries = set(query for query in response.content[0].get("text", "").splitlines())
            queries.setdefault(platform, current_queries)

        logger.info(f"STATE: generate_search_queries_social_media_operator"
                    f"generated {len(current_queries)} queries for {platform}")

    previous_queries = dict_query_reducer(
        state.previous_queries,
        queries
    )

    logger.info("STATE: generate_search_queries_social_media_operator - ENDED, "
        "going to: merge_search_queries_synthesizer_router ")
    return Command(
        # The next node(s) to go to
        goto="merge_search_queries_synthesizer_router",
        # The update to apply to the state
        update={"current_queries": queries, "previous_queries": previous_queries}
    )


async def merge_search_queries_synthesizer_router(
    state: State, runtime: Runtime[Context], config: RunnableConfig
) -> List[Command]:
    logger.info("STATE: merge_search_queries_synthesizer_router - STARTED")

    flow_config = config.get('configurable', {}).get('flows',
         {}).get(state.flow, {})
    rules_data = {
        'stats': state.flow_stats,
        'input': state.input.model_dump(mode='json'),
        'person': state.unified_person.model_dump(mode='json'),
    }
    next_nodes = []
    _next_nodes = [
        "process_google_candidates_search_operator",
        "process_linkedin_candidates_search_operator",
        "process_facebook_candidates_search_operator",
        "process_instagram_candidates_search_operator",
    ]
    for next_node in _next_nodes:
        if not (node_config := flow_config.get(next_node)):
            continue
        engine = create_engine(**node_config)
        # Evaluate next node run
        result = engine.evaluate(rules_data)
        # NOTE: here allow or reject should be not hardcoded or so
        if result.decision == 'allow':
            next_nodes.append(next_node)
    if next_nodes:
        logger.info("STATE: merge_search_queries_synthesizer_router - ENDED, "
            f"going to: {', '.join(next_nodes)} ")
        return [Command(goto=n) for n in next_nodes]
    else:
        logger.info("STATE: merge_search_queries_synthesizer_router - "
            "next nodes has been not found in config or not passed criteria ")
        logger.info("STATE: merge_search_queries_synthesizer_router - ENDED, "
            "going to: END ")
        return Command(goto=END)


async def process_google_candidates_search_operator(
    state: State, runtime: Runtime[Context], config: RunnableConfig
) -> Command:
    queries = state.current_queries.get("google", {})
    url_to_query = state.url_to_query

    logger.info("STATE: process_google_candidates_search_operator - STARTED "
                f"(searching {len(queries)} queries)")
    flow_config = config.get('configurable', {}).get('flows',
         {}).get(state.flow, {})

    url_dict, scraped_content = await search_google_by_query_set(queries,
        limit=flow_config.get("google_search_items_per_page", 50),
        urls_exclude=url_to_query.keys())

    scraped_content = normalize_result(scraped_content, 'google')
    scraped_content = {url: content for url, content in scraped_content.items()
        if url not in state.matched_urls}

    # Get person info for query normalization
    person_info = None

    # NOTE: person data should be not part of context. Deprecated!
    '''
    try:
        #person_info = json.loads(runtime.context.person_str_json)
    except (json.JSONDecodeError, AttributeError):
        pass
    '''
    # Replacement context data and backward compatibility workaround
    # for None values in state.input model
    person_info = {f: v if v is not None else ''
        for f, v in state.input.model_dump(mode="json").items()}

    # Create URL to query mapping for statistics tracking
    # Use normalized queries to remove personal information
    for query, urls in url_dict.items():
        normalized_query = normalize_query(query, person_info)
        for url in urls:
            url_to_query[url] = normalized_query  # Use normalized query as key

    # Initialize query stats for current queries using normalized queries
    current_query_stats = state.query_stats.get('google', {}).copy()
    for query in state.current_queries:
        normalized_query = normalize_query(query, person_info)
        if normalized_query not in current_query_stats:
            current_query_stats[normalized_query] = {
                "matched": 0, "not_matched": 0}

    logger.info("STATE: process_google_candidates_search_operator - ENDED, "
                " going to: merge_search_results_synthesizer")
    update = {
        "current_queries": {'google': set()},
        "url_dict": url_dict,
        "url_to_query": url_to_query,
        "query_stats": {'google': current_query_stats},
        "result_set": {'google': scraped_content}
    }
    return Command(goto="merge_search_results_synthesizer", update=update)


async def process_linkedin_candidates_search_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    queries = state.current_queries.get("linkedin", {})
    logger.info("STATE: process_linkedin_candidates_search_operator - STARTED "
                f"(searching {len(queries)} queries)")
    social_media_results = await search_linkedin_by_query_set(queries)

    logger.info("STATE: process_linkedin_candidates_search_operator - ENDED, "
                " going to: merge_search_results_synthesizer")
    update = {
        "current_queries": {'linkedin': set()},
    }
    if social_media_results:
        results = normalize_result(social_media_results, 'linkedin')
        results = {url: content for url, content in results.items() if url not in state.matched_urls}
        update['result_set'] = {"linkedin": results}
    return Command(goto="merge_search_results_synthesizer", update=update)


async def process_facebook_candidates_search_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    queries = state.current_queries.get("facebook", {})
    logger.info("STATE: process_facebook_candidates_search_operator - STARTED "
                f"(searching {len(queries)} queries)")
    social_media_results = await search_facebook_by_query_set(queries)
    logger.info("STATE: process_facebook_candidates_search_operator - ENDED, "
                " going to: merge_search_results_synthesizer")
    update = {
        "current_queries": {'facebook': set()},
    }
    if social_media_results:
        results = normalize_result(social_media_results, 'facebook')
        results = {url: content for url, content in results.items() if url not in state.matched_urls}
        update['result_set'] = {"facebook": results}
    return Command(goto="merge_search_results_synthesizer", update=update)


async def process_instagram_candidates_search_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    queries = state.current_queries.get("instagram", {})
    logger.info("STATE: process_instagram_candidates_search_operator - STARTED "
                f"(searching {len(queries)} queries)")
    social_media_results = await search_instagram_by_query_set(queries)
    logger.info("STATE: process_instagram_candidates_search_operator - ENDED, "
                " going to: merge_search_results_synthesizer")
    update = {
        "current_queries": {'instagram': set()},
    }
    if social_media_results:
        results = normalize_result(social_media_results, 'instagram')
        results = {url: content for url, content in results.items() if url not in state.matched_urls}
        update['result_set'] = {"instagram": results}
    return Command(goto="merge_search_results_synthesizer", update=update)


async def merge_search_results_synthesizer(
    state: State, runtime: Runtime[Context]
) -> Command:
    logger.info("STATE: merge_search_results_synthesizer - STARTED")
    # TODO: data to Candidate with images saving?
    logger.info("STATE: merge_search_results_synthesizer - ENDED, "
                "going to: match_search_results_operator")
    return Command(goto="match_search_results_operator")


async def match_search_results_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    logger.info("STATE: match_search_results_operator - STARTED")

    tasks = []
    profile_pictures_str = "\n".join(
        f"{image}" for image in state.images[:3]) if state.images else ""

    result_set = state.result_set.copy()

    for platform, content in result_set.items():

        match platform:
            case "google":
                new_google_scraped_content = {}
                for url, scraped_content in content.items():
                    try:
                        parsed_content = scraped_content.get("content", "")
                        parsed_content = parsed_content[:2000] if parsed_content else ""
                        images = scraped_content["images"]
                        images_str = "\n".join(f"- {i}" for i in images) if images else ""
                        if parsed_content != "":
                            msg_content = runtime.context.google_match_prompt.format(
                                options=MATCH_OPTIONS,
                                system_time=datetime.now(tz=UTC).isoformat(),
                                url_path=url,
                                images=images_str,
                                profile_pictures=profile_pictures_str,
                                person_info=runtime.context.person_str_json,
                                parsed_content=parsed_content)
                            message = HumanMessage(content=msg_content)
                            tasks.append(model.ainvoke([message]))
                            new_google_scraped_content[url] = scraped_content
                    except Exception as e:
                        logger.error(f"Error processing Google URL {url}: {e}")
                        continue
            case "linkedin" | "facebook" | "instagram":
                for url, scraped_content in content.items():
                    try:
                        msg_content = runtime.context.sm_match_prompt.format(
                            options=json.dumps(MATCH_OPTIONS),
                            system_time=datetime.now(tz=UTC).isoformat(),
                            person_info=runtime.context.person_str_json,
                            profile_pictures=profile_pictures_str,
                            platform=platform,
                            content=json.dumps(scraped_content))
                        message = HumanMessage(content=msg_content)
                        tasks.append(model.ainvoke([message]))
                    except Exception as e:
                        logger.error(f"Error processing Social Media URL {url}: {e}")
                        continue
            case _:
                logger.error(f"Invalid platform: {platform}")
                continue

    messages = await asyncio.gather(*tasks, return_exceptions=True)

    logger.info(
        "STATE: match_search_results_operator - ENDED, "
        "going to: extract_matched_results_operator"
    )
    return Command(
        goto="extract_matched_results_operator",
        update={
            "messages": messages,
            "result_set": {"google": new_google_scraped_content},
        },
    )


async def extract_matched_results_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    logger.info("STATE: extract_matched_results_operator - STARTED")
    tasks = []
    messages = []
    matched_urls = []
    updated_query_stats = state.query_stats.copy()
    google_stats = updated_query_stats.get('google', {}).copy()
    linkedin_stats = updated_query_stats.get('linkedin', {}).copy()
    messages = state.messages

    model_w_structured_response = model.with_structured_output(
        ExtractedCandidate.model_json_schema(), method="json_schema")

    result_set = state.result_set.copy()
    new_result_set = {
        "google": {},
        "linkedin": {},
        "facebook": {},
        "instagram": {}
    }
    match_options = runtime.context.match_options
    reuse_match_options = runtime.context.reuse_match_options
    result_messages = get_result_messages_by_source(result_set, messages)
    for platform, content in result_set.items():
        platform_messages = result_messages[platform]
        match platform:
            case "google":
                for message, url in zip(platform_messages, content.keys()):
                    try:
                        match = message.content[0].get("text", "")
                    except Exception as e:
                        logger.error(f"Error processing Google URL {url}: {e}")
                        try:
                            match = json.loads(message.content[0]).get("text", "")
                        except Exception as e:
                            logger.error(f"Error parsing message content to json for URL {url}: {e}")
                            continue
                    query = state.url_to_query.get(url, None)
                    try:
                        match = re.search(r"Match Level: (\w+)", match).group(1)
                    except Exception as e:
                        logger.error(f"Error extracting match from message content for URL {url}: {e}")
                        continue

                    if match in match_options:
                        # TODO: find where content could get different dict structure
                        # 1 option: {"url": {"content": "..."}}
                        # 2 option: {"content": "..."}
                        if _content := content.get(url):
                            content = _content
                        prompt = runtime.context.url_details_prompt.format(
                            system_time=datetime.now(tz=UTC).isoformat(),
                            url_path=url,
                            parsed_content=json.dumps(content),
                            source=platform,
                            match_option=match
                        )

                        structured_message = HumanMessage(content=prompt)
                        tasks.append(model_w_structured_response.ainvoke([structured_message]))
                        messages.append(structured_message)

                        matched_urls.append(url)

                        if query:
                            if query not in google_stats:
                                google_stats[query] = {"matched": 0, "not_matched": 0}
                            google_stats[query]["matched"] += 1
                    else:
                        if match in reuse_match_options:
                            new_result_set[platform][url] = content
                        if query:
                            if query not in google_stats:
                                google_stats[query] = {"matched": 0, "not_matched": 0}
                    google_stats[query]["not_matched"] += 1

            case "linkedin" | "facebook" | "instagram":
                for message, url in zip(platform_messages, content.keys()):
                    try:
                        match = message.content[0].get("text", "")
                    except Exception:
                       match = ""
                    # add query stats
                    if match in match_options:
                        sm_content = content[url]['content']
                        prompt = runtime.context.structured_extraction_prompt.format(
                            system_time=datetime.now(tz=UTC).isoformat(),
                            content=json.dumps(sm_content),
                            source=platform,
                            match_option=match
                        )
                        structured_message = HumanMessage(content=prompt)
                        tasks.append(model_w_structured_response.ainvoke([structured_message]))
                        messages.append(structured_message)

                        matched_urls.append(url)
                    else:
                        if match in reuse_match_options:
                            new_result_set[platform][url] = content[url]['content']
            case _:
                logger.error(f"Invalid platform: {platform}")
                continue

    # NOTE: mathed results in new form
    results = await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("STATE: extract_matched_results_operator - ENDED, "
                "going to: merge_extracted_candidates_operator")

    return Command(
        goto="merge_extracted_candidates_operator",
        update={
            "messages": messages,
            "extracted_candidates": results,
            "reuse_result_set": new_result_set,
            "query_stats": {"google": google_stats, "linkedin": linkedin_stats},
            "matched_urls": matched_urls,
        },
    )

async def merge_extracted_candidates_operator(
    state: State, runtime: Runtime[Context]
) -> Command:
    logger.info("STATE: merge_extracted_candidates_operator - STARTED")
    extracted_candidates = state.extracted_candidates
    unified_person = merge_extracted_candidates(extracted_candidates, state.unified_person)
    logger.info("STATE: merge_extracted_candidates_operator - ENDED, "
                "going to: merge_candidate_results_router")

    return Command(
        goto="merge_candidate_results_router",
        update={
            "unified_person": unified_person,
            "first_run": False,
        }
    )

async def merge_candidate_results_router(
    state: State, runtime: Runtime[Context]
) -> List[Command]:
    logger.info("STATE: merge_candidate_results_router - STARTED")
    logger.info("STATE: merge_candidate_results_router - ENDED, "
                "going to: END")
    return Command(goto=END)


async def end_flow(
    state: State, runtime: Runtime[Context]
):
    logger.info("STATE: end_flow - STARTED")
    logger.info("STATE: end_flow - ENDED, terminating graph execution")
    return Command(goto=END)
