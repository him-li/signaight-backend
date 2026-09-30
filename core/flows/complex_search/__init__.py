import uuid
from docarray import DocList
from typing import List

from core.models import PersonModel, CandidateModel, SearchEventModel
from core.clients.ds_app import api as ds_app_api
from core.documents import (
    SearchRequestDoc,
    EnrichRequestDoc,
)
from core.utils import build_urn, build_person_urn, clean_person_name
from core.config import settings

from .linkedin_client import linkedin_client_run
from .email_client import email_client_run
from .phone_client import phone_client_run
from .utils import (get_person_city,
                    get_person_education,
                    get_person_work,
                    )


async def complex_search_flow(
    persons: List[uuid.UUID],
    search_id: uuid.UUID,
):
    linkedin_search_docs = DocList()
    email_search_docs = DocList()
    phone_search_docs = DocList()
    enrich_docs = DocList()
    for person_id in persons:
        person = await PersonModel.get(person_id)
        person_urn = build_urn("persons", str(person.id))
        # TODO: maybe use utils function core.build_search_docarray
        search_doc = SearchRequestDoc(
            urn=person_urn,
            search_id=str(search_id),
            # TODO: resource in doc deprecated value and should removed soon
            resource='vetric',
        )
        try:
            linkedin_url = person.network_signature.url.linkedin_profile_url[0]
        except Exception:
            linkedin_url = None
        try:
            search_doc.name = clean_person_name(
                person.personal_details.name.full_name.full_name)
            search_doc.f_name = clean_person_name(
                person.personal_details.name.first_name.f_name)
            search_doc.l_name = clean_person_name(
                person.personal_details.name.last_name.l_name)
        except Exception:
            pass
        try:
            if search_doc.name:
                res = ds_app_api.ds_request.common_name(
                    body={"full_name": search_doc.name},
                    headers={
                        'x-remote-context': search_doc.urn
                    }
                )
                if res.body.get("common_name"):
                    search_doc.is_rare_name = False
        except Exception:
            pass
        try:
            search_doc.city = get_person_city(person)
        except Exception:
            pass
        try:
            search_doc.email_address = (person.personal_details
                                        .email.email_address[0])
        except Exception:
            pass
        try:
            search_doc.phone_number = (person.personal_details
                                       .phone.phones[0])
        except Exception:
            pass
        try:
            search_doc.work = get_person_work(person)
        except Exception:
            pass
        try:
            search_doc.education = get_person_education(person)
        except Exception:
            pass
        try:
            if any(person.network_signature.username.model_dump().values()):
                search_doc.username = next(iter(
                    person.network_signature.username.model_dump().values()))
        except Exception:
            pass
        try:
            if any(person.biographic_details.description_bio_intro.
                   model_dump().values()):
                search_doc.bio = next(iter(
                    person.biographic_details.description_bio_intro.
                    model_dump().values()))
        except Exception:
            pass
        if linkedin_url:
            linkedin_search_docs.append(search_doc)
        elif search_doc.email_address:
            email_search_docs.append(search_doc)
        elif search_doc.phone_number:
            phone_search_docs.append(search_doc)
        if linkedin_url:
            enrich_docs.append(EnrichRequestDoc(
                urn=person_urn,
                search_id=str(search_id),
                # NOTE: pydantic v2 Url object could not be turned into string
                # automatically and raise protobuf error
                profile_url=str(linkedin_url)
            ))
    host = (settings.JINA_REMOTE_FLOW_LINKEDIN
            if settings.JINA_REMOTE_FLOW_LINKEDIN else None)
    if linkedin_search_docs:
        return await linkedin_client_run(
            search_id,
            persons,
            linkedin_search_docs,
            enrich_docs,
            host=host
        )
    if email_search_docs:
        return await email_client_run(
            search_id,
            persons,
            email_search_docs,
            enrich_docs,
            host=host,
        )
    if phone_search_docs:
        return await phone_client_run(
            search_id,
            persons,
            phone_search_docs,
            enrich_docs,
            host=host
        )
