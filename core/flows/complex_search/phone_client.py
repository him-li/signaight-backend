from core.dotty_dictionary import dotty
from core.utils.constants.primary_candidates import SIGNAIGHT_PHONE_FLOW_PRIMARY_CANDIDATE_SOURCES
from core.utils.get_names_list import name_resolution
from jina import Client
from typing import List
from asyncio import sleep


from core.clients.ds_app import api as ds_app_api
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
    AggregateRequestDoc
)
from core.logging import logger
from core.models import PersonModel
from core.utils import clean_person_name
from core.utils.urn import build_urn, parse_urn
from core.config import settings

from .utils import (
    get_person_education,
    get_person_city,
    get_person_work,
    # create_enrich_doc,
    create_enrich_doc_list,
    create_enrich_doc_list_candidate_urn as create_enrich_doc_list_cand_urn)


async def phone_client_run(
    search_id,
    persons,
    search_docs: List[SearchRequestDoc],
    enrich_docs: List[EnrichRequestDoc],
    host: str = None,
):
    params = {
        "async": True
    }
    linkedin_enrich_docs = []

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

    # if flow is local control it manually
    if not host:
        flow.start()

    flow_finished = False
    try:
        client = Client(**params)
        while not await client._is_flow_ready():
            await sleep(1)
        # 1 step - search in grayfox phone, and aggregate data from those candidates
        async for resp in client.post(
                on='/search',
                inputs=search_docs,
                target_executor='Search*',
                parameters={
                    'source': ["grayfox"],
                    'resource': "vetric",
                    # backward compatibility params
                    'flow_step': 'search',
                    'primary_candidate_sources': SIGNAIGHT_PHONE_FLOW_PRIMARY_CANDIDATE_SOURCES
                }
        ):
            pass

        grayfox_aggregate_docs = []
        for person_id in persons:
            grayfox_aggregate_docs.append(AggregateRequestDoc(
                person_id=str(person_id),
                urn=build_urn('persons', str(person_id)),
                search_id=str(search_id),
            ))
        async for resp in client.post(
            on='/enrich',
            inputs=grayfox_aggregate_docs,
            target_executor='AggregateCandidatesToPersons'
        ):
            pass

        for doc in search_docs:
            person_id = parse_urn(doc.urn)
            person = await PersonModel.get(person_id)
            try:
                if email_address := person.personal_details.email.email_address[0]:
                    doc.email_address = email_address
                    doc.phone_number = None

                    # 1 step - search in grayfox, and aggregate data from
                    # those candidates only if there is an email address
                    async for resp in client.post(
                            on='/search',
                            inputs=search_docs,
                            target_executor='Search*',
                            parameters={
                                'source': ["grayfox"],
                                'resource': "vetric",
                                # backward compatibility params
                                'flow_step': 'search',
                                'primary_candidate_sources': SIGNAIGHT_PHONE_FLOW_PRIMARY_CANDIDATE_SOURCES
                            }
                    ):
                        pass

                    grayfox_aggregate_docs = []
                    for person_id in persons:
                        grayfox_aggregate_docs.append(AggregateRequestDoc(
                            person_id=str(person_id),
                            urn=build_urn('persons', str(person_id)),
                            search_id=str(search_id),
                        ))
                    async for resp in client.post(
                        on='/enrich',
                        inputs=grayfox_aggregate_docs,
                        target_executor='AggregateCandidatesToPersons'
                    ):
                        pass
            except Exception as e:
                print(f"Grayfox search did not retrieve email: {e}")

        second_enrich_docs = []
        for doc in search_docs:
            person_id = parse_urn(doc.urn)
            person = await PersonModel.get(person_id)
            f_name = clean_person_name(
                person.personal_details.name.first_name.f_name)
            l_name = clean_person_name(
                person.personal_details.name.last_name.l_name)
            full_name = clean_person_name(
                person.personal_details.name.full_name.full_name)
            doc.f_name = f_name
            doc.l_name = l_name
            doc.name = full_name
            person_dict = dotty(person.model_dump())
            normalized_person_name = await name_resolution(person_dict)
            parts = normalized_person_name.strip().split() if normalized_person_name else []

            if len(parts) == 2:
                doc.f_name = parts[0]
                doc.l_name = parts[1]
                doc.name = f"{parts[0]} {parts[1]}"
            if len(parts) > 2:
                doc.f_name = parts[0]
                doc.l_name = " ".join(parts[1:])
                doc.name = f"{parts[0]} {' '.join(parts[1:])}"
            try:
                res = ds_app_api.ds_request.common_name(
                    body={"full_name": doc.name},
                    headers={
                        'x-remote-context': doc.urn
                    }
                )
                if res.body.get("common_name"):
                    doc.is_rare_name = False
            except Exception:
                pass
            try:
                try:
                    if linkedin_urls := (
                            person.network_signature.url.linkedin_profile_url):
                        print("linkedin_urls: ", linkedin_urls)
                        for url in linkedin_urls:
                            print(url)
                            enrich_docs.append(EnrichRequestDoc(
                                urn=doc.urn,
                                search_id=str(search_id),
                                # NOTE: pydantic v2 Url object could not be turned
                                # into string automatically and raise protobuf error
                                profile_url=str(url)
                            ))
                except Exception:
                    pass
                try:
                    if facebook_ids := (
                            person.network_signature.user_id.facebook_user_id):
                        print("facebook_ids", facebook_ids)
                        for facebook_id in facebook_ids:
                            print(facebook_id)
                            second_enrich_docs.append(EnrichRequestDoc(
                                urn=doc.urn,
                                search_id=str(search_id),
                                # NOTE: pydantic v2 Url object could not be turned
                                # into string automatically and raise protobuf error
                                source_id=facebook_id,
                                source='facebook'
                            ))
                except Exception:
                    pass
                try:
                    doc.city = get_person_city(person)
                except Exception:
                    pass
                try:
                    doc.education = get_person_education(person)
                except Exception:
                    pass
                try:
                    doc.work = get_person_work(person)
                except Exception:
                    pass
            except Exception:
                pass
            try:
                if any(person.network_signature.username.
                       model_dump().values()):
                    doc.username = next(iter(
                        person.network_signature.username.
                        model_dump().values()))
            except Exception:
                pass
            try:
                if any(person.biographic_details.description_bio_intro.
                       model_dump().values()):
                    doc.bio = next(iter(
                        person.biographic_details.description_bio_intro.
                        model_dump().values()))
            except Exception:
                pass

        # 2 step - if person has linkedin url, enrich linkedin,
        # else search linkedin in Vetric
        if enrich_docs:
            async for resp in client.post(
                on='/enrich',
                inputs=enrich_docs,
                target_executor='Enrich*',
                parameters={
                    'source': "linkedin",
                    'resource': "vetric"
                }
            ):
                pass
        else:
            async for resp in client.post(
                    on='/search',
                    inputs=search_docs,
                    target_executor='Enrich*',
                    parameters={
                        'source': ["linkedin"],
                        'resource': "vetric",
                        'SearchWebScraper__google': {'pages': 2},
                        # backward compatibility params
                        'flow_step': 'search',
                    }
            ):
                pass

            for doc in search_docs:
                enrich_doc = EnrichRequestDoc(
                    urn=doc.urn,
                    search_id=doc.search_id,
                    source='linkedin',
                    resource='vetric'
                )
                enrich_docs.append(enrich_doc)

            # 2 step 1 stage - choose linkedin primary candidate
            # by face comparison service enrichment

            async for resp in client.post(
                on='/enrich',
                inputs=enrich_docs,
                target_executor='ComparePrimaryCandidateByFace',
            ):
                for doc in resp:
                    enrich_doc_res = await create_enrich_doc_list(doc,
                                                                  search_id)
                    for enrich_doc in enrich_doc_res:
                        if enrich_doc and enrich_doc.source == 'linkedin':
                            linkedin_enrich_docs.append(enrich_doc)
                    else:
                        continue
                pass

            # 2 step 2 stage - enrich linkedin
            if linkedin_enrich_docs:
                async for resp in client.post(
                    on='/enrich',
                    inputs=linkedin_enrich_docs,
                    target_executor='Enrich*',
                    parameters={
                        'source': ["linkedin"],
                        'resource': "vetric"
                    }
                ):
                    pass

                # 2 step 3 stage - enrich aggregate
                linkedin_aggregate_docs = []
                for person_id in persons:
                    linkedin_aggregate_docs.append(AggregateRequestDoc(
                        person_id=str(person_id),
                        urn=build_urn('persons', str(person_id)),
                        search_id=str(search_id),
                    ))

                async for resp in client.post(
                    on='/enrich',
                    inputs=linkedin_aggregate_docs,
                    target_executor='AggregateCandidatesToPersons'
                ):
                    for doc in resp:
                        print(doc)

            for doc in search_docs:
                person_id = parse_urn(doc.urn)
                person = await PersonModel.get(person_id)
                if person:
                    try:
                        doc.city = get_person_city(person)
                    except Exception:
                        pass
                    try:
                        doc.education = get_person_education(person)
                    except Exception:
                        pass
                    try:
                        doc.work = get_person_work(person)
                    except Exception:
                        pass
                    try:
                        if any(person.network_signature.username.
                               model_dump().values()):
                            doc.username = next(iter(
                                person.network_signature.username.
                                model_dump().values()))
                    except Exception:
                        pass
                    try:
                        if any(person.biographic_details.description_bio_intro.
                               model_dump().values()):
                            doc.bio = next(iter(
                                person.biographic_details.
                                description_bio_intro.
                                model_dump().values()))
                    except Exception:
                        pass

        first_search_sources = ["instagram",
                                # "twitter", # disabled due not paid api access
                                "xing",
                                "google",
                                "eumw",
                                "interpol"
                                ]
        print("second_enrich_docs", second_enrich_docs)
        if not any(doc.source in ['facebook', 'facebook_grfx'] for
                   doc in second_enrich_docs):
            first_search_sources = ["facebook",
                                    *first_search_sources
                                    ]

        # 3 step - search in google, facebook and instagram
        async for resp in client.post(
                on='/search',
                inputs=search_docs,
                target_executor='Search*',
                parameters={
                    'source': first_search_sources,
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

        # 2 step 1 stage - choose primary candidates
        # by face comparison service enrichment
        # multiple calls used to ensure full comparison

        async for resp in client.post(
            on='/enrich',
            inputs=enrich_docs,
            target_executor='ComparePrimaryCandidateByFace',
        ):
            for doc in resp:
                enrich_doc_res = await create_enrich_doc_list_cand_urn(
                    doc, search_id)
                if enrich_doc_res:
                    second_enrich_docs.extend(enrich_doc_res)
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
                    enrich_doc_res = await create_enrich_doc_list_cand_urn(
                        doc, search_id)
                    if enrich_doc_res:
                        second_enrich_docs.extend(enrich_doc_res)
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
                    enrich_doc_res = await create_enrich_doc_list_cand_urn(
                        doc, search_id)
                    if enrich_doc_res:
                        second_enrich_docs.extend(enrich_doc_res)
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
        #         inputs=linkedin_enrich_docs,
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
    except Exception as e:
        logger.error("Phone flow")
        logger.error(type(e))
        logger.error(e)
        print(str(e))

    # if flow is local control it manually
    if not host:
        flow.close()

    return flow_finished
