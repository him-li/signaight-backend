from core.utils.normalize_list import normalize_to_list
from jina import Flow, Client
from docarray import DocList
from typing import List

from core.documents import EnrichRequestDoc, EnrichResponseDoc
from core.models import PersonModel
from core.utils import build_urn

from services.TwitterAPI.executor import TwitterAPI
from services.ResultAPIReducer.executor import ResultAPIReducer


async def twitter_enrich_flow(
    persons: List[PersonModel]
):

    enrich_docs = DocList[EnrichRequestDoc]()

    for person in persons:
        person_id = person.id
        ns = getattr(person, "network_signature", None)
        if not ns:
            continue

        matched = getattr(ns, "matched_profiles", None)
        if not matched:
            continue

        twitter_match = getattr(matched, "twitter", None)
        if not twitter_match:
            continue

        primary = getattr(twitter_match, "primary_candidate", None) or {}
        if not primary:
            continue

        urn = build_urn("persons", str(person_id))

        for candidate_data in primary.values():
            source_id = getattr(candidate_data, "profile_id", None)
            username = getattr(candidate_data, "profile_username", None)
            profile_urls = normalize_to_list(
                getattr(candidate_data, "profile_url", None)
            )

            enrich_docs.append(
                EnrichRequestDoc(
                    urn=urn,
                    source_id=source_id,
                    resource="vetric",
                    source="twitter",
                    username=username,
                    profile_url=str(profile_urls[0]) if profile_urls else None,
                )
            )

    if not enrich_docs:
        return []

    flow = (
        Flow(
            protocol="GRPC",
            timeout_ctrl=12000,
            grpc_server_options={
                "grpc.keepalive_time_ms": 100000,
                "grpc.keepalive_timeout_ms": 50000,
                "grpc.keepalive_permit_without_calls": True,
                "grpc.http2.max_ping_strikes": 5,
                "grpc.http2.min_ping_interval_without_data_ms": 10000,
            },
        )
        .config_gateway(cors=True)
        .add(
            uses=TwitterAPI,
            name="EnrichTwitterAPI",
        )
        .add(
            uses=ResultAPIReducer,
            name="EnrichResultAPIReducer",
            needs=["EnrichTwitterAPI"],
            no_reduce=True,
        )
    )

    response = []

    with flow:
        client = Client(asyncio=True)

        async for resp in client.post(
            "/enrich",
            inputs=enrich_docs,
            return_type=DocList[EnrichResponseDoc],
            request_size=1,
            parameters={
                "source": ["twitter"],
                "resource": "vetric",
                "flow_step": "enrich",
            },
        ):
            response.extend(resp)

    return response
