from jina import Client, DocumentArray
from core.documents import SearchRequestDoc

docs = DocumentArray[SearchRequestDoc]()
docs.append(SearchRequestDoc(
    urn="urn:signaight:person:8ada2ff7-4e3b-4702-af1d-5b46ce10a7e1",
    name="Yonit",
    resource="web_scraper"
))

c = Client(port=51235)
c.post(on='/enrich', inputs=docs)
