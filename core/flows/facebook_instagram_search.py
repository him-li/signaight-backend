import uuid
from jina import Flow, Client
from docarray import DocList
from typing import List

from services.SearchIn.executor import SearchIn
from services.FacebookAPI.executor import FacebookAPI
from services.InstagramAPI.executor import InstagramAPI
from services.ResultAPIReducer.executor import ResultAPIReducer

from core.documents import SearchRequestDoc
from core.models import PersonModel
from core.utils import build_urn


async def facebook_instagram_search_flow(
    persons: List[PersonModel],
    search_id: uuid.UUID = uuid.uuid4()
):
    search_docs = DocList[SearchRequestDoc]()
    for person in persons:
        person_urn = build_urn("persons", str(person.id))
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
            uses=SearchIn,
            name="SearchIn",
        ).add(
            uses=FacebookAPI,
            name="SearchFacebookAPI",
            needs="SearchIn"
        ).add(
            uses=InstagramAPI,
            name="SearchInstagramAPI",
            needs="SearchIn"
        ).add(
            uses=ResultAPIReducer,
            name="SearchResultAPIReducer",
            needs=[
                'SearchFacebookAPI',
                'SearchInstagramAPI'
            ],
            no_reduce=True
        )

    with flow as f:  # Using it as a Context Manager will start the Flow
        client = Client(
            port=f.port,
            protocol=f.protocol,
            asyncio=True,
        )
        async for resp in client.post(
                on='/search',
                inputs=search_docs,
                target_executor='Search*',
                parameters={
                    'source': ["facebook", "instagram"],
                    'resource': "vetric",
                    # backward compatibility params
                    'flow_step': 'search',
                }
                ):
            for doc in resp:
                print(doc)
