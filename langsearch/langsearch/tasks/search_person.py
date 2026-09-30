import copy
import uuid
from beanie.exceptions import DocumentNotFound
from pathlib import Path
from datetime import datetime, timezone
# from langgraph.checkpoint.mongodb import MongoDBSaver

from core.logging import logger
from langsearch.graph import builder as graph_builder, Context
from langsearch.models.matcher_results import (UnifiedPerson,
    UnifiedPersonModel, ExtractedCandidate, ExtractedCandidateModel, WorkExperienceModel)
from langsearch.tasks import * # noqa
from langsearch.utils.graph_config import load_graph_config
from langsearch.graph.state import dict_query_reducer
from langsearch.tracing import load_prompt


async def search_person_task(
    person_id: uuid.UUID,
    flow: str,
):
    agent_config = load_graph_config(
        Path(__file__).resolve().parent.parent / 'langsearch.yaml')
    if not agent_config:
        logger.error("graph config has been not found")
        return

    # TODO: adopt global timeout here later
    result = []
    matched_urls = []
    url_to_query = {}
    previous_queries = {}
    init_result_set = {
        "google": {},
        "linkedin": {},
        "facebook": {},
        "instagram": {}
    }
    result_set = {
        "google": {},
        "linkedin": {},
        "facebook": {},
        "instagram": {}
    }
    graph = graph_builder.compile()
    iteration_config = next((item for item
        in agent_config.get('iterations', [])
        if item.get("default", False)), None)
    if not iteration_config:
        raise ValueError("No default config found for iteration")
    for i in range(0, int(agent_config.get('max_iterations', 1))):
        # Build iteration config
        try:
            iteration_config = {
                **iteration_config,
                **agent_config.get('iterations', [])[i]
            }
        except Exception:
            logger.warning(f"There is no {i+1} iteration config found. Default used")
        # get person from database
        person = await UnifiedPersonModel.get(person_id)
        if not person:
            logger.error("No person found")
            return

        logger.info(f"Gaph iteration {i+1} for search "
            f"{person.input.model_dump_json(exclude_unset=True,
                exclude_none=True)}")

        # UnifiedPersonModel contain same model attributes but less so we need to
        # shrinkdown them with SearchInput schema at the moment
        config = {
            "configurable": {
                # very important to use copy of config cause dict get modified
                # in grpah progress.
                # TODO: if config does not get changes maybe reasonable to
                # process it before graph
                **copy.deepcopy(agent_config),
                **{
                    "thread_id": str(person.id),
                    "run_id": str(uuid.uuid4()),
                    "checkpoint_ns": "langsearch",
                }
            },
            #"callbacks": [langfuse_handler]
        }
        state = {
            "flow": flow,
            "person_id": person.id,
            # input field is required for graph processing
            "input": person.input,
            # input field will dropped in type migration from
            # UnifiedPersonModel to UnifiedPerson
            'unified_person': person,
            'previous_queries': previous_queries,
            # NOTE: i == 0 here we add some criteria on what iteration we want to reuse the result set also should exist for every iteration
            'result_set': (result_set
                if iteration_config.get("use_results", False)
                else init_result_set),
            'matched_urls': matched_urls,
            'url_to_query': url_to_query,
        } # type: ignore
        '''
        # NOTE: currently disable cause we do not operate with chqck logic for
        # previously searched candidates. This logic require presence ID from
        # database to prevent incremental saving(recommended, but require
        # additional logic) or wiping provious candidates before save every
        # time when graph return them(not recommended, code commented below)

        extracted_candidates = []
        # restore previously saved extracted persons
        extracted_candidates_query = ExtractedCandidateModel.find(
            ExtractedCandidateModel.unified_person.id == person.id
        )
        async for extracted_person in extracted_candidates_query:
            extracted_candidates.append(ExtractedCandidateModel)
        if extracted_candidates:
        state['extracted_candidates'] = extracted_candidates
        '''

        context = Context(
            system_prompt=load_prompt("SYSTEM_PROMPT"),
            google_match_prompt=load_prompt("GOOGLE_MATCH_PROMPT", iteration_number=i),
            url_details_prompt=load_prompt("URL_DETAILS_PROMPT"),
            sm_match_prompt=load_prompt("SM_MATCH_PROMPT", iteration_number=i),
            structured_extraction_prompt=load_prompt("STRUCTURED_EXTRACTION_PROMPT"),
            person_search_query_prompt=load_prompt("PERSON_SEARCH_QUERY_PROMPT"),
            person_social_media_search_query_prompt=load_prompt("PERSON_SOCIAL_MEDIA_SEARCH_QUERY_PROMPT"),
            person_str_json=person.input.model_dump_json(exclude_unset=True,
                exclude_none=True),
            iteration_number=i,
            # NOTE: these are the default match options for the graph which should be defined for every iteration
            match_options=iteration_config.get("match_options",
                ["confirmed_match"]),
            reuse_match_options=iteration_config.get("reuse_match_options", []),
        )
        '''
        # checkpointer powered graph
        # Error 'update' command document too large
        # due MongoDB document max size 16MiB
        # Alternatives:
        #  - S3 checkpointer - there is few possible libs but all of them does not have async support or have problems with async operations
        #  - Redis checkpointer - not tested
        # https://github.com/redis-developer/langgraph-redis/tree/main
        try:
            db_name = settings.MONGODB_URI.path.strip('/').split('/')[0]
        except Exception as e:
            logger.info(e)
            print("there is no database specified use default signaight")
            db_name = "signaight"
        # Seems MongoDBSaver sync only and require separate connection
        with MongoDBSaver.from_conn_string(str(settings.MONGODB_URI), db_name) as checkpointer:
            try:
                # to continue loop restore point required as state = null
                graph = graph_builder.compile(checkpointer=checkpointer)
                res = await graph.ainvoke(state, config=config,
                    name="ReAct Agent", context=context)
            except Exception as e:
                print(str(e))
                res = None
        '''
        try:
            res = await graph.ainvoke(state, config=config,
                    name="ReAct Agent", context=context)
        except Exception:
            logger.error("Error invoking graph")
            raise

        '''
        # cleanup all extracted persons to write new sequence of extracted persons
        # At the moment there is no logic to extend them withot duplications
        #await ExtractedCandidateModel.find(
        #    ExtractedCandidateModel.unified_person.id == person.id
        #).delete()
        '''
        for item in res.get('extracted_candidates', []):
            if isinstance(item, ExtractedCandidate):
                item = item.model_dump()
            try:
                extracted_candidate = ExtractedCandidateModel(
                    unified_person=person, **item)
                extracted_candidate.timestamp = datetime.now(timezone.utc)
                await extracted_candidate.insert()
            except Exception as e:
                logger.error(f"ExtractedCandidate processing error: {str(e)}")
                continue
        if _unified_person := res.get('unified_person'):
            if isinstance(_unified_person, UnifiedPerson):
                _unified_person.end_timestamp = datetime.now(timezone.utc)
                _unified_person = _unified_person.model_dump()
            person = UnifiedPersonModel(**{**person.model_dump(),
                **_unified_person})
            # update input data for next iteration
            person.update_input_from_model()
            try:
                await person.replace()
            except (ValueError, DocumentNotFound):
                logger.error("Can't replace a non existing document")
        previous_queries = res.get('previous_queries', {})
        result_set = dict_query_reducer(result_set, res.get('reuse_result_set', {}))
        matched_urls += res.get('matched_urls', [])
        url_to_query = res.get('url_to_query', {})
        result.append(res)
    return result
