import asyncio
import uuid
from datetime import datetime
from mergedeep import merge, Strategy
from glom import glom
from fastapi import (
    APIRouter,
    Response,
    Depends,
    status as http_status,
    Request,
    BackgroundTasks,
    HTTPException,
)
from fastapi_filter import FilterDepends

from api.auth import FiefAccessTokenInfo, auth, fief
from api.pagination import Page, Params
from api.socketio import socket_manager
from api.v1.events.search.dependencies import SearchCRUD, get_search_crud

from core.config import settings
from core.models import CandidateModel
from core.providers import build_fixture_candidates
from core.flows import aggregation_flow
from core.flows.facebook_enrich import facebook_enrich_flow
from core.flows.instagram_enrich import instagram_enrich_flow
from core.flows.twitter_enrich import twitter_enrich_flow
from core.flows.xing_enrich import xing_enrich_flow
from core.flows.interpol_enrich import interpol_enrich_flow
from core.flows.linkedin_enrich import linkedin_enrich_flow
from core.socketio import MessageBuilder
from core.utils import extract_profile_source
from core.clients.vetric.linkedin.mapping_specs import VtLISpecs
from core.clients.vetric.instagram import (api as instagram_api, VtrcIgSpecs)
from core.documents.base import EnrichRequestDoc
from core.utils.instagram_username import extract_instagram_username
from core.utils.urn import build_urn
from core.clients.vetric.linkedin import (api as linkedin_api, VtLISpecs)
from services.FacebookAPI.executor.vtrc_facebook import enrich_timeline
from core.clients.vetric.facebook import api, VtrcFbSpecs
from services.InstagramAPI.executor.vtrc_instagram.vtrc_executor import VetricInstagramAPI
from services.LinkedinAPI.executor.vtrc_linkedin.vtrc_executor import VetricLinkedinAPI
from services.LinkedinAPI.executor.vtrc_linkedin.vtrc_executor import VetricLinkedinAPI

from ..crud import PersonModel
from .filters import CandidateFilter
from .dependencies import CandidatesCRUD, get_candidates_crud
from .schemas import CandidateListRead, CandidateCreate, CandidateRead, CandidateUpdate


router = APIRouter()


@router.get(
    "/",
    response_model=Page[CandidateListRead],
    status_code=http_status.HTTP_200_OK,
)
async def get_candidates(
    person_id: uuid.UUID,
    params: Params = Depends(),
    filter: CandidateFilter = FilterDepends(CandidateFilter),
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[CandidateListRead]:
    # filter.person__id = request.path_params.get("person_id")
    # NOTE: filter require id as string for now

    if not settings.EXTERNAL_PROVIDERS_ENABLED:
        person = await candidates._person(person_id)
        existing_fixture_candidates = await CandidateModel.find(
            CandidateModel.person.id == person.id,
            CandidateModel.resource == "fixture",
        ).count()
        if not existing_fixture_candidates:
            for data in build_fixture_candidates(person, str(person.id)):
                await CandidateModel(person=person, **data).insert()
        filter.ds_filter = None
    candidates_list = await candidates.read_list(person_id, params, filter)
    if not candidates_list.items:
        filter.ds_filter = None
        candidates_list = await candidates.read_list(person_id, params, filter)

    return candidates_list


@router.get(
    "/{candidate_id}",
    response_model=CandidateRead,
    status_code=http_status.HTTP_200_OK,
)
async def get_candidate(
    person_id: uuid.UUID,
    candidate_id: uuid.UUID,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    return await candidates.read(person_id, candidate_id)


@router.post(
    "/",
    response_model=CandidateRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_candidate(
    person_id: uuid.UUID,
    candidate: CandidateCreate,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    if not candidate.search_id:
        candidate.search_id = str(person_id)
    if not candidate.searched_at:
        candidate.searched_at = datetime.now()
    if not candidate.source:
        candidate.source = extract_profile_source(candidate.model_dump())
    candidate_data = candidate.model_dump()
    if candidate.network_signature:
        match candidate.source:
            case "facebook":
                source_id = (
                    candidate.network_signature.user_id.facebook_user_id[0]
                    if candidate.network_signature.user_id
                    and candidate.network_signature.user_id.facebook_user_id
                    else None
                )
                if not source_id:
                    url = (
                        candidate.network_signature.url.facebook_profile_url[0]
                        if candidate.network_signature.url
                        and candidate.network_signature.url.facebook_profile_url
                        else None
                    )
                    res = await api.async_general.resolve_url(params={"url": str(url)})

                    res_body = res.body
                    spec = VtrcFbSpecs.url_resolver_spec
                    mapped = glom(res_body, spec, default={})

                    source_id = mapped.get("id")

                cand_data = await enrich_timeline.enrich_timeline(source_id)
                candidate_data = {**candidate_data, **cand_data}
            case "instagram":
                source_id = (
                    candidate.network_signature.user_id.instagram_user_id[0]
                    if candidate.network_signature.user_id
                    and candidate.network_signature.user_id.instagram_user_id
                    else None
                )
                if not source_id:
                    url = (
                        candidate.network_signature.url.instagram_profile_url[0]
                        if candidate.network_signature.url
                        and candidate.network_signature.url.instagram_profile_url
                        else None
                    )
                    username_from_url = extract_instagram_username(str(url))
                    if not username_from_url:
                        return

                    res = await instagram_api.async_user.usernameinfo(username_from_url)
                    res_body = res.body
                    spec = VtrcIgSpecs.usernameinfo_spec
                    mapped = glom(res_body, spec, default={})
                    source_id = mapped.get("user_id")
                vetric_api = VetricInstagramAPI()
                doc = EnrichRequestDoc(
                    source_id=source_id,
                    urn=build_urn("persons", str(person_id)),
                    resource="vetric",
                    source="instagram",
                )
                cand_data = await vetric_api._enrich_info(doc)
                candidate_data = merge(candidate_data, cand_data, strategy=Strategy.ADDITIVE)
            case "linkedin":
                source_id = (
                    candidate.network_signature.user_id.linkedin_user_id[0]
                    if candidate.network_signature.user_id
                    and candidate.network_signature.user_id.linkedin_user_id
                    else None
                )
                if not source_id:
                    url = (
                        candidate.network_signature.url.linkedin_profile_url[0]
                        if candidate.network_signature.url
                        and candidate.network_signature.url.linkedin_profile_url
                        else None
                    )
                    try:
                        params = {"url": url}
                        response = await linkedin_api.async_profile.resolve_url(params=params)
                        response_body = response.body
                        spec = VtLISpecs.url_resolver_spec
                        source_id = glom(response_body, spec)
                    except Exception as e:
                        print(str(e))
                        return

                    
                vetric_api = VetricLinkedinAPI()
                doc = EnrichRequestDoc(
                    source_id=source_id,
                    urn=build_urn("persons", str(person_id)),
                    resource="vetric",
                    source="linkedin",
                    profile_url=str(url) if url else None,
                )
                cand_data = await vetric_api._enrich_overview(doc)
                candidate_data = merge(candidate_data, cand_data, strategy=Strategy.ADDITIVE)
            case _:
                pass

    return await candidates.create(person_id, candidate_data)


@router.put(
    "/{candidate_id}",
    response_model=CandidateRead,
    response_description="Review record updated",
)
async def update_candidate(
    person_id: uuid.UUID,
    candidate_id: uuid.UUID,
    candidate: CandidateUpdate,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    return await candidates.update(person_id, candidate_id, candidate.model_dump())


@router.put(
    "/{candidate_id}/primary",
    # response_model=CandidateRead,
    response_class=Response,
    response_description="Review record updated",
)
async def update_primary_candidate(
    person_id: uuid.UUID | str,
    candidate_id: uuid.UUID | str,
    request: Request,
    background_tasks: BackgroundTasks,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    searches_crud: SearchCRUD = Depends(get_search_crud),
) -> CandidateRead:
    # person_id = request.path_params.get("person_id")
    search_id = request.query_params.get("search_id")

    user_info = await fief.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")

    person = await PersonModel.get((uuid.UUID(person_id)
                                    if isinstance(person_id, str) else
                                    person_id))
    if not person:
        raise HTTPException(
            status_code=500,
            detail="Candidate have no proper person"
        )
    # TODO: check what I removed here
    # if not isinstance(candidate_id, uuid.UUID):
    #     matched_profiles = (
    #         person.network_signature.matched_profiles.model_dump())

    #     matched_profiles[candidate_id] = {**matched_profiles.get(candidate_id),
    #                                       'primary_candidate': "no-primary"}
    #     person.network_signature.matched_profiles = matched_profiles
    #     await person.save_changes()

    #     return Response(status_code=200)

    candidate = await candidates.read(person_id, candidate_id)
    # TODO: frontend pushes wrong candidate id in request.
    # It raise error in flow!!!
    if not person.id == candidate.person.id:
        raise HTTPException(
            status_code=402,
            detail="Candidate and person missmatch"
        )
    source = candidate.source
    resource = candidate.resource

    if not settings.EXTERNAL_PROVIDERS_ENABLED:
        from core.models import NetworkSignature
        from core.models.matched_profiles import (
            MatchedProfiles, SourceInfo, PrimaryCandidateInfo)
        if not person.network_signature:
            person.network_signature = NetworkSignature()
        if not person.network_signature.matched_profiles:
            person.network_signature.matched_profiles = MatchedProfiles()
        same_source = await candidates.read_all_by_source_resource(
            person_id, source, resource)
        for previous in await same_source.to_list():
            if previous.id != candidate.id and previous.primary:
                await candidates.update(person_id, previous.id, {"primary": False})
        await candidates.update(person_id, candidate_id,
                                {"primary": True, "ds_filter": True})
        network = candidate.network_signature
        candidate_url = getattr(network.url, f"{source}_profile_url", None) if network and network.url else None
        candidate_username = getattr(network.username, f"{source}_username", None) if network and network.username else None
        candidate_name = candidate.personal_details.name if candidate.personal_details else None
        full_name = getattr(candidate_name.full_name, f"{source}_full_name", None) if candidate_name and candidate_name.full_name else None
        profile = PrimaryCandidateInfo(
            full_name=full_name, profile_url=candidate_url,
            profile_username=candidate_username[0] if candidate_username else None)
        setattr(person.network_signature.matched_profiles, source,
                SourceInfo(primary_candidate={str(candidate.id): profile},
                           candidates_count=await same_source.count()))
        person.last_update = datetime.now()
        await person.replace()
        return Response(status_code=200)

    # prior_primary_candidates = await candidates.read_primary(
    #     person_id, source, resource, search_id
    # )
    # primary_list = await prior_primary_candidates.to_list()

    # for primary_candidate in primary_list:
    #     await candidates.update(person_id, primary_candidate.id, {"primary": False})

    search_data = {
        "user_id": user_id,
        "flows_list": [{
            "Vetric_instagram": ["instagram", "vetric"],
            "Vetric_facebook": ["facebook", "vetric"],
            "Vetric_twitter": ["twitter", "vetric"]}],
        "persons_list": [person_id],
        "retries": 0,
    }

    search = await searches_crud.create(search_data)
    search_id_uuid = search.id
    search_created_at = search.created_at


    await candidates.update(person_id, candidate_id, {"primary": True, "ds_filter": True})
    background_tasks.add_task(
        asyncio.get_event_loop().create_task,
        make_enrich_aggregate(
            access_token_info,
            person_id,
            source,
            resource,
            search_id_uuid,
            search_created_at,
            searches_crud,
            candidate_id),
    )

    return Response(status_code=200)


@router.delete(
    "/{candidate_id}",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT,
)
async def delete_candidate(
    person_id: uuid.UUID,
    candidate_id: uuid.UUID,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    await candidates.delete(person_id, candidate_id)


async def make_enrich_aggregate(access_token_info,
                                person_id,
                                source,
                                resource,
                                search_id_uuid,
                                search_created_at,
                                searches_crud,
                                candidate_id):
    person = await PersonModel.get(person_id)
    try:
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        host = (settings.JINA_REMOTE_FLOW_LINKEDIN
                if settings.JINA_REMOTE_FLOW_LINKEDIN else None)   
        message = MessageBuilder.person_message(person_id, "updated")
        await socket_manager.send_message_by_user_id(user_id, message)
        now = datetime.now()
        search_update = {
            "updated_at": now,
            "status": "Started",
        }
        await searches_crud.update(search_id_uuid, search_update)
        await aggregation_flow(person_id, candidate_id, host)

       
        if resource != 'epieos':

            match source:
                case 'facebook':
                    await facebook_enrich_flow([person], host)
                case 'instagram':
                    await instagram_enrich_flow([person], host)
                case 'twitter':
                    await twitter_enrich_flow([person])
                case 'xing':
                    await xing_enrich_flow([person], host)
                case 'interpol':
                    await interpol_enrich_flow([person], host)
                case 'linkedin':
                    await linkedin_enrich_flow([person], host)
                case _:
                    pass

        now = datetime.now()
        search_duration = now - search_created_at
        search_update = {
            "status": "Done",
            "percent_completed": 100,
            "duration": search_duration,
            "updated_at": now
        }

        await searches_crud.update(search_id_uuid, search_update)

        message = MessageBuilder.person_message(person_id, "updated")
        await socket_manager.send_message_by_user_id(user_id, message)
    except Exception as e:
        print('Error in enrich aggregate flow:', e)
        now = datetime.now()
        search_duration = now - search_created_at
        search_update = {
            "status": "Error",
            "percent_completed": 100,
            "duration": search_duration,
            "updated_at": now,
        }
        await searches_crud.update(search_id_uuid, search_update)
        person = await PersonModel.get(person_id)
        person.search_state.is_done = True
        person.search_state.status = "Success"
        await person.save_changes()
        message = MessageBuilder.person_message(person_id, "updated")
        await socket_manager.send_message_by_user_id(user_id, message)
