from jina import Flow
from services.SearchIn.executor import SearchIn
from services.SearchOut.executor import SearchOut
from services.Aggregation.executor import Aggregation
from services.LinkedinAPI.executor import LinkedinAPI
from services.FacebookAPI.executor import FacebookAPI
from services.InstagramAPI.executor import InstagramAPI
from services.ResultAPIReducer.executor import ResultAPIReducer
from services.ResultAPIMerger.executor import ResultAPIMerger
from services.PrimaryCandidateByFaceCompare.executor import (
    PrimaryCandidateByFaceCompare
)
from services.ProfilerAPI.executor import ProfilerAPI
from typing import List

from core.config import settings

def build_executors_replica_list(
    name: str,
    replicas: int,
    port: int=55961
) -> List[str]:
    if settings.JINA_KUBERNETES_MODE:
        k8s_host_parts = [
            name,
            settings.ENVIRONMENT,
            settings.JINA_KUBERNETES_HOSTS_SUFFIX
        ]
        return [('.').join(k8s_host_parts)]
    else:
        return [f"grpc://{name}-{num}:{port}" for num in range(1, replicas+1)]


def build_complex_flow(
    port: int = 51234,
    protocol: List = ['GRPC'],
):
    params = {
        "timeout_ctrl": 12000,
        "port": port,
        "protocol": protocol,
        "prefetch": 16,
        #"retries": 5,
        #"timeout_send": 1800*1000,
        #"timeout_ready": -1,
        "asyncio": True,
        "grpc_server_options": {
            "grpc.keepalive_time_ms": 7200000,
            "grpc.keepalive_timeout_ms": 100000,
            "grpc.keepalive_permit_without_calls": True,
            "grpc.http2.max_ping_strikes": 0,
            "grpc.http2.min_ping_interval_without_data_ms": 100000
        },
    }
    if settings.JINA_REMOTE_FLOW_LINKEDIN:
        params['port'] = settings.JINA_REMOTE_FLOW_LINKEDIN.port
        params['protocol'] = [settings.JINA_REMOTE_FLOW_LINKEDIN.scheme]

    if settings.JINA_REMOTE_EXECUTORS:
        external_config = {
            #'protocol': protocol,
            #'port': [55961],
            #'replicas': 2,
            'polling': 'ANY',
            'external': True
        }
        return Flow(**params).config_gateway(cors=True).add(
            uses=SearchIn,
            name="SearchIn",
        ).add(
            name="SearchFacebookAPI",
            needs="SearchIn",
            host=build_executors_replica_list(
                "jina-executor-facebookapi",
                settings.JINA_EXECUTOR_FACEBOOKAPI_REPLICAS
            ),
            **external_config
        ).add(
            name="SearchInstagramAPI",
            needs="SearchIn",
            host=build_executors_replica_list(
                "jina-executor-instagramapi",
                settings.JINA_EXECUTOR_INSTAGRAMAPI_REPLICAS
            ),
            **external_config
        # ).add(
        #     name="SearchWebScraper",
        #     needs="SearchIn",
        #     host=build_executors_replica_list(
        #         "jina-executor-webscraper",
        #         settings.JINA_EXECUTOR_WEBSCRAPER_REPLICAS
        #     ),
        #    **external_config
        ).add(
            name="SearchProfilerAPI",
            needs="SearchIn",
            host=build_executors_replica_list(
                "jina-executor-profilerapi",
                settings.JINA_EXECUTOR_FACEBOOKAPI_REPLICAS
            ),
            **external_config
        ).add(
            uses=ResultAPIMerger,
            name="SearchResultAPIMerger",
            needs=[
                'SearchFacebookAPI',
                'SearchInstagramAPI',
                #'SearchTwitterAPI',
                #'SearchWebScraper',
                'SearchProfilerAPI'
            ],
            replicas=5,
            no_reduce=True
        ).add(
            name="SearchResultAPIReducer",
            needs='SearchResultAPIMerger',
            host=build_executors_replica_list(
                "jina-executor-resultapireducer",
                settings.JINA_EXECUTOR_RESULTAPIREDUCER_REPLICAS
            ),
            **external_config
        ).add(
            uses=SearchOut,
            name="TransitionNode",
            floating=True,
        ).add(
            name="EnrichLinkedinAPI",
            host=build_executors_replica_list(
                "jina-executor-linkedinapi",
                settings.JINA_EXECUTOR_LINKEDINAPI_REPLICAS
            ),
            **external_config
        ).add(
            uses=ResultAPIMerger,
            name="EnrichResultAPIMerger",
            needs='EnrichLinkedinAPI',
            replicas=5,
            no_reduce=True
        ).add(
            name="EnrichResultAPIReducer",
            needs='EnrichResultAPIMerger',
            host=build_executors_replica_list(
                "jina-executor-resultapireducer",
                settings.JINA_EXECUTOR_RESULTAPIREDUCER_REPLICAS
            ),
            **external_config
        ).add(
            uses=PrimaryCandidateByFaceCompare,
            name="ComparePrimaryCandidateByFace",
            host=build_executors_replica_list(
                "jina-executor-primarycandidatebyfacecompare",
                settings.JINA_EXECUTOR_PRIMARYCANDIDATEBYFACECOMPARE_REPLICAS
            ),
            **external_config
        ).add(
            name="AggregateCandidatesToPersons",
            host=build_executors_replica_list(
                "jina-executor-aggregation",
                settings.JINA_EXECUTOR_AGGREGATION_REPLICAS
            ),
            **external_config
        )
    else:
        return Flow(**params).config_gateway(cors=True).add(
            uses=SearchIn,
            name="SearchIn",
        ).add(
            uses=FacebookAPI,
            name="SearchFacebookAPI",
            needs="SearchIn",
        ).add(
            uses=InstagramAPI,
            name="SearchInstagramAPI",
            needs="SearchIn",
        #).add(
        #    uses=WebScraper,
        #    name="SearchWebScraper",
        #    needs="SearchIn",
        ).add(
            uses=ProfilerAPI,
            name="SearchProfilerAPI",
            needs="SearchIn",
        ).add(
            uses=ResultAPIMerger,
            name="SearchResultAPIMerger",
            needs=[
                'SearchFacebookAPI',
                'SearchInstagramAPI',
                #'SearchTwitterAPI',
                #'SearchWebScraper',
                'SearchProfilerAPI'
            ],
            replicas=5,
            no_reduce=True
        ).add(
            uses=ResultAPIReducer,
            name="SearchResultAPIReducer",
            needs='SearchResultAPIMerger',
        ).add(
            uses=SearchOut,
            name="TransitionNode",
            floating=True,
        ).add(
            uses=LinkedinAPI,
            name="EnrichLinkedinAPI",
        ).add(
            uses=ResultAPIMerger,
            name="EnrichResultAPIMerger",
            needs='EnrichLinkedinAPI',
        ).add(
            uses=ResultAPIReducer,
            name="EnrichResultAPIReducer",
            needs='EnrichResultAPIMerger',
            replicas=5,
            no_reduce=True
        ).add(
            uses=PrimaryCandidateByFaceCompare,
            name="ComparePrimaryCandidateByFace",
        ).add(
            uses=Aggregation,
            name="AggregateCandidatesToPersons",
        )
