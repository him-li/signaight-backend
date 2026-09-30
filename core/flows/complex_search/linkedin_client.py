from jina import Client
from jina.excepts import InternalNetworkError
from typing import List
from aiohttp import ClientError
from asyncio import sleep, CancelledError
from uuid import UUID
from docarray import DocList
from grpc.aio import AioRpcError
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
    AggregateRequestDoc
)
from core.logging import logger
from core.models import SearchEventModel, PersonModel, CandidateModel
from core.utils.urn import build_urn, SignAIghtURN
from core.config import settings

from .utils import (
    # create_enrich_doc,
    # create_enrich_doc_list,
    create_enrich_doc_list_candidate_urn)


async def linkedin_client_run(
    search_id,
    persons,
    search_docs: List[SearchRequestDoc],
    enrich_docs: List[EnrichRequestDoc],
    host: str = None,
):
    params = {
        "async": True
    }
    # initiate flow locally if there remote is not set
    if not host:
        params['protocol'] = ['GRPC']
        params['port'] = 51324
        from .flow import build_complex_flow
        flow = build_complex_flow(
            port=params['port'],
            protocol=params['protocol']
        )
    else:
        # docarray expose iterable object instead string
        params['host'] = str(host)  # 'jina-linkedin-flow'
        # params['protocol'] = 'http' #settings.JINA_REMOTE_FLOW_LINKEDIN.scheme
        # params['host'] = 'jina-linkedin-flow' #settings.JINA_REMOTE_FLOW_LINKEDIN.host
        # params['port'] = 5124 #settings.JINA_REMOTE_FLOW_LINKEDIN.port


    flow_finished = False
    # if flow is local control it manually
    if not host:
        flow.start()
    try:
        client = Client(**params)
        while not await client._is_flow_ready():
            await sleep(1)
        # 1 step - search in google, facebook and instagram

        async for resp in client.post(
                on='/search',
                inputs=search_docs,
                target_executor='Search*',
                parameters={
                    'source': ["facebook",
                                "instagram",
                                # "twitter", # disabled due not paid api access
                                "xing",
                                "grayfox",
                                "google",
                                "eumw",
                                "interpol"
                               ],
                    'resource': "vetric",
                    'SearchWebScraper__google': {'pages': 2},
                    'SearchFacebookAPI__search_fields': [
                        ['f_name', 'l_name', 'work'],
                        ['f_name', 'l_name', 'city'],
                        ['f_name', 'l_name', 'education'],
                        ['email_address'],
                    ],
                    'SearchFacebookAPI__rare_name_fields': [
                        'f_name', 'l_name'],
                    'SearchInstagramAPI__search_fields': [
                        ['f_name', 'l_name', 'city'],
                        ['f_name', 'l_name', 'bio'],
                        ['email_address'],
                        ['username'],
                    ],
                    'SearchInstagramAPI__rare_name_fields': [
                        'f_name', 'l_name'],
                    'SearchWebScraper__google_search_fields': [
                        ['f_name', 'l_name', 'work'],
                        ['f_name', 'l_name', 'education'],
                        ['f_name', 'l_name', 'bio'],
                        ['f_name', 'l_name', 'email_address'],
                    ],
                    'SearchWebScraper__google_rare_name_fields': [
                        'f_name', 'l_name'],
                    # backward compatibility params
                    'flow_step': 'search',
                }
        ):
            pass

        async for resp in client.post(
            on='/enrich',
            inputs=enrich_docs,
            return_type=DocList[EnrichRequestDoc],
            target_executor='Enrich*',
            parameters={
                'source': "linkedin",
                'resource': "vetric"
            }
        ):
            search = await SearchEventModel.get(search_id)
            for _doc in resp:
                urn = SignAIghtURN.parse(_doc.urn)
                # NOTE: person request to db is workaround cause enrich respond
                # does not contain proper data for some reason
                person = await PersonModel.get(UUID(urn.id))
                person.search_id = str(search_id)
                li_candidate = CandidateModel(
                    source='linkedin',
                    resource='vetric',
                    person=UUID(urn.id),
                    searched_at=search.created_at,
                    primary=True,
                    **person.model_dump()
                )
                await li_candidate.insert()

        # 2 step 1 stage - choose primary candidates
        # by face comparison service enrichment
        # multiple calls used to ensure full comparison
        second_enrich_docs = []
        async for resp in client.post(
            on='/enrich',
            inputs=enrich_docs,
            target_executor='ComparePrimaryCandidateByFace',
        ):
            for doc in resp:
                enrich_docs = await create_enrich_doc_list_candidate_urn(
                    doc, search_id)
                if enrich_docs:
                    second_enrich_docs.extend(enrich_docs)
                else:
                    continue
        if (not any(doc.source == 'facebook' for doc in second_enrich_docs) and
           not any(doc.source == 'instagram' for doc in second_enrich_docs)):
            async for resp in client.post(
                on='/enrich',
                inputs=enrich_docs,
                target_executor='ComparePrimaryCandidateByFace',
            ):
                for doc in resp:
                    enrich_docs = await create_enrich_doc_list_candidate_urn(
                        doc, search_id)
                    if enrich_docs:
                        second_enrich_docs.extend(enrich_docs)
                    else:
                        continue
        if (not any(doc.source == 'facebook' for doc in second_enrich_docs) and
           not any(doc.source == 'instagram' for doc in second_enrich_docs)):
            async for resp in client.post(
                on='/enrich',
                inputs=enrich_docs,
                target_executor='ComparePrimaryCandidateByFace',
            ):
                for doc in resp:
                    enrich_docs = await create_enrich_doc_list_candidate_urn(
                        doc, search_id)
                    if enrich_docs:
                        second_enrich_docs.extend(enrich_docs)
                    else:
                        continue

        # NOTE: Multiple Facebook searches deprecated, because they are
        #  already in first search

        # # 2 step 2 stage - choose primary candidates
        # # try to compare by facebook image
        # if not any(doc.source == 'facebook' for doc in second_enrich_docs):
        #     for doc in search_docs:
        #         doc.work = None
        #     async for resp in client.post(
        #             on='/search',
        #             inputs=search_docs,
        #             target_executor='Search*',
        #             parameters={
        #                 'source': ["facebook"],
        #                 'resource': "vetric",
        #                 # backward compatibility params
        #                 'flow_step': 'search',
        #             }
        #     ):
        #         pass

        #     async for resp in client.post(
        #         on='/enrich',
        #         inputs=enrich_docs,
        #         target_executor='ComparePrimaryCandidateByFace',
        #     ):
        #         for doc in resp:
        #             enrich_doc = await create_enrich_doc(doc, search_id)
        #             if enrich_doc:
        #                 second_enrich_docs.append(enrich_doc)
        #             else:
        #                 continue

        # if not any(doc.source == 'facebook' for doc in second_enrich_docs):
        #     for doc in search_docs:
        #         doc.city = None
        #     async for resp in client.post(
        #             on='/search',
        #             inputs=search_docs,
        #             target_executor='Search*',
        #             parameters={
        #                 'source': ["facebook"],
        #                 'resource': "vetric",
        #                 # backward compatibility params
        #                 'flow_step': 'search',
        #             }
        #     ):
        #         pass

        #     async for resp in client.post(
        #         on='/enrich',
        #         inputs=enrich_docs,
        #         target_executor='Compare*',
        #     ):
        #         for doc in resp:
        #             enrich_doc = await create_enrich_doc(doc, search_id)
        #             if enrich_doc:
        #                 second_enrich_docs.append(enrich_doc)
        #             else:
        #                 continue

        # if not any(doc.source == 'facebook' for doc in second_enrich_docs):
        #     for doc in search_docs:
        #         doc.education = None
        #     async for resp in client.post(
        #             on='/search',
        #             inputs=search_docs,
        #             target_executor='Search*',
        #             parameters={
        #                 'source': ["facebook"],
        #                 'resource': "vetric",
        #                 # backward compatibility params
        #                 'flow_step': 'search',
        #             }
        #     ):
        #         pass

        #     async for resp in client.post(
        #         on='/enrich',
        #         inputs=enrich_docs,
        #         target_executor='Compare*',
        #     ):
        #         for doc in resp:
        #             enrich_doc = await create_enrich_doc(doc, search_id)
        #             if enrich_doc:
        #                 second_enrich_docs.append(enrich_doc)
        #             else:
        #                 continue
        # NOTE: hack for websearch data post search processing
        websearch_enrich_docs = []
        for person_id in persons:
            websearch_enrich_docs.append(EnrichRequestDoc(
                urn=build_urn('persons', str(person_id)),
                search_id=str(search_id),
                source="google"
            ))
        if second_enrich_docs or websearch_enrich_docs:
            # 4 step - conditional enrichment if primary candidate found
            async for resp in client.post(
                on='/enrich',
                inputs=second_enrich_docs+websearch_enrich_docs,
                target_executor='Search*',
                parameters={
                    'source': [
                        "facebook",
                        "instagram",
                        "xing",
                        "interpol",
                        "google"
                    ],
                    'resource': "vetric",
                    # backward compatibility params
                    'flow_step': "enrich"
                }
            ):
                pass
        # 5 step - candidate data aggregation into person
        aggregate_docs = []
        for person_id in persons:
            aggregate_docs.append(AggregateRequestDoc(
                person_id=str(person_id),
                urn=build_urn('persons', str(person_id)),
                search_id=str(search_id),
            ))

        async for resp in client.post(
            on='/enrich',
            inputs=aggregate_docs,
            target_executor='AggregateCandidatesToPersons'
        ):
            for doc in resp:
                print(doc)

        # NOTE: add here post enrich processing for websearch entities with
        # with full set of person data for ai analyze
        if websearch_enrich_docs:
            async for resp in client.post(
                on='/enrich',
                inputs=websearch_enrich_docs,
                target_executor='SearchWebScraper',
                parameters={
                    'source': ["google"],
                    'SearchWebScraper__google': {'postprocess': True},
                }
            ):
                pass
        flow_finished = True
    except (AioRpcError, ClientError, InternalNetworkError) as e:
        logger.error("linkedin flow")
        logger.error(e.code())
        logger.error(type(e))
        logger.error(e)
    except CancelledError as e:
        logger.error("linkedin flow")
        logger.error(type(e))
        logger.error(e)
    except Exception as e:
        logger.error("linkedin flow")
        logger.error(type(e))
        logger.error(e)

    # if flow is local control it manually
    if not host:
        flow.close()

    return flow_finished
