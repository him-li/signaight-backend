import uuid
from core.utils.constants.primary_candidates import COMMON_PRIMARY_CANDIDATE_SOURCES
from jina import Client
from asyncio import sleep
from docarray import DocList

from core.utils import build_urn
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
)
from core.dotty_dictionary import dotty
from core.models import CandidateModel

from core.config import settings


async def grayfox_search_flow(
    search_id,
    persons,
    host: str = None,
):
    search_docs = DocList[SearchRequestDoc]()
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
        params['host'] = str(host)  # 'jina-linkedin-flow'
        # params['protocol'] = 'http' #settings.JINA_REMOTE_FLOW_LINKEDIN.scheme
        # params['host'] = 'jina-linkedin-flow' #settings.JINA_REMOTE_FLOW_LINKEDIN.host
        # params['port'] = 5124 #settings.JINA_REMOTE_FLOW_LINKEDIN.port


    # if flow is local control it manually
    if not host:
        flow.start()
    # try:
    client = Client(**params)
    while not client._is_flow_ready():
        sleep(1)
    # 1 step - search in google, facebook and instagram
    async for resp in client.post(
            on='/search',
            inputs=search_docs,
            target_executor='Search*',
            parameters={
                'source': ["grayfox"],
                'resource': "vetric",
                'SearchSERP__pages': 2,
                # backward compatibility params
                'flow_step': 'search',
                'primary_candidate_sources': COMMON_PRIMARY_CANDIDATE_SOURCES
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


async def create_enrich_doc(doc, search_id):
    candidate = await CandidateModel.get(uuid.UUID(doc.id))
    if candidate:
        candidate_dict = dotty(candidate.model_dump())
        source_id_key = f'network_signature.user_id.{candidate.source}_user_id'
        username_key = (f'network_signature.username.{candidate.source}'
                        '_username')
        profile_url_key = (f'network_signature.url.{candidate.source}'
                           '_profile_url')

        source_id = candidate_dict.get(source_id_key)
        username = candidate_dict.get(username_key)
        profile_url = candidate_dict.get(profile_url_key)

        if source_id:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                source_id=source_id,
                source=candidate.source
            )
        elif profile_url:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                profile_url=str(profile_url),
                source=candidate.source
            )
        elif username:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                username=username,
                source=candidate.source
            )
    return None
