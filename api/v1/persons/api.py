import asyncio
import csv
import uuid
import pandas
from beanie.operators import In
from io import StringIO
from typing import Dict, List, Union
from core.models.merge_metadata import MergeMetadata, MergeStrategy, MergedBy
from core.models.utils.update_connection_graph import GraphBuilder, build_dynamic_view, nx_to_cytoscape, rewrite_relationships
from core.utils.get_person_display_name import get_person_display_name
from core.utils.merge_persons.merge_auto_collections import merge_auto_collections
from fastapi import (
    APIRouter,
    Query,
    Response,
    Depends,
    status as http_status,
    Request,
    HTTPException,
    BackgroundTasks,
)
from fastapi.responses import StreamingResponse
from fastapi_filter import FilterDepends
from flatten_json import flatten

from api.v1.projects.dependencies import ProjectsCRUD, get_projects_crud
from api.auth import AccessTokenInfo, auth, user_directory, UserInfo
from api.pagination import Page, Params
from api.socketio import socket_manager
from api.v1.events.search.dependencies import get_search_crud, SearchCRUD

from core.dotty_dictionary import Dotty
from core.logging import logger
from core.models import (
    PersonModelAuditLog, ActiveSearchEventModel, PersonModel, WebSearchModel)
from core.models.comment import Comment
from core.models.person import Person, RecruitingSource
from core.socketio import MessageBuilder
from core.utils import transform_user_info
from tasks.app import recalculate_person_score

from .candidates.api import router as candidates_router
from .candidates.dependencies import get_candidates_crud, CandidatesCRUD
from .filters import (PersonHistoryFilter, PersonsFilterByProject,
                      PersonsFilter, PersonsExportFilter)
from .dependencies import PersonsCRUD, get_persons_crud
from .schemas import (
    GraphConnection,
    GraphResponse,
    MergeRequest,
    MergeResponse,
    PersonFieldPatch,
    PersonListRead,
    PersonRead,
    PersonCreate,
    PersonUpdate,
    PersonIdsSchema,
    PersonDeleteBatch,
    ConnectionCreate
)
from api.v1.projects.schemas import PersonRankingView
from api.v1.projects.api import (
    get_leaderboard_info,
    get_leaderboard_widgets,
    get_person_basic_data,
    get_person_ranking_data,
    refresh_all_persons_search as origin_refresh_all_persons_search)

from api.v1.flags.filters import FlagFilter
from api.v1.flags.dependencies import FlagsCRUD, get_flags_crud
from api.v1.flags.schemas import FlagRead


router = APIRouter()


def _inline_refs(obj: any, defs: dict, seen: set | None = None) -> any:
    """Recursively replace all $ref pointers with their inlined definitions."""
    if seen is None:
        seen = set()

    if isinstance(obj, dict):
        if "$ref" in obj:
            ref_name = obj["$ref"].replace("#/$defs/", "")
            if ref_name in seen:
                return {"type": "object", "description": f"(circular ref: {ref_name})"}
            seen = seen | {ref_name}
            resolved = _inline_refs(defs.get(ref_name, {}), defs, seen)
            extras = {k: v for k, v in obj.items() if k != "$ref"}
            return {**resolved, **extras} if extras else resolved

        return {
            k: _inline_refs(v, defs, seen)
            for k, v in obj.items()
            if k != "$defs"
        }

    if isinstance(obj, list):
        return [_inline_refs(item, defs, seen) for item in obj]

    return obj


def _strip_nullable(obj: any) -> any:
    """Remove null variants from anyOf and simplify where possible."""
    if isinstance(obj, dict):
        if "anyOf" in obj:
            siblings = {k: _strip_nullable(v) for k, v in obj.items() if k != "anyOf"}
            non_null = [s for s in obj["anyOf"] if s.get("type") != "null"]

            if len(non_null) == 0:
                return {**siblings, "type": "null"}

            if len(non_null) == 1:
                return _strip_nullable({**non_null[0], **siblings})

            types = {s.get("type") for s in non_null}
            if len(types) == 1:
                return _strip_nullable({**non_null[0], **siblings})

            return {**siblings, "anyOf": [_strip_nullable(s) for s in non_null]}

        return {k: _strip_nullable(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_strip_nullable(item) for item in obj]

    return obj


@router.get(
    "/schema",
    response_model=None,
    status_code=http_status.HTTP_200_OK,
    summary="Get Person JSON Schema",
    description="Returns the fully-inlined JSON Schema for the Person model (all $ref resolved).",
)
async def get_person_schema() -> dict:
    schema = PersonRead.model_json_schema(by_alias=False)
    defs = schema.get("$defs", {})
    inlined = _inline_refs(schema, defs)
    return _strip_nullable(inlined)


@router.get(
    "",
    response_model=Page[PersonListRead],
    status_code=http_status.HTTP_200_OK
)
async def get_persons(
    params: Params = Depends(),
    filter: PersonsFilter = FilterDepends(PersonsFilter),
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> Page[PersonListRead]:
    return await persons.list(params, filter)


@router.post(
    "/export",
    response_class=Response,
    status_code=http_status.HTTP_200_OK
)
async def get_persons_export(
    data: PersonIdsSchema,
    filter: PersonsExportFilter = FilterDepends(PersonsExportFilter),
    persons: PersonsCRUD = Depends(get_persons_crud),
):
    data = await persons.export(filter, data.model_dump())
    items = []
    for item in data:
        item = flatten(item.model_dump(mode='json'), '.')
        items.append([
            item.get('personal_details.name.full_name.full_name'),
            item.get('personal_details.email.email_address.0'),
            item.get('signaight_score'),
            item.get('compatibility'),
        ])
    sheet = pandas.DataFrame(
        items,
        columns=["Full Name", "Email", "SignAIght Score", "Compatibility"]
    )
    return StreamingResponse(
        iter([sheet.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)]),
        media_type="text/csv",
        headers={f"Content-Disposition": f"attachment; filename=project_report.csv"}
    )


@router.get(
    "/by-project/{id}",
    response_model=Page[PersonListRead],
    status_code=http_status.HTTP_200_OK,
    deprecated=True
)
async def get_persons_by_project_id(
    id: uuid.UUID | str,
    params: Params = Depends(),
    filter: PersonsFilter = FilterDepends(PersonsFilterByProject),
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> Page[PersonListRead]:
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
      /persons
    '''
    # WARNING: with big qty of project could produce high load.
    # TODO: investigate how it is possible to filter data via linked
    # model fields
    filter.project__id = id
    return await get_persons(params, filter, persons)


@router.get(
    "/by-project/{id}/leaderboard-info",
    status_code=http_status.HTTP_200_OK,
    deprecated=True
)
async def get_leaderboard_info_by_project_id(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
      /projects/{id}/leaderboard-info
    '''
    return await get_leaderboard_info(id, projects, access_token_info)


@router.get(
    "/by-project/{id}/leaderboard-widgets",
    status_code=http_status.HTTP_200_OK,
    deprecated=True
)
async def get_leaderboard_widgets_by_project_id(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
      /projects/{id}/leaderboard-widgets
    '''
    return await get_leaderboard_widgets(id, projects, access_token_info)


@router.get(
    "/by-project/{id}/basic-info",
    status_code=http_status.HTTP_200_OK,
    response_model=List[PersonRead],
    response_model_exclude_none=True,
    deprecated=True
)
async def get_person_basic_data_by_project_id(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
      /projects/{id}/basic-info
    '''
    return await get_person_basic_data(id, projects, access_token_info)


@router.get(
    "/by-project/{id}/ranking",
    status_code=http_status.HTTP_200_OK,
    response_model=List[PersonRankingView],
    response_model_exclude_none=True,
    deprecated=True
)
async def get_person_ranking_data_by_project_id(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
    /projects/{id}/ranking
    '''
    return await get_person_ranking_data(id, projects, access_token_info)


@router.get(
    "/by-project/{id}/refresh-all",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT,
    deprecated=True
)
async def refresh_all_persons_search(
    id: uuid.UUID,
    background_tasks: BackgroundTasks,
    persons: PersonsCRUD = Depends(get_persons_crud),
    candidates_crud: CandidatesCRUD = Depends(get_candidates_crud),
    searches_crud: SearchCRUD = Depends(get_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
    user_info: UserInfo = Depends(auth.current_user()),
):
    '''
    Path is deprecated, should be removed soon. Requests should be directed to
     /projects/{id}/refresh-all
    '''
    await origin_refresh_all_persons_search(id,
                                            background_tasks,
                                            persons,
                                            candidates_crud,
                                            searches_crud,
                                            access_token_info,
                                            user_info)


@router.get("/{id}",
            response_model=PersonRead,
            status_code=http_status.HTTP_200_OK)
async def get_person(
    id: uuid.UUID,
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> PersonRead:
    return await persons.read(id)


@router.get(
    "/{id}/history",
    response_model=Page[PersonModelAuditLog],
    status_code=http_status.HTTP_200_OK,
)
async def get_person_history(
    id: uuid.UUID,
    params: Params = Depends(),
    filter: PersonHistoryFilter = FilterDepends(PersonHistoryFilter),
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> Page[PersonModelAuditLog]:
    return await persons.read_history(params, id, filter)


@router.get(
    "/{id}/web_search",
    response_model=List[WebSearchModel],
    status_code=http_status.HTTP_200_OK,
)
async def get_web_search_by_person(
    id: uuid.UUID | str,
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> List[WebSearchModel]:
    web_searches = await persons.get_web_search_by_person_id(id)
    return web_searches


@router.post(
    "",
    response_model=PersonRead,
    status_code=http_status.HTTP_201_CREATED
)
async def add_person(
    person_create: PersonCreate,
    background_tasks: BackgroundTasks,
    project_id: uuid.UUID,
    search_existing: bool = True,
    persons: PersonsCRUD = Depends(get_persons_crud),
    candidates_crud: CandidatesCRUD = Depends(get_candidates_crud),
    searches_crud: SearchCRUD = Depends(get_search_crud),
) -> PersonRead:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    person_create.project_id = project_id
    person_create.search_existing = search_existing
    person = await persons.create(person_create, user_info)
    # demo_data = await demo_data_check(person.id, persons)
    message = MessageBuilder.person_message(person.id, "added")
    await socket_manager.send_message_by_user_id(user_id, message)
    return person


@router.post(
    "/by-csv",
    response_model=List[PersonRead],
    status_code=http_status.HTTP_201_CREATED
)
async def import_persons(
    request: Request,
    background_tasks: BackgroundTasks,
    project_id: uuid.UUID,
    search_existing: bool = True,
    candidates_crud: CandidatesCRUD = Depends(get_candidates_crud),
    searches_crud: SearchCRUD = Depends(get_search_crud),
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> List[PersonRead]:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    req_content_type = request.headers.get("content-type")
    if "multipart/form-data" not in req_content_type:
        raise HTTPException(
            http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            (
                f"Unsupported content type {req_content_type},"
                f" please upload a CSV file"
            ),
        )
    form_data = await request.form()
    if not form_data.get("csv"):
        raise HTTPException(
            http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            (
                f"Unsupported file type {upload_file.content_type},"
                f" please upload a CSV file"
            ),
        )
    upload_file = form_data.get("csv")
    if upload_file.content_type != "text/csv":
        raise HTTPException(
            http_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            (
                f"Unsupported file type {upload_file.content_type},"
                f" please upload a CSV file"
            ),
        )
    created_persons = []
    if upload_file.content_type == "text/csv":
        file_content = await upload_file.read()
        file_content = file_content.decode("utf-8-sig").encode("utf-8")
        persons_data = parse_csv(file_content)
        user_info = transform_user_info(user_info)
        user_id = user_info.get("id")
        for data in persons_data:
            data["project_id"] = project_id
            try:
                person_create = PersonCreate(**data,
                                             search_existing=search_existing)
                person = await persons.create(person_create,
                                              user_info,
                                              is_bulk=True)
            except Exception as e:
                logger.error(str(e))
                continue
            if not person:
                continue
            created_persons.append(person)
        message = MessageBuilder.person_message(None, "added", str(project_id))
        await socket_manager.send_message_by_user_id(user_id, message)
    return created_persons


@router.put(
    "/{id}",
    response_model=PersonRead,
    response_description="Review record updated"
)
async def update_person(
    id: uuid.UUID,
    person: PersonUpdate,
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> PersonRead:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    updated_person = await persons.update(id, person, user_info)
    message = MessageBuilder.person_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_id, message)
    return updated_person


@router.patch(
    "/{id}/comment", response_model=PersonRead,
    response_description="Review record updated"
)
async def patch_person_comment(
    id: uuid.UUID,
    comment: Comment,
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> PersonRead:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    comment = {**comment.model_dump(), "created_by": user_info}
    updated_person_comment = await persons.patch_comment(id,
                                                         comment,
                                                         user_info)
    message = MessageBuilder.person_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_id, message)
    return updated_person_comment


@router.patch(
    "/{id}/connections", response_model=PersonRead,
    response_description="Review record updated"
)
async def patch_person_connection(
    id: uuid.UUID,
    connection: ConnectionCreate,
    persons: PersonsCRUD = Depends(get_persons_crud),
) -> PersonRead:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    updated_person_connection = await persons.patch_connection(id,
                                                               connection,
                                                               user_info)
    message = MessageBuilder.person_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_info.get("id"), message)
    return updated_person_connection


@router.patch(
    "/{id}", response_model=PersonRead,
    response_description="Review record updated"
)
async def patch_person(
    id: uuid.UUID,
    person: PersonUpdate,
    persons: PersonsCRUD = Depends(get_persons_crud),
    operation: Union[str, None] = Query(default=None),
) -> PersonRead:
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    if operation is not None:
        patch = PersonFieldPatch(
            data=person.model_dump(exclude_unset=True),
            operation=operation,
        )
        updated_person = await persons.patch_fields(id, patch, user_info)
    else:
        updated_person = await persons.patch(id, person, user_info)
    message = MessageBuilder.person_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_id, message)
    return updated_person


@router.delete(
    "/{id}",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT
)
async def delete_person(
    id: uuid.UUID,
    persons: PersonsCRUD = Depends(get_persons_crud),
):
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    person = await persons.read(id)
    if person.recruiting_source == RecruitingSource.internet:
        if person.search_id:
            try:
                await remove_active_search_project_id(person)
            except Exception as e:
                print(str(e))
    await persons.delete(id)
    message = MessageBuilder.person_message(id, "deleted")
    await socket_manager.send_message_by_user_id(user_id, message)


@router.delete(
    "",
    response_model=None,
    status_code=http_status.HTTP_204_NO_CONTENT
)
async def delete_persons_banch(
    data: PersonDeleteBatch,
    persons: PersonsCRUD = Depends(get_persons_crud),
):
    principal = persons.get_principal()
    user_info = get_principal_user_info(principal)
    user_id = user_info.get("id")
    try:
        count = await persons.delete_many(data)
        message = MessageBuilder.persons_batch_delete_message(
            "succeeded", count)
        await socket_manager.send_message_by_user_id(user_id, message)
    except Exception:
        message = MessageBuilder.persons_batch_delete_message("failed")
        await socket_manager.send_message_by_user_id(user_id, message)


@router.post(
    "/graph",
    status_code=http_status.HTTP_200_OK,
    response_model=GraphResponse,
)
async def enrich_persons_test(
    request_body: GraphConnection
):
    persons = []
    if request_body.project_id:
        persons = await PersonModel.find(
            PersonModel.project.id == uuid.UUID(request_body.project_id)
        ).to_list()
    if request_body.selected_persons:
        persons = await PersonModel.find(
            In(PersonModel.id, [uuid.UUID(pid)
               for pid in request_body.selected_persons])
        ).to_list()
    builder = GraphBuilder()
    graph = builder.build(persons, from_database=False)
    updated_graph = build_dynamic_view(
        graph, node_types=request_body.node_types, edge_types=request_body.edge_types)
    bidirectional_graph = rewrite_relationships(
        updated_graph, connection_type=request_body.connection_type, min_degree=request_body.min_degree)
    result = nx_to_cytoscape(bidirectional_graph)
    return {"result": result}


@router.get(
    "/{id}/red-flags",
    response_model=Page[FlagRead],
    status_code=http_status.HTTP_200_OK,
    deprecated=True
)
async def get_person_red_flags(
    id: uuid.UUID | str,
    params: Params = Depends(),
    filter: FlagFilter = FilterDepends(FlagFilter),
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> Page[FlagRead]:
    return await flags.read_all_flags_by_person(params, filter, id)


router.include_router(
    candidates_router, prefix="/{person_id}/candidates", tags=["persons"]
)


def parse_csv(file_content: bytes) -> List[Dict[str, str]]:
    buffer = StringIO(file_content.decode())

    def ensure_phone_number_format(phone: str | None):
        phone = phone.strip() if phone else None
        if not phone:
            return None
        return [phone if phone.startswith("+") else f'+{phone}']

    # load CSV data into dataframe
    try:
        csv_data = pandas.read_csv(
            buffer,
            keep_default_na=False,
            converters={
                "Linkedin URL": lambda v: v.strip() if v else None,
                "Email": lambda v: [v.strip()] if v else None,
                "Phone": ensure_phone_number_format,
                "First Name": lambda v: v.strip() if v else None,
                "Last Name": lambda v: v.strip() if v else None,
            }
        )
    except Exception:
        raise HTTPException(
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Unsupported CSV schema. Uploaded fil is not in CSV format"
        )
    csv_data = csv_data.reset_index()
    # Check for required fields in dataframe
    for i, row in csv_data.iterrows():
        _row = row.to_dict()
        if (not _row.get("Linkedin URL") and not _row.get("Email")
                and not _row.get("Phone")):
            raise HTTPException(
                http_status.HTTP_422_UNPROCESSABLE_ENTITY,
                (
                    "Unsupported CSV schema. "
                    "Supported headers are: Linkedin URL, Email, Phone, "
                    "First Name, Last Name. "
                    "One column Linkedin URL, Email or Phone are mandatory "
                    "for all applicants"
                    "Uploaded file contains {} headers.".format(
                        ', '.join(list(csv_data)))
                ),
            )
    # rename fields with dotted schema by dataframe tools
    csv_data = csv_data.rename(
        columns={
            "Linkedin URL": "network_signature.url.linkedin_profile_url",
            "Email": "personal_details.email.email_address",
            "Phone": "personal_details.phone.phones",
            "First Name": "personal_details.name.first_name.f_name",
            "Last Name": "personal_details.name.last_name.l_name",
        }
    )
    # perform list of structured dicts from dataframe
    persons_data = []
    for i, row in csv_data.iterrows():
        pd = {k: v for k, v in row.to_dict().items()
              if v not in (None, '', [], {}, ())}
        pd = Dotty.from_flat_dict(pd)
        del pd['index']
        # assembly full name from first_name and last_name
        fn_chunks = []
        if f_name := pd.get("personal_details.name.first_name.f_name"):
            fn_chunks.append(f_name)
        if l_name := pd.get("personal_details.name.last_name.l_name"):
            fn_chunks.append(l_name)
        if len(fn_chunks) > 0:
            pd['personal_details.name.full_name.full_name'] = (" "
                                                               .join(fn_chunks).strip())
        persons_data.append(pd.to_dict())

    return persons_data


async def demo_data_check(person_id, persons_crud: PersonsCRUD):
    demo_data = False
    demo_target = await persons_crud.read(person_id)
    try:
        # NOTE: demo data check id based only on firstname and lastname!
        demo_source = await persons_crud.read_demo_data(
            demo_target.personal_details.name.first_name.f_name.strip(),
            demo_target.personal_details.name.last_name.l_name.strip(),
        )
        if demo_source:
            demo_data = True
            return demo_data
        else:
            return demo_data
    except Exception:
        return demo_data


async def update_active_search(person: PersonCreate):
    active_search = await ActiveSearchEventModel.get(person.search_id)
    candidates = active_search.search_results

    def to_list(value):
        if not value:
            return []
        return value if isinstance(value, list) else [value]

    person_urls = set(to_list(person.network_signature.url.linkedin_profile_url))

    candidate = [
        c for c in candidates
        if person_urls.intersection(
            set(to_list(c.network_signature.url.linkedin_profile_url))
        )
    ]

    if candidate:
        candidate = candidate[0]

        if isinstance(candidate.projects_list, list):
            if person.project.id not in candidate.projects_list:
                candidate.projects_list.append(person.project.id)
        else:
            candidate.projects_list = [person.project.id]

    await active_search.save()


async def remove_active_search_project_id(person: PersonModel):
    search_id = person.search_id
    project_id = person.project.id

    active_search = await ActiveSearchEventModel.get(search_id)
    candidates = active_search.search_results

    def to_list(value):
        if not value:
            return []
        return value if isinstance(value, list) else [value]

    person_urls = set(to_list(person.network_signature.url.linkedin_profile_url))

    candidate = [
        c for c in candidates
        if person_urls.intersection(
            set(to_list(c.network_signature.url.linkedin_profile_url))
        )
    ]

    if candidate:
        candidate = candidate[0]

        if isinstance(candidate.projects_list, list):
            candidate.projects_list = [
                pid for pid in candidate.projects_list
                if pid != project_id
            ]
        else:
            candidate.projects_list = []

    await active_search.save()


@router.post("/merge", response_model=MergeResponse)
async def merge_persons(
    req: MergeRequest,
    background_tasks: BackgroundTasks,
    persons: PersonsCRUD = Depends(get_persons_crud),
):
    try:
        project_id = req.project_id
        merged_person = req.merged_person
        principal = persons.get_principal()
        user_info = get_principal_user_info(principal)

        if len(req.person_ids) < 2:
            raise HTTPException(400, "At least two persons required")

        if req.merge_mode == "auto":
            merge_strategy = MergeStrategy(
                conflict_resolution="last_updated",
                merged_arrays="last_updated",
            )

        else:
            merge_strategy = MergeStrategy(
                conflict_resolution="manual",
            )

        merged_person.merge_metadata = MergeMetadata(
            merged_from_person_ids=req.person_ids,
            merge_mode=req.merge_mode,
            merged_by=MergedBy(
                user_id=user_info.get("id"),
                email=user_info.get("email"),
            ),
            merge_strategy=merge_strategy,
        )
        persons_init = await PersonModel.find(
            In(PersonModel.id, [uuid.UUID(id) for id in req.person_ids])
        ).to_list()
        collections = merge_auto_collections(persons_init)
        merged_person.posts = collections["posts"]
        merged_person.connections = collections["connections"]
        merged_person.interests = collections["interests"]
        merged_person.geo_trace = collections["geo_trace"]
        person = await persons.merge_persons(merged_person,
                                             user_info,
                                             project_id,
                                             req.person_ids)
        # run logic for scores recalc
        background_tasks.add_task(
            asyncio.get_event_loop().create_task,
            calculate_merged_person_score(person),
        )
        return {
            "merged_person_id": str(person.id),
            "merge_mode": req.merge_mode,
        }
    except Exception as e:
        print('ERROR during merge:', str(e))
        raise HTTPException(
            500,
            "Something went wrong while merging. Please try again."
        ) from e

async def calculate_merged_person_score(person: Person):
    try:
        await recalculate_person_score.kiq(str(person.id))
    except Exception as e:
        logger.info(e)
        return


def get_principal_user_info(principal):
    return {
        "firstname": principal.first_name,
        "lastname": principal.last_name,
        "id": principal.id,
        "email": principal.email
    }
