from jina import Client
from asyncio import sleep
from docarray import DocList
from typing import Union

from core.documents import (
    ActiveSearchRequestDoc,
)

from core.config import settings
from core.utils import build_urn


async def active_search_flow(
    search_id,
    title: str = None,
    education: str = None,
    location: Union[int, str] = None,
    host: str = None,
):
    search_docs = DocList[ActiveSearchRequestDoc]()
    active_search_doc = ActiveSearchRequestDoc(
        urn=build_urn("events", str(search_id)),
        title=title,
        education=education,
        location=location,
        search_id=str(search_id),
        resource='grayfox',
    )
    search_docs.append(active_search_doc)

    params = {
        "async": True
    }
    # initiate flow locally if there remote is not set
    if not host:
        from .complex_search.flow import build_complex_flow
        flow = build_complex_flow()
    else:
        # docarray expose iterable object instead string
        params['host'] = str(host)  # 'jina-linkedin-flow'
        # params['protocol'] = 'http' #settings.JINA_REMOTE_FLOW_LINKEDIN.scheme
        # params['host'] = 'jina-linkedin-flow' #settings.JINA_REMOTE_FLOW_LINKEDIN.host
        # params['port'] = 5124 #settings.JINA_REMOTE_FLOW_LINKEDIN.port


    # if flow is local control it manually
    if not host:
        flow.start()
    # try:
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)
    # 1 step - search in google, facebook and instagram
    async for resp in client.post(
            on='/active_search',
            inputs=search_docs,
            target_executor='Search*',
            parameters={
                'source': ["grayfox"],
                'resource': "grayfox",
                'SearchSERP__pages': 2,
                # backward compatibility params
                'flow_step': 'search',
            }
    ):
        for doc in resp:
            print(doc)
        pass

    # except Exception as e:
    #    print(str(e))
    # if flow is local control it manually
    if not host:
        flow.close()
