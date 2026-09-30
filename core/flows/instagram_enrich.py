from core.utils.normalize_list import normalize_to_list
from jina import Client
from docarray import DocList
from typing import List
from asyncio import sleep

from core.config import settings
from core.documents import EnrichRequestDoc
from core.models import PersonModel
from core.utils import build_urn


async def instagram_enrich_flow(
    persons: List[PersonModel],
    host: str = None
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

        instagram_match = getattr(matched, "instagram", None)
        if not instagram_match:
            continue

        primary = getattr(instagram_match, "primary_candidate", None) or {}
        if not primary:
            continue

        urn = build_urn("persons", str(person_id))

        for candidate_id, candidate_data in primary.items():
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
                    source="instagram",
                    username=username,
                    profile_url=str(profile_urls[0]) if profile_urls else None,
                )
            )

    if not enrich_docs:
        return []

    params = {"async": True}

    if not host:
        from .complex_search.flow import build_complex_flow
        flow = build_complex_flow()
    else:
        params["host"] = str(host)

    response = []

    if not host:
        flow.start()

    client = Client(**params)

    while not await client._is_flow_ready():
        await sleep(1)  # FIXED (must await)

    async for resp in client.post(
        "/enrich",
        target_executor="Search*",
        inputs=enrich_docs,
        parameters={
            "source": ["instagram"],
            "resource": "vetric",
            "flow_step": "enrich",
        },
    ):
        response.extend(resp)

    return response
