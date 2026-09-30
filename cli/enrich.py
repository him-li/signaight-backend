from jina import Flow, Client
from docarray import DocList
from typing import List, Dict, Union, Optional

from core.documents import (
    EnrichRequestDoc,
    FacebookEnrichDoc,
    InstagramEnrichDoc,
    LinkedinEnrichDoc
)
from cli.typer_async import AsyncTyper, Argument

from services.SearchIn.executor import SearchIn
from services.SearchOut.executor import SearchOut
from services.FacebookAPI.executor import FacebookAPI
from services.ResultAPIReducer.executor import ResultAPIReducer

from .base import build_executors_list
from core.utils import build_urn

app = AsyncTyper()


# DEPRECATED, new way in core.flows package
@app.async_command()
async def facebook(
    person_id: str = Argument(..., help="Person UUID"),
    source_id: str = Argument(..., help="Source Profile ID"),
    resource: str = Argument(..., help="API resource"),
):
    docs_in = build_enrich_docarray(person_id, source_id, resource)

    docs_out = await enrich_facebook_data(docs_in)
    return docs_out


# DEPRECATED, new way in core.flows package
async def enrich_facebook_data(docs):
    flow = (
        Flow(protocol="grpc")
        .add(uses=SearchIn, name="searchIn")
        .add(
            uses=FacebookAPI,
            name="facebookAPI",
            needs="searchIn",
        )
        .add(uses=ResultAPIReducer, name="resultAPIReducer",
             needs="facebookAPI")
        .add(uses=SearchOut, name="searchOut", needs="resultAPIReducer")
    )
    response = []
    with flow as f:
        client = Client(
            port=f.port,
            protocol=f.protocol,
            asyncio=True,
        )
        async for resp in client.post(
            "/enrich",
            DocList[EnrichRequestDoc](docs),
            return_type=DocList[FacebookEnrichDoc],
            request_size=1,
            show_progress=True,
        ):
            for doc in resp:
                response.append(doc)
    return response


def build_enrich_docarray(
    person_id: str,
    source_ids: Dict,
    sources_resources: List[Dict],
    usernames: Optional[Dict],
    profile_urls: Optional[Dict]
):
    docs = []
    for source_resource in sources_resources:
        source_id = source_ids.get(source_resource["source"])
        username = usernames.get(source_resource["source"])
        profile_url = profile_urls.get(source_resource["source"])

        doc = EnrichRequestDoc(
            urn=build_urn("persons", str(person_id)),
            source_id=source_id,
            resource=source_resource.get("resource"),
            source=source_resource.get("source"),
            username=username,
            profile_url=profile_url
        )
        docs.append(doc)
    return docs


# DEPRECATED, new way in core.flows package
async def all(
    person_id: str,
    source_ids: str,
    sources_resources: List[Dict],
    source_username: Optional[Dict],
    source_profile_url: Optional[Dict]
):
    """
    If argument or option value is string and contain few words encapsulate it
    in doublequotes. Ex: "Jhon Doe".

    Example of usage:
    $ python cli/main.py search all "jhon.doe@gmail.com"
    """
    docs = build_enrich_docarray(
        person_id,
        source_ids,
        sources_resources,
        source_username,
        source_profile_url
    )

    executors = build_executors_list(sources_resources, flow_step='enrich')

    flow = Flow().add(uses=SearchIn, name="searchIn")
    for executor in executors:
        flow = flow.add(**executor)

    flow = flow.add(
        uses=ResultAPIReducer,
        name="APIReducer",
        needs=[executor.get("name") for executor in executors],
        no_reduce=True,
    ).add(
        uses=SearchOut,
        name="searchOut",
        needs="APIReducer",
    )

    response = []

    with flow as f:  # Using it as a Context Manager will start the Flow
        client = Client(port=f.port, protocol=f.protocol, asyncio=True)
        async for resp in client.post(
            "/enrich",
            inputs=DocList[EnrichRequestDoc](docs),
            return_type=DocList[
                Union[FacebookEnrichDoc, InstagramEnrichDoc, LinkedinEnrichDoc]
            ],
            request_size=len(executors),
            parameters={
                executor.get("name") + "__name":
                executor.get("uvicorn_kwargs")
                for executor in executors
            },
        ):
            for doc in resp:
                response.append(doc)
        return response
