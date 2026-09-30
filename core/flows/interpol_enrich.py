from jina import Client, Flow
from docarray import DocList
from typing import List
from asyncio import sleep

from core.config import settings
from core.documents import (
    EnrichRequestDoc,
)
from core.models import PersonModel
from services.WebScraper.executor import WebScraper
from services.ResultAPIReducer.executor import ResultAPIReducer

from core.utils import build_urn


async def interpol_enrich_flow(
    persons: List[PersonModel],
    host: str = None
):
    enrich_docs = DocList[EnrichRequestDoc]()
    for person in persons:
        person_id = person.id
        source_resource = {"resource": "WebScraper", "source": "interpol"}
        profile_url = None

        try:
            profile_url = person.network_signature.url.interpol_profile_url
        except Exception:
            pass

        enrich_doc = EnrichRequestDoc(
            urn=build_urn("persons", str(person_id)),
            resource=source_resource.get("resource"),
            source=source_resource.get("source"),
            profile_url=str(profile_url)
        )
        enrich_docs.append(enrich_doc)

    params = {
        "async": True
    }
    # initiate flow locally if there remote is not set
    if not host:
        from .complex_search.flow import build_complex_flow
        flow = build_complex_flow()
    else:
        # docarray expose iterable object instead string
        params['host'] = str(host)


    '''
    flow = (
        Flow(
            protocol="GRPC",
            timeout_ctrl=12000,
            grpc_server_options={
                "grpc.keepalive_time_ms": 100000,
                "grpc.keepalive_timeout_ms": 50000,
                "grpc.keepalive_permit_without_calls": True,
                "grpc.http2.max_ping_strikes": 5,
                "grpc.http2.min_ping_interval_without_data_ms": 10000
            }
        )
        .config_gateway(cors=True)
        .add(
            uses=WebScraper,
            name="SearchWebScraper",
        )
        .add(
            uses=ResultAPIReducer,
            name="SearchResultAPIReducer",
            needs=["SearchWebScraper"],
            no_reduce=True
        )
    )
    '''

    response = []

    # if flow is local control it manually
    if not host:
        flow.start()
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)

    # with flow as f:
    #    client = Client(port=f.port, protocol=f.protocol, asyncio=True)
    async for resp in client.post(
        "/enrich",
        target_executor='Search*',
        inputs=enrich_docs,
        parameters={
            'source': ["interpol"],
            'resource': "web",
            # backward compatibility params
            'flow_step': 'enrich',
        },
    ):
        for doc in resp:
            response.append(doc)
        return response
