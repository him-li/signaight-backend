from langgraph.graph import StateGraph, START, END

from .nodes import (
    start_flow_operator,
    generate_search_queries_router,
    generate_search_queries_google_operator,
    generate_search_queries_social_media_operator,
    merge_search_queries_synthesizer_router,
    process_google_candidates_search_operator,
    process_linkedin_candidates_search_operator,
    process_facebook_candidates_search_operator,
    process_instagram_candidates_search_operator,
    merge_search_results_synthesizer,
    match_search_results_operator,
    extract_matched_results_operator,
    merge_extracted_candidates_operator,
    merge_candidate_results_router,
    end_flow,
    #appender,
    #matcher,
    #merger_flow,
    #end_flow
)
from .context import Context
from .state import InputState, State

builder = StateGraph(State, input_schema=InputState, context_schema=Context)

# dispose technical things or/and prepare some data
# decide which type of queries should processed
builder.add_node(start_flow_operator)
# generate queries in parallel
builder.add_node(generate_search_queries_router)
# optional generate google queries if enabled
builder.add_node(generate_search_queries_google_operator)
# optional generate social media queries if enabled
builder.add_node(generate_search_queries_social_media_operator)
# merge all generated queries into one State field as dict
# where key is source(google, facebook, etc) and value is list/set of queries
builder.add_node(merge_search_queries_synthesizer_router)
# parallel run of designated nodes on chosen sources to process
builder.add_node(process_google_candidates_search_operator)
builder.add_node(process_linkedin_candidates_search_operator)
builder.add_node(process_facebook_candidates_search_operator)
builder.add_node(process_instagram_candidates_search_operator)
# merge all taken data into State messages field
builder.add_node(merge_search_results_synthesizer)
builder.add_node(match_search_results_operator)
builder.add_node(extract_matched_results_operator)
builder.add_node(merge_extracted_candidates_operator)
builder.add_node(merge_candidate_results_router)
builder.add_node(end_flow)

'''
# at the moment could route to `start_flow_operator` or to the `END`
# WARNING: this methodology looks like while loop and require count of
# iteration to garceful exit from flow loop to follow state machine pattern
builder.add_node(match_candidates_person_router)
'''
builder.add_edge(START, "start_flow_operator")
