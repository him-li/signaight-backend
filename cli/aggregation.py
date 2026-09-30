from jina import Flow, Client
from docarray import DocList

from core.documents import (
    AggregateRequestDoc,
)
from cli.typer_async import AsyncTyper, Argument

from services.Aggregation.executor import Aggregation


app = AsyncTyper()


# DEPRECATED, new way in core.flows package
@app.async_command()
async def aggregate(
    person_id: str = Argument(..., help="Person UUID"),
    candidate_id: str = Argument(..., help="Candidate UUID"),
):
    p_id = format(str(person_id))
    c_id = format(str(candidate_id))

    docs_in = build_aggregate_docarray(p_id, c_id)
    doc_out = await aggregate_data(docs_in)
    return doc_out


async def aggregate_data(docs):
    flow = (
        Flow(protocol="grpc")
        .add(uses=Aggregation, name="aggregate")
    )
    response = []
    with flow as f:
        client = Client(
            port=f.port,
            protocol=f.protocol,
            asyncio=True,
        )
        async for resp in client.post(
            "/",
            DocList[AggregateRequestDoc](docs),
            request_size=1,
            show_progress=True,
        ):
            for doc in resp:
                response.append(doc)
    return response


def build_aggregate_docarray(
    person_id,
    candidate_id,
):
    doc = AggregateRequestDoc(
        person_id=person_id,
        candidate_id=candidate_id,
    )
    docs = []
    docs.append(doc)
    return docs
