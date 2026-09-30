from jina import Client
from docarray import DocList
from typing import List
from asyncio import sleep
import uuid

from core.config import settings
from core.documents import (
    EnrichRequestDoc, SearchRequestDoc
)
from core.models import PersonModel
from core.utils import build_urn


async def webscraper_search_flow(
    persons: List[PersonModel],
    search_id: uuid.UUID = uuid.uuid4(),
    host: str = None
):
    search_docs = DocList()
    for person in persons:
        person_id = person.id
        source_resource = {"resource": "vetric", "source": ["xing", "eumw"]}

        search_doc = SearchRequestDoc(
            urn=build_urn("persons", str(person_id)),
            name=person.personal_details.name.full_name.full_name,
            search_id=str(search_id),
            f_name=person.personal_details.name.first_name.f_name,
            l_name=person.personal_details.name.last_name.l_name,

            resource='vetric'
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


    response = []

    # # if flow is local control it manually
    if not host:
        flow.start()
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)

    async for resp in client.post(
        on="/search",
        target_executor='Search*',
        inputs=search_docs,
        parameters={
            'source': ["xing", "eumw"],
            'resource': "WebScraper",
            'SearchSERP__pages': 2,
            # backward compatibility params
            'flow_step': 'search',
        },
    ):
        for doc in resp:
            response.append(doc)
    return response
