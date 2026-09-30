from jina import Flow, Client, DocumentArray
from typing import Union, List, Dict

from core.documents import (
    SearchRequestDoc,
    FacebookResponseDoc,
    InstagramResponseDoc,
    LinkedinResponseDoc,
)
from core.utils import build_search_docarray

from cli.typer_async import AsyncTyper, Argument, Option

from services.SearchIn.executor import SearchIn
from services.SearchOut.executor import SearchOut
from services.ResultAPIReducer.executor import ResultAPIReducer
from services.Aggregation.executor import Aggregation
from services.PrimaryCandidate.executor import PrimaryCandidate

from .base import build_executors_list

app = AsyncTyper()


# DEPRECATED, new way in core.flows package
@app.async_command()
async def all(
    name: str = Argument(...,
                         help="Person Firstname and Lastname. Ex: Jhon Doe"),
    search_and_enrich: bool = Argument(...,
                                       help="run search with enrichment"),
    person_id: str = Argument(..., help="Person UUID"),
    sources_resources: List[Dict] = Argument(
        ..., help="List of API sources and resources"
    ),
    search_id: str = Argument(..., help="Search ID"),
    f_name: str = Argument(..., help="Person Firstname"),
    l_name: str = Argument(..., help="Person Lastname"),
    email_address: str = Argument(..., help="Person Email Address"),
    city: str = Option("", help="City with country or region Ex: London, UK"),
    education: str = Option("", help=("Eductaion title. "
                                      "Ex: Harvard Business School")),
    work: str = Option("", help="Work title Ex: Acme Inc"),
):
    """
    If argument or option value is string and contain few words encapsulate it
    in doublequotes. Ex: "Jhon Doe".

    Example of usage:
    $ python cli/main.py search all "jhon.doe@gmail.com"
    """

    docs = build_search_docarray(
        name,
        person_id,
        sources_resources,
        search_id,
        f_name,
        l_name,
        email_address,
        {
            "city": city,
            "education": education,
            "work": work,
        },
    )

    flow = Flow().add(uses=SearchIn, name="searchIn")

    search_enrich = build_search_enrich(flow,
                                        sources_resources,
                                        full_search_enrich=search_and_enrich)

    flow = search_enrich.get("flow")
    client_params = search_enrich.get("client_params")
    next_step_needs = search_enrich.get("next_step_needs")

    flow = flow.add(
        uses=SearchOut,
        name="searchOut",
        needs=next_step_needs,
    )

    response = []

    with flow as f:  # Using it as a Context Manager will start the Flow
        client = Client(port=f.port, protocol=f.protocol, asyncio=True)
        async for resp in client.post(
            "/search",
            inputs=DocumentArray[SearchRequestDoc](docs),
            return_type=DocumentArray[
                Union[FacebookResponseDoc, InstagramResponseDoc,
                      LinkedinResponseDoc]
            ],
            request_size=1,
            parameters={**client_params},
        ):
            for doc in resp:
                response.append(doc)
        return response


# DEPRECATED, new way in core.flows package
async def linkedin_first(
    name: str = Argument(...,
                         help="Person Firstname and Lastname. Ex: Jhon Doe"),
    person_id: str = Argument(..., help="Person UUID"),
    sources_resources: List[Dict] = Argument(
        ..., help="List of API sources and resources"
    ),
    search_id: str = Argument(..., help="Search ID"),
    f_name: str = Argument(..., help="Person Firstname"),
    l_name: str = Argument(..., help="Person Lastname"),
    email_address: str = Argument(..., help="Person Email Address"),
    city: str = Option("", help="City with country or region Ex: London, UK"),
    education: str = Option("", help=("Eductaion title. "
                                      "Ex: Harvard Business School")),
    work: str = Option("", help="Work title Ex: Acme Inc"),
):
    """
    If argument or option value is string and contain few words encapsulate it
    in doublequotes. Ex: "Jhon Doe".

    Example of usage:
    $ python cli/main.py search all "jhon.doe@gmail.com"
    """

    li_source_resource = [source_resource for source_resource
                          in sources_resources if
                          source_resource["source"] == 'linkedin']

    if not li_source_resource:
        raise Exception("No Linkedin source resource found")

    fb_ig_sources_resources = [
        source_resource for
        source_resource in sources_resources
        if source_resource["source"] == 'facebook'
        or source_resource["source"] == 'instagram']

    if not fb_ig_sources_resources:
        raise Exception("No Facebook or Instagram source resource found")

    docs = build_search_docarray(
        name,
        person_id,
        li_source_resource,
        search_id,
        f_name,
        l_name,
        email_address,
        {
            "city": city,
            "education": education,
            "work": work,
        },
    )

    li_executors = build_executors_list(li_source_resource)
    li_executor = li_executors[0]

    flow = (Flow(
        ).add(
            uses=SearchIn,
            name="searchIn"
        ).add(
            **li_executor
        ).add(
            uses=ResultAPIReducer,
            name="linkedinAPIReducer",
            needs=li_executor.get("name")
        ).add(
            uses=PrimaryCandidate,
            needs="linkedinAPIReducer",
            name="linkedinPrimaryCandidate",
        ).add(
            uses=Aggregation,
            name="linkedinAggregation",
            needs="linkedinPrimaryCandidate",
            uvicorn_kwargs={"sources_resources": sources_resources})
    )

    search_enrich = build_search_enrich(flow,
                                        fb_ig_sources_resources,
                                        "linkedinAggregation",
                                        full_search_enrich=True)

    flow = search_enrich.get("flow")
    client_params = search_enrich.get("client_params")
    next_step_needs = search_enrich.get("next_step_needs")

    flow = (flow.add(
        uses=PrimaryCandidate,
        needs=next_step_needs,
        name="fbIgPrimaryCandidate",
    ).add(
        uses=Aggregation,
        name="FbIgAggregation",
        needs="fbIgPrimaryCandidate",
    ).add(
        uses=SearchOut,
        name="searchOut",
        needs="FbIgAggregation",
    ))

    response = []

    li_search_params = {
        executor.get("name") + "__kwargs": executor.get("uvicorn_kwargs")
        for executor in li_executors
    }

    li_reducer_params = {
        "linkedinAPIReducer__flow_step": "search",
        "linkedinAPIReducer__sources_resources": sources_resources,
        "linkedinAPIReducer__no_enrich": True
    }

    aggregation_params = {"linkedinAggregation__sources_resources":
                          sources_resources}

    client_params = {**client_params,
                     **li_search_params,
                     **li_reducer_params,
                     **aggregation_params}

    with flow as f:  # Using it as a Context Manager will start the Flow
        client = Client(port=f.port, protocol=f.protocol, asyncio=True)
        async for resp in client.post(
            "/search",
            inputs=DocumentArray[SearchRequestDoc](docs),
            return_type=DocumentArray[
                Union[FacebookResponseDoc, InstagramResponseDoc,
                      LinkedinResponseDoc]
            ],
            request_size=len(sources_resources),
            parameters={
                **client_params
            },
        ):
            for doc in resp:
                response.append(doc)
        return response


def build_search_enrich(flow,
                        sources_resources,
                        search_executors_needs="searchIn",
                        full_search_enrich=False):
    search_executors = build_executors_list(sources_resources,
                                            search_executors_needs,
                                            "search")

    for executor in search_executors:
        flow = flow.add(**executor)

    flow = flow.add(
        uses=ResultAPIReducer,
        name="search_APIReducer",
        needs=[executor.get("name") for executor in search_executors],
        no_reduce=True,
        uvicorn_kwargs={"sources_resources": sources_resources}
    )

    search_executors_params = {
        executor.get("name") + "__kwargs": executor.get("uvicorn_kwargs")
        for executor in search_executors
    }

    search_reducer_params = {
        "search_APIReducer__sources_resources": sources_resources,
        "search_APIReducer__flow_step": "search",
        "search_APIReducer__no_enrich": full_search_enrich}

    return_dict = {}

    if full_search_enrich is True:

        enrich_executors = build_executors_list(sources_resources,
                                                "search_APIReducer",
                                                "enrich")

        for executor in enrich_executors:
            flow = flow.add(**executor)

        flow = flow.add(
            uses=ResultAPIReducer,
            name="enrich_APIReducer",
            needs=[executor.get("name") for executor in enrich_executors],
            no_reduce=True,
            uvicorn_kwargs={"sources_resources": sources_resources}
        )

        enrich_executors_params = {
            executor.get("name") + "__kwargs": executor.get("uvicorn_kwargs")
            for executor in enrich_executors
        }

        enrich_reducer_params = {
            "enrich_APIReducer__sources_resources": sources_resources,
            "enrich_APIReducer__flow_step": "enrich",
            "enrich_APIReducer__no_enrich": False}

        client_params = {
            **search_executors_params,
            **enrich_executors_params,
            **search_reducer_params,
            **enrich_reducer_params}

        return_dict["next_step_needs"] = "enrich_APIReducer"

    else:
        client_params = {
            **search_executors_params,
            **search_reducer_params}

        return_dict["next_step_needs"] = "search_APIReducer"

    return_dict["flow"] = flow
    return_dict["client_params"] = client_params

    return return_dict
