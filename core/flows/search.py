from jina import Flow, Client

from services.SearchSERP.executor import SearchSERP


async def search_serp(
        person_id,
        query,
        lang='en',
        pages=2):
    flow = Flow().add(uses=SearchSERP, name="SearchSERP")

    with flow as f:  # Using it as a Context Manager will start the Flow
        client = Client(port=f.port, protocol=f.protocol, asyncio=True)
        async for resp in client.post(
            "/search",
            parameters={
                'SearchSERP__person_id': person_id,
                'SearchSERP__query': query,
                'SearchSERP__pages': pages,
            }
        ):
            for doc in resp:
                print(doc)
