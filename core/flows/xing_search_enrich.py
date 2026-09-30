import uuid
from jina import Flow, Client
from docarray import DocList
from typing import List
from asyncio import sleep

from core.config import settings
from services.SearchIn.executor import SearchIn
from services.WebScraper.executor import WebScraper
from services.ResultAPIReducer.executor import ResultAPIReducer


from core.models import PersonModel
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
)
from core.utils import build_urn


async def xing_search_enrich_flow(
    persons: List[PersonModel],
    search_id: uuid.UUID = uuid.uuid4(),
    host: str = None
):
    search_docs = DocList()
    enrich_docs = DocList()
    for person in persons:
        person_urn = build_urn("persons", str(person.id))
        # TODO: maybe use utils function core.build_search_docarray
        search_doc = SearchRequestDoc(
            name=person.personal_details.name.full_name.full_name,
            urn=person_urn,
            search_id=str(search_id),
            f_name=person.personal_details.name.first_name.f_name,
            l_name=person.personal_details.name.last_name.l_name,
            # TODO: resource in doc deprecated value and should removed soon
            resource='vetric',
        )
        try:
            search_doc.email_address = (person.personal_details
                                        .email.email_address[0])
        except Exception:
            pass
        search_docs.append(search_doc)
    '''
    flow = Flow(
        timeout_ctrl=1200,
        grpc_server_options={
            "grpc.keepalive_time_ms": 10000,
            "grpc.keepalive_timeout_ms": 5000,
            "grpc.keepalive_permit_without_calls": True,
            "grpc.http2.max_ping_strikes": 0,
            "grpc.http2.min_ping_interval_without_data_ms": 10000
        },
    ).add(
        uses=WebScraper,
        name="SearchWebScraper",
    ).add(
        uses=ResultAPIReducer,
        name="SearchResultAPIReducer",
        needs=[
            'SearchWebScraper'
        ],
        no_reduce=True
    )
    '''
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

    if not host:
        flow.start()
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)

    # with flow as f:  # Using it as a Context Manager will start the Flow
    #    client = Client(
    #        port=f.port,
    #        protocol=f.protocol,
    #        asyncio=True,
    #    )
        # 1 step - search in xing
    enrich_docs = []
    async for resp in client.post(
            on='/search',
            inputs=search_docs,
            target_executor='Search*',
            parameters={
                'source': ["xing"],
                'resource': "WebScraper",
                'SearchSERP__pages': 2,
                # backward compatibility params
                'flow_step': 'search',
            }
    ):
        for doc in resp:
            print("search resp doc")
            print(doc)
            if doc.doctype == "SearchResponseDoc":
                enrich_docs.append(
                    EnrichRequestDoc(
                        urn=doc.urn,
                        search_id=str(search_id),
                        profile_url=(doc.network_signature.get(
                            "url").get("xing_profile_url")),
                        source=doc.source,
                    )
                )

    if enrich_docs:
        # 2 step - conditional enrichment if search results found
        async for resp in client.post(
            on='/enrich',
            inputs=enrich_docs,
            target_executor='Search*',
            parameters={
                'source': ["xing"],
                'resource': "WebScraper",
                # backward compatibility params
                'flow_step': "enrich",
                # 'doc' : enrich_docs[0]
            }
        ):
            for doc in resp:
                print(doc)
