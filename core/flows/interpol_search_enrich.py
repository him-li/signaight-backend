import uuid
from asyncio import sleep
from jina import Client
from docarray import DocList
from typing import List


from core.config import settings
from core.models import PersonModel
from core.documents import (
    SearchRequestDoc, EnrichRequestDoc
)
from core.utils import build_urn


async def interpol_search_flow(
    persons: List[PersonModel],
    search_id: uuid.UUID = uuid.uuid4(),
    host: str = None,
):
    search_docs = DocList()
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


    # if flow is local control it manually
    if not host:
        flow.start()
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)

    enrich_docs = []
    async for resp in client.post(
            on='/search',
            inputs=search_docs,
            target_executor='Search*',
            parameters={
                'source': ["interpol"],
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
                            "url").get("interpol_profile_url")),
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
                'source': ["interpol"],
                'resource': "WebScraper",
                # backward compatibility params
                'flow_step': "enrich",
                # 'doc' : enrich_docs[0]
            }
        ):
            for doc in resp:
                print(doc)
