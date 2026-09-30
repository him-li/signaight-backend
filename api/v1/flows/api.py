from typing import Dict
from core.utils.get_names_list import name_resolution
from fastapi import (
    APIRouter,
    status as http_status,
    Depends,
    BackgroundTasks,
)
from core.models.event import SearchEventModel, Status
from core.models.search_state import SearchStatus
from core.utils.base import transform_user_info
import asyncio
from datetime import datetime

from api.auth import auth, fief, FiefUserInfo, FiefAccessTokenInfo
from api.v1.persons.dependencies import get_persons_crud, PersonsCRUD
from core.logging import logger
from core.models import Person, PersonModel
from core.config import settings
from core.models.candidate import CandidateModel
from core.providers import build_fixture_candidates
from core.utils import (
    build_source_ids_dict,
    build_usernames_dict,
    build_profile_urls_dict,
)
from tasks.app import run_complex_search_flow, send_notification


# NOTE: new way to run flows from core.flows package
from core.flows import (
    facebook_enrich_flow,
    instagram_enrich_flow,
    complex_search_flow,
    twitter_enrich_flow,
    linkedin_enrich_flow,
    xing_enrich_flow,
)


from api.socketio import socket_manager
from core.socketio import MessageBuilder

router = APIRouter()


# NOTE: probably deprecated
@router.post("", status_code=http_status.HTTP_202_ACCEPTED, deprecated=True)
async def search_persons(
    request_body: Dict,
    background_tasks: BackgroundTasks,
    persons_crud: PersonsCRUD = Depends(get_persons_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await fief.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")

    selected_persons = request_body.get("selected_persons")

    if not settings.EXTERNAL_PROVIDERS_ENABLED:
        created = 0
        for person_id in selected_persons or []:
            person = await persons_crud.read(person_id)
            existing = await CandidateModel.find(
                CandidateModel.person.id == person.id,
                CandidateModel.resource == "fixture",
            ).count()
            if existing:
                continue
            for data in build_fixture_candidates(person, str(person.id)):
                await CandidateModel(person=person, **data).insert()
                created += 1
            message = MessageBuilder.person_message(person.id, "updated")
            await socket_manager.send_message_by_user_id(user_id, message)
        return {"message": "Offline candidate search completed",
                "provider": "fixture", "candidates_created": created}

    # inject demo data and return demo status if data was really demo
    demo_flow = False
    for person_id in selected_persons:
        demo_flow = await demo_data_check_update(person_id, persons_crud)

    if demo_flow is True:
        message = MessageBuilder.person_message(person_id, "updated")
        await socket_manager.send_message_by_user_id(user_id, message)

    if demo_flow is False:
        print("linkedin flow")
        background_tasks.add_task(
            asyncio.get_event_loop().create_task,
            make_search(
                persons_crud,
                selected_persons,
                user_id,
            ),
        )

    return {"message": "Search initiated"}


@router.post("/enrich", status_code=http_status.HTTP_202_ACCEPTED)
async def enrich_persons(
    request_body: Dict,
    background_tasks: BackgroundTasks,
    persons_crud: PersonsCRUD = Depends(get_persons_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user_info: FiefUserInfo = Depends(auth.current_user()),
):
    if not settings.EXTERNAL_PROVIDERS_ENABLED:
        return {"message": "External providers are disabled; no enrichment was started"}
    user_info = transform_user_info(user_info)
    selected_persons = request_body.get("selected_persons")

    for person in selected_persons:
        person_info = await persons_crud.read(person)
        if person_info.search_state.status != SearchStatus.in_progress:
            background_tasks.add_task(
                asyncio.get_event_loop().create_task,
                call_enrich(person_info, user_info, persons_crud),
            )

    return {"message": "Enrich initiated"}


async def make_search(
    persons_crud,
    selected_persons,
    user_id,
):
    for person in selected_persons:
        person_info = await persons_crud.read(person)
        if settings.JINA_REMOTE_FLOW_LINKEDIN:
            await run_complex_search_flow.kiq([str(person_info.id)], str(user_id))
        else:
            await complex_search_flow([person_info.id], user_id)


async def call_enrich(person: Person, userinfo, persons_crud):
    if not person.network_signature:
        return
    try:
        source_ids = build_source_ids_dict(person)
        usernames = build_usernames_dict(person)
        profile_urls = build_profile_urls_dict(person)
        host = (
            settings.JINA_REMOTE_FLOW_LINKEDIN
            if settings.JINA_REMOTE_FLOW_LINKEDIN
            else None
        )
        search = None
        if (source_ids) or (profile_urls):
            search = SearchEventModel(
                **{
                    "user_id": userinfo["id"],
                    "flows_list": [],
                    "persons_list": [person.id],
                    "retries": 0,
                }
            )
            print("facebook before started")
            now = datetime.now()
            search.updated_at = now
            search.status = Status.started
            await search.insert()
            try:
                person.last_update = datetime.now()
                person.last_edited_by = userinfo
                person.search_state.is_done = False
                person.search_state.status = "In progress"
                await person.replace()
            except Exception as err:
                print("error", err)
            send_notification(
                str(userinfo["id"]),
                MessageBuilder.search_message(search.id, "started"),
            )
        if source_ids.get("facebook"):
            await facebook_enrich_flow([person], host)

        if source_ids.get("instagram"):
            await instagram_enrich_flow([person], host)

        if source_ids.get("twitter") or usernames.get("twitter"):
            await twitter_enrich_flow([person])

        if profile_urls.get("linkedin"):
            await linkedin_enrich_flow([person], host)

        if profile_urls.get("xing"):
            await xing_enrich_flow([person], host)
        if (source_ids) or (profile_urls):
            now = datetime.now()
            if search:
                search_duration = now - search.created_at
                search.updated_at = now
                search.status = Status.done
                search.percent_completed = 100
                search.duration = search_duration
                await search.replace()
            person = await persons_crud.read(person.id)
            person.last_update = datetime.now()
            person.last_edited_by = userinfo
            person.search_state.is_done = True
            person.search_state.status = "Success"
            person_f_name = None
            person_l_name = None
            person_full_name = None
            normalized_person_name = await name_resolution(person.model_dump())
            parts = normalized_person_name.strip().split() if normalized_person_name else []

            if len(parts) == 2:
                person_f_name = parts[0]
                person_l_name = parts[1]
            if len(parts) > 2:
                person_f_name = parts[0]
                person_l_name = " ".join(parts[1:])
            person_full_name = normalized_person_name
            if not person.personal_details:
                person.personal_details = {}

            if not person.personal_details.name:
                person.personal_details.name = {}

            name = person.personal_details.name

            if not getattr(name, "full_name", None):
                name.full_name = {}

            if not getattr(name, "first_name", None):
                name.first_name = {}

            if not getattr(name, "last_name", None):
                name.last_name = {}

            if person_full_name:
                name.full_name.full_name = person_full_name

            if person_f_name:
                name.first_name.f_name = person_f_name

            if person_l_name:
                name.last_name.l_name = person_l_name
            await person.replace()
            send_notification(
                str(userinfo["id"]),
                MessageBuilder.search_message(search.id, "finished"),
            )
    except Exception as e:
        logger.info(e)
        return


async def demo_data_check_update(person_id, persons_crud: PersonsCRUD):
    demo_data = False
    demo_target = await persons_crud.read(person_id)
    try:
        demo_source = await persons_crud.read_demo_data(
            demo_target.personal_details.name.first_name.f_name.strip(),
            demo_target.personal_details.name.last_name.l_name.strip(),
        )
    except Exception:
        demo_source = None

    if demo_source:
        demo_data = True
        demo_data_dict = demo_source.model_dump()
        # relations cleanup
        demo_data_dict.pop("_id", None)
        demo_data_dict.pop("id", None)
        demo_data_dict.pop("project", None)
        # switch data from demo to false
        demo_target_dict = demo_target.model_dump()
        new_person_data = {**demo_target_dict, **demo_data_dict}
        new_person_data["demo_data"] = False
        now_time = datetime.now()
        new_person_data["last_update"] = now_time

        update_person = PersonModel(**new_person_data)
        await persons_crud.update(demo_target.id, update_person)
    return demo_data
