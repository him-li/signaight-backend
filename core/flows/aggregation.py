from jina import Client
from docarray import DocList
from asyncio import sleep
from core.documents import (
    AggregateRequestDoc,
)

from core.config import settings
from core.utils import build_urn


async def aggregation_flow(
    person_id: str,
    candidate_id: str,
    host: str = None
):
    p_id = format(str(person_id))
    c_id = format(str(candidate_id))

    docs_in = build_aggregate_docarray(p_id, c_id)
    doc_out = await aggregate_data(docs_in, host)
    return doc_out


async def aggregate_data(docs, host: str = None):
    ''' outdated form of flow
    flow = (
        Flow(protocol="grpc")
        .add(uses=Aggregation, name="aggregate")
    )
    flow = (
        Flow(
            protocol="GRPC",
            timeout_ctrl=12000,
            grpc_server_options={
                "grpc.keepalive_time_ms": 100000,
                "grpc.keepalive_timeout_ms": 50000,
                "grpc.keepalive_permit_without_calls": True,
                "grpc.http2.max_ping_strikes": 5,
                "grpc.http2.min_ping_interval_without_data_ms": 10000
            }
        )
        .config_gateway(cors=True)
        .add(uses=Aggregation, name="aggregate")
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


    response = []

    if not host:
        flow.start()
    client = Client(**params)
    while not await client._is_flow_ready():
        sleep(1)

    async for resp in client.post(
        "/enrich",
        inputs=DocList[AggregateRequestDoc](docs),
        target_executor="Aggregate*",
        parameters={
            "rule_set_skipping": True,
        },
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
        urn=build_urn("person", str(person_id))
    )
    docs = []
    docs.append(doc)
    return docs
