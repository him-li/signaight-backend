import asyncio
from core.dbclient import with_transaction
from core.utils.reassign_candidates_to_merged_person import (
    reassign_candidates_to_merged_person)
import pendulum
import uuid
from beanie.operators import In, NotIn, Set, Or
from bson.binary import Binary as uuidBinary
from datetime import datetime
from fastapi import HTTPException, status as http_status, BackgroundTasks
from typing import Dict, Iterable, List

from api.acl import Principal
from api.crud import BasicCRUD
from api.local_authorization import require_project_access
from api.pagination import paginate
from core.config import settings
from core.logging import logger
from core.models import (
    PersonModel,
    CandidateModel,
    ProjectModel,
    PersonModelAuditLog,
    ResourceActionLogModel,
    WebSearchModel,
    FlagModel,
    EvaluationModel,
    AlertsModel
)
from core.dotty_dictionary import dotty
from core.models.person import Person
from core.models.connections import (
    FacebookConnection,
    InstagramConnection,
    Connections,
    Friends,
    Followers,
    Following)
from core.models.utils import (
    extend_person_info,
    enrich_connection_info)
from core.flows import complex_search_flow
from core.providers import build_fixture_candidates
from core.models.search_state import SearchState, SearchStatus
from tasks.app import (
    run_complex_search_flow,
    recalculate_person_score)
from .schemas import (
    ActionMethod,
    PersonFieldPatch,
    PersonListRead,
    PersonListView,
    PersonExportView,
    PersonDeleteBatch,
    ConnectionData
)
from ..projects.schemas import ProjectIdView, PersonRankingView


class PersonsCRUD(BasicCRUD):

    kind = "api.v1.persons"

    def __init__(self,
                 background_tasks: BackgroundTasks,
                 principal: Principal,
                 ):
        super().__init__(principal)
        self.background_tasks = background_tasks

    async def _pagination_transformer(self, items):
        return [PersonListRead(**item.model_dump()) for
                item in items]

    async def _logs_pagination_transformer(self, items):
        return [PersonModelAuditLog(**item.model_dump()) for
                item in items]

    async def _get_demo_person(self, person):
        # NOTE: demo data check id based only on firstname and lastname!
        try:
            f_name = person.personal_details.name.first_name.f_name.strip()
            l_name = person.personal_details.name.last_name.l_name.strip()
        except Exception:
            return False
        demo_person = await PersonModel.find_one(
            {
                "personal_details.name.first_name.f_name": f_name,
                "personal_details.name.last_name.l_name": l_name,
                "demo_data": True,
            }
        )
        if demo_person:
            return demo_person
        return False

    async def create(self, create, userinfo, is_bulk=False):
        # check for project existence
        if create.project_id:
            project = await ProjectModel.get(create.project_id)
            # TODO: this line has no sence cause there is no proper attribute in schema
            create.project = project if project else None
        else:
            if not is_bulk:
                raise HTTPException(
                    http_status.HTTP_400_BAD_REQUEST,
                    "Project required",
                )
            else:
                return None
        try:
            linkedin_url = create.network_signature.url.linkedin_profile_url
        except Exception:
            linkedin_url = None
        try:
            email = create.personal_details.email.email_address[0]
        except Exception:
            email = None
        try:
            phone = create.personal_details.phone.phones[0]
        except Exception:
            phone = None
        # check for same person with same linkedin url or email in project
        # , dedup
        # WARNING! sanitizing function hardcoded by param ONLY for linkedin urls
        if linkedin_url:
            exists = await PersonModel.find(
                PersonModel.project.id == create.project_id,
                (PersonModel.network_signature.url.linkedin_profile_url
                 == create.network_signature.url.linkedin_profile_url)
            ).exists()
            if exists:
                if not is_bulk:
                    raise HTTPException(
                        http_status.HTTP_400_BAD_REQUEST,
                        "Person already exists in campaign",
                    )
                else:
                    return None
        elif email:
            exists = await PersonModel.find(
                PersonModel.project.id == create.project_id,
                (PersonModel.personal_details.email.email_address[0]
                 == create.personal_details.email.email_address[0])
            ).exists()
            if exists:
                if not is_bulk:
                    raise HTTPException(
                        http_status.HTTP_400_BAD_REQUEST,
                        "Person already exists in campaign",
                    )
                else:
                    return None
        elif phone:
            exists = await PersonModel.find(
                PersonModel.project.id == create.project_id,
                (PersonModel.personal_details.phone.phones[0]
                 == create.personal_details.phone.phones[0])
            ).exists()
            if exists:
                if not is_bulk:
                    raise HTTPException(
                        http_status.HTTP_400_BAD_REQUEST,
                        "Person already exists in campaign",
                    )
                else:
                    return None

        # check for added persons qty by user daily
        exists_persons_daily = await ResourceActionLogModel.find(
            ResourceActionLogModel.meta.user_id == uuid.UUID(
                userinfo.get('id')),
            ResourceActionLogModel.meta.kind == self.kind,
            ResourceActionLogModel.meta.action == "create",
            ResourceActionLogModel.ts >= pendulum.now().start_of('day'),
            ResourceActionLogModel.ts <= pendulum.now().end_of('day')
        ).count()
        await self.authorized('create', {
            "owner_id": project.user_id,
            "future_persons_daily": exists_persons_daily + 1
        })
        demo_person = await self._get_demo_person(create)
        if demo_person:
            demo_data_dict = demo_person.model_dump()
            # relations cleanup
            demo_data_dict.pop('_id', None)
            demo_data_dict.pop('id', None)
            demo_data_dict.pop('project', None)
            # switch data from demo to false
            demo_target_dict = create.model_dump()
            person = PersonModel(**{
                **{
                    **demo_target_dict,
                    **demo_data_dict
                },
                **{
                    "demo_data": False,
                    "last_update": datetime.now(),
                    "last_edited_by": userinfo
                }
            })
            await person.insert()
            # get demo person flags
            demo_person_flags_query = FlagModel.find(
                {"person.$id": demo_person.id})
            async for demo_person_flag in demo_person_flags_query:
                demo_flag = demo_person_flag.model_dump(
                    exclude={'_id', 'id', 'person'}
                )
                flag = FlagModel(person=person.id, **demo_flag)
                await flag.insert()
            # get demo person evaluation
            demo_person_evaluations_query = EvaluationModel.find(
                {"person.$id": demo_person.id})
            async for demo_person_evaluation in demo_person_evaluations_query:
                print(demo_person_evaluation)
                demo_evaluation = demo_person_evaluation.model_dump(
                    exclude={'_id', 'id', 'person'}
                )
                evaluation = EvaluationModel(person=person.id,
                                             **demo_evaluation)
                await evaluation.insert()
            # get demo person alerts
            demo_person_alerts_query = AlertsModel.find(
                {"person.$id": demo_person.id})
            async for demo_person_alert in demo_person_alerts_query:
                demo_alert = demo_person_alert.model_dump(
                    exclude={'_id', 'id', 'person'}
                )
                alert = FlagModel(person=person.id, **demo_alert)
                await alert.insert()
        else:
            # search for existing person by linkedin url sorting by updated
            # TODO: maybe normalize linkedin_profile_url needed
            no_name_list = [None, "", "undefined"]
            existing_persons = None
            if linkedin_url:
                existing_persons = await PersonModel.find(
                    (PersonModel.network_signature.url.linkedin_profile_url
                        == create.network_signature.url.linkedin_profile_url),
                    PersonModel.search_state.is_done == True,
                    PersonModel.search_state.status == "Success",
                    NotIn(
                        PersonModel.personal_details.name.first_name.f_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.last_name.l_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.full_name.full_name,
                        no_name_list),
                ).sort(-PersonModel.last_update).to_list()
            elif email:
                existing_persons = await PersonModel.find(
                    (PersonModel.personal_details.email.email_address[0]
                        == create.personal_details.email.email_address[0]),
                    PersonModel.search_state.is_done == True,
                    PersonModel.search_state.status == "Success",
                    NotIn(
                        PersonModel.personal_details.name.first_name.f_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.last_name.l_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.full_name.full_name,
                        no_name_list),
                ).sort(-PersonModel.last_update).to_list()
            elif phone:
                existing_persons = await PersonModel.find(
                    (PersonModel.personal_details.phone.phones[0]
                        == create.personal_details.phone.phones[0]),
                    PersonModel.search_state.is_done == True,
                    PersonModel.search_state.status == "Success",
                    NotIn(
                        PersonModel.personal_details.name.first_name.f_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.last_name.l_name,
                        no_name_list),
                    NotIn(
                        PersonModel.personal_details.name.full_name.full_name,
                        no_name_list),
                ).sort(-PersonModel.last_update).to_list()

            if existing_persons and create.search_existing:
                existing_person = existing_persons[0]
                source_person_id = existing_person.id
                person_data = self._cleanup_data_for_copy(
                    existing_person.model_dump())
                person = PersonModel(**{
                    **person_data,
                    **{
                        "project": create.project_id,
                        "last_update": datetime.now(),
                        "last_edited_by": userinfo,
                        "search_state": {
                            "is_done": False,
                            "status": "In progress"
                        }
                    }
                })
                await person.insert()
                # get candidates for copied person
                candidates = await CandidateModel.find(
                    CandidateModel.person.id == source_person_id,
                    CandidateModel.primary == True
                ).to_list()
                for candidate in candidates:
                    candidate_data = self._cleanup_data_for_copy(
                        candidate.model_dump())
                    candidate_data['person'] = person.id
                    now_time = datetime.now()
                    candidate_data["searched_at"] = now_time
                    candidate = CandidateModel(**candidate_data)
                    await candidate.insert()

                self.background_tasks.add_task(
                    asyncio.get_event_loop().create_task,
                    self._calculate_score(person.id),
                )
            else:
                try:
                    create = await extend_person_info.extend_personal_details(
                        create)
                    person = PersonModel(
                        **{**create.model_dump(),
                           **{"last_edited_by": userinfo}})
                    await person.insert()

                    self.background_tasks.add_task(
                        asyncio.get_event_loop().create_task,
                        self._do_search(
                            userinfo.get('id'),
                            person,
                        ),
                    )
                except Exception as e:
                    print(e)
                    if is_bulk:
                        return None
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Person could not created! {str(e)}"
                        )

        # save success hit for creat action into log
        # TODO: maybe move into the model After create event
        resource_action_log = ResourceActionLogModel(**{
            "ts": datetime.now(),
            "meta": {
                "kind": self.kind,
                "action": "create",
                "user_id": userinfo.get('id')
            }
        })
        await ResourceActionLogModel.insert_one(resource_action_log)

        return person

    # NOTE: PErson and Candidate are very similar with structure
    def _cleanup_data_for_copy(self, data: Dict):
        data = dotty(data)
        fields = ['_id', 'id', 'project', 'comments',
                  'signaight_score', 'scores', 'search_state',
                  'created_at', 'last_update', 'last_edited_by',
                  'network_signature.matched_profiles', 'compatibility']
        data['recruiting_source'] = data.get('recruiting_source').value
        for field in fields:
            try:
                data.pop(field, None)
            except Exception as e:
                logger.info(e)
        data["demo_data"] = False
        data = data.to_dict()
        return data

    async def _do_search(self, user_id, persons):
        '''
        Search initiator internal method for new persons

        Arguments:
        user_id (UUID): current authorized user id
        persons (list): persons list

        Returns:
        None
        '''
        if not isinstance(persons, list):
            persons = [persons]

        if not settings.EXTERNAL_PROVIDERS_ENABLED:
            for person in persons:
                existing = await CandidateModel.find(
                    CandidateModel.person.id == person.id,
                    CandidateModel.resource == "fixture",
                ).count()
                if not existing:
                    for data in build_fixture_candidates(
                            person, str(person.id)):
                        await CandidateModel(person=person, **data).insert()
                if not person.network_signature:
                    from core.models import NetworkSignature
                    person.network_signature = NetworkSignature()
                from core.models.matched_profiles import MatchedProfiles, SourceInfo
                if not person.network_signature.matched_profiles:
                    person.network_signature.matched_profiles = MatchedProfiles()
                for source in ("linkedin", "instagram", "facebook"):
                    if not getattr(person.network_signature.matched_profiles, source):
                        setattr(person.network_signature.matched_profiles,
                                source, SourceInfo(candidates_count=2))
                person.search_state = SearchState(
                    is_done=True, status=SearchStatus.success)

                person.last_update = datetime.now()
                await person.replace()
            return

        for person in persons:
            if settings.JINA_REMOTE_FLOW_LINKEDIN:
                await run_complex_search_flow.kiq([str(person.id)],
                                                  str(user_id))
            else:
                await complex_search_flow([person.id], user_id)
        '''
            await complex_search_flow([person.id], search.id)
            search.updated_at = now
            search.status = "Done"
            search.percent_completed = 100
            search.duration = (now - search.created_at)
            await search.save()
        if search.status == "Done":
            message = MessageBuilder.search_message(search.id, "finished")
            await socket_manager.send_message_by_user_id(user_id, message)
        else:
            message = MessageBuilder.search_message(
                search.id, "In progress")
            await socket_manager.send_message_by_user_id(user_id, message)
        '''

    async def _calculate_score(self, person_id):
        if settings.JINA_REMOTE_FLOW_LINKEDIN:
            await recalculate_person_score.kiq(str(person_id))
        else:
            await recalculate_person_score(person_id)

    async def _adopt_filter_for_list(self, filter):
        # prevent loading persons where current user not owner of project
        query = ProjectModel.find_all()
        query = await self.authorized(
            'list',
            query,
            {
                "request.resource.attr.owner_id": "user_id"
            },
            kind="api.v1.projects"
        )
        # if filter.project__project_platform:
        #     query = query.find(ProjectModel.project_platform ==
        #                        filter.project__project_platform)
        user_projects = await query.project(ProjectIdView).to_list()
        user_project_ids = [project.id for project in user_projects]
        if filter.project__id:
            if filter.project__id in user_project_ids:
                user_project_ids = [filter.project__id]
            else:
                user_project_ids = []
        # check for filter attributes project__id and project__project_platform
        if filter.project__id:
            filter.project__id = None
        if filter.project__project_platform:
            filter.project__project_platform = None
        # DEPRECATED: filters working well when pagination fetch_links enabled
        # check for filter attributes project__id and project__project_platform
        if filter.project__project_platform:
            filter.project__project_platform = None
        return user_project_ids

    async def list(self, params, filter):
        user_project_ids = await self._adopt_filter_for_list(filter)
        query = None
        if filter.flags__in:
            person_ids = await self.resolve_person_ids_by_flags(filter.flags__in)
            if not person_ids:
                return await paginate(
                    query.find({"_id": {"$in": []}})
                )

            query = PersonModel.find(
                In(PersonModel.project.id, user_project_ids),
                In(PersonModel.id, person_ids),
            ).project(PersonListView)
            filter.flags__in = None
        else:
            query = PersonModel.find(
                In(PersonModel.project.id, user_project_ids),
            ).project(PersonListView)

        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query,
                              transformer=self._pagination_transformer)

    async def resolve_person_ids_by_flags(
        self, flags: Iterable[str],
    ) -> set:
        """
        Returns person IDs that have ANY of the given flags set (not None).
        """
        or_conditions = [
            {flag: {"$ne": None}}
            for flag in flags
        ]

        cursor = FlagModel.find(
            Or(*or_conditions),
            fetch_links=False,
        )

        return {pf.person.ref.id async for pf in cursor}

    async def create_without_search(self,
                                    create,
                                    userinfo,
                                    project_id,
                                    session) -> List[Person]:
        person_project = None
        if project_id:
            project = await ProjectModel.get(project_id)
            person_project = project if project else None

        try:

            person = PersonModel(
                **{**create.model_dump(),
                   **{
                       "last_edited_by": userinfo,
                    "last_update": datetime.now(),
                    "project": person_project
                }
                })
            await person.insert(session=session)

        except Exception as e:
            print(e)
        try:
            resource_action_log = ResourceActionLogModel(**{
                "ts": datetime.now(),
                "meta": {
                    "kind": self.kind,
                    "action": "merge",
                    "user_id": userinfo.get('id')
                }
            })
            await ResourceActionLogModel.insert_one(resource_action_log)
        except Exception as e:
            print(e)

        return person

    async def export(self, filter, data):
        user_project_ids = await self._adopt_filter_for_list(filter)
        query = PersonModel.find(
            In(PersonModel.project.id, user_project_ids),
            fetch_links=True
        )

        if person_ids := data.get('persons', []):
            query = query.find(
                In(PersonModel.id, person_ids)
            )
        query = query.project(PersonExportView)
        query = filter.filter(query)
        query = filter.sort(query)
        return await query.to_list()

    async def read_ids_list_by_project(self, project_id):
        project = await ProjectModel.get(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project does not exist!")
        require_project_access(self.principal, project.user_id)

        projects_person_ids = await PersonModel.find(
            PersonModel.project.id == project_id,
            fetch_links=True
        ).project(PersonRankingView).to_list()
        return [person.id for person in projects_person_ids]

    async def read_list_by_projects(self, params, filter, project_ids):
        # Beanie documented filtering with linked models
        try:
            project_ids_uuid_binary = [
                uuid.UUID(project_id) for project_id in project_ids
            ]
        except Exception:
            project_ids_uuid_binary = [
                project_id for project_id in project_ids
            ]
        query = PersonModel.find(
            # {"project.$id": {"$in": project_ids_uuid_binary}},
            In(PersonModel.project.id, project_ids_uuid_binary),
            fetch_links=True
        ).project(PersonListView)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def get_web_search_by_person_id(self, person_id: str):
        person_uuid = uuid.UUID(person_id)
        web_searches = await WebSearchModel.find(
            WebSearchModel.person.id == person_uuid,
            WebSearchModel.is_match == True
        ).to_list()
        return web_searches

    async def read_history(self, params, id, filter):
        uuid_binary = uuidBinary.from_uuid(id)
        query = PersonModelAuditLog.find({"entity.$id": uuid_binary})
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query,
                              transformer=self._logs_pagination_transformer)

    async def read(self, id) -> Person:
        person = await PersonModel.get(id, fetch_links=True)
        if not person or not person.project:
            raise HTTPException(
                status_code=404, detail="Person does not exist!")
        require_project_access(self.principal, person.project.user_id)
        return person

    async def read_demo_data(self, f_name, l_name):
        person = await PersonModel.find_one(
            {
                "personal_details.name.first_name.f_name": f_name,
                "personal_details.name.last_name.l_name": l_name,
                "demo_data": True,
            }
        )
        return person

    async def update(self, id, update, userinfo):
        person = await self.read(id)
        update = {k: v for k, v in update.model_dump().items()
                  if v is not None}
        for k, v in update.items():
            setattr(person, k, v)
        person.last_edited_by = userinfo
        person.set_editor(**userinfo)
        await person.save_changes()
        await PersonModel.rebuild_graph_connections(id)
        return person

    async def patch_comment(self, id, comment, userinfo):
        person = await self.read(id)
        comments = person.comments if person.comments is not None else []
        comments.append(comment)
        setattr(person, "comments", comments)
        person.last_edited_by = userinfo
        person.set_editor(**userinfo)

        await person.save_changes()
        return person

    async def patch_connection(self, id, connection, userinfo):
        person = await self.read(id)

        if not person.connections:
            person.connections = self._create_empty_connections()
        person.connections = self._ensure_nested_connections(
            person.connections)

        platform, connection_info = await self._enrich_connection_info(
            connection.connection_data)
        connection_type = connection.connection_type
        if connection_type == 'bidirectional':
            if platform == 'facebook':
                person.connections.friends.facebook.append(
                    FacebookConnection(**connection_info))
            elif platform == 'instagram':
                person.connections.followers.instagram.append(
                    InstagramConnection(**connection_info))
                person.connections.following.instagram.append(
                    InstagramConnection(**connection_info))
        elif connection_type == 'following':
            if platform == 'facebook':
                person.connections.following.facebook.append(
                    FacebookConnection(**connection_info))
            elif platform == 'instagram':
                person.connections.following.instagram.append(
                    InstagramConnection(**connection_info))
        elif connection_type == 'follower':
            if platform == 'facebook':
                person.connections.followers.facebook.append(
                    FacebookConnection(**connection_info))
            elif platform == 'instagram':
                person.connections.followers.instagram.append(
                    InstagramConnection(**connection_info))

        person.last_edited_by = userinfo
        person.set_editor(**userinfo)

        await person.save_changes()
        return person

    async def _enrich_connection_info(self, connection_data: ConnectionData):
        platform, connection_info = await enrich_connection_info(
            connection_data)
        return platform, connection_info

    def _create_empty_connections(self):
        return Connections(
            friends=Friends(
                facebook=[],
            ),
            followers=Followers(
                facebook=[],
                instagram=[]
            ),
            following=Following(
                facebook=[],
                instagram=[]
            )
        )

    def _ensure_nested_connections(self, connections) -> Connections:
        if not hasattr(connections, "friends") or not connections.friends:
            connections.friends = Friends(facebook=[])
        elif (not hasattr(connections.friends, "facebook") or
              not connections.friends.facebook):
            connections.friends.facebook = []

        if (not hasattr(connections, "followers") or
                not connections.followers):
            connections.followers = Followers(facebook=[], instagram=[])
        elif (not hasattr(connections.followers, "facebook") or
              not connections.followers.facebook):
            connections.followers.facebook = []
        elif (not hasattr(connections.followers, "instagram") or
              not connections.followers.instagram):
            connections.followers.instagram = []

        if (not hasattr(connections, "following") or
                not connections.following):
            connections.following = Following(facebook=[], instagram=[])
        elif (not hasattr(connections.following, "facebook") or
              not connections.following.facebook):
            connections.following.facebook = []
        elif (not hasattr(connections.following, "instagram") or
              not connections.following.instagram):
            connections.following.instagram = []
        return connections

    async def patch(self, id, patch, userinfo):
        person = await self.read(id)
        patch = {k: v for k, v in patch.model_dump().items() if v is not None}
        for key, value in patch.items():
            setattr(person, key, value)
        person.last_edited_by = userinfo
        person.set_editor(**userinfo)

        await person.save_changes()
        await PersonModel.rebuild_graph_connections(id)
        return person

    async def patch_fields(self, id, patch: PersonFieldPatch, userinfo):
        person = await self.read(id)
        self._apply_fields(person, patch.data, patch.operation)
        person.last_edited_by = userinfo
        person.set_editor(**userinfo)
        await person.save_changes()
        await PersonModel.rebuild_graph_connections(id)
        return person

    def _apply_fields(self, obj, data: dict, operation: str):
        """Recursively apply *data* onto *obj* (Pydantic model or plain dict)."""
        for key, value in data.items():
            current = getattr(obj, key, None)

            if current is None or operation == "replace":
                setattr(obj, key, value)
            elif isinstance(current, list) and isinstance(value, list):
                # add → extend the list
                setattr(obj, key, current + value)
            elif isinstance(value, dict) and hasattr(current, "model_fields"):
                # nested Pydantic model → recurse
                self._apply_fields(current, value, operation)
            elif isinstance(current, dict) and isinstance(value, dict):
                # plain dict → deep merge in-place
                self._merge_dicts(current, value, operation)
            else:
                # scalar or type mismatch → always replace
                setattr(obj, key, value)

    def _merge_dicts(self, target: dict, source: dict, operation: str):
        for k, v in source.items():
            if k not in target or operation == "replace":
                target[k] = v
            elif isinstance(target[k], list) and isinstance(v, list):
                target[k] = target[k] + v
            elif isinstance(target[k], dict) and isinstance(v, dict):
                self._merge_dicts(target[k], v, operation)
            else:
                target[k] = v

    async def delete(self, id):
        person = await self.read(id)
        # NOTE: We use person detaching from project instead of deleting
        # Outdated persons by 3 monts criteria will deleted by
        # periodic task garbage collector
        person.project = None
        await person.save_changes()
        return person

    async def delete_many(self, data: PersonDeleteBatch, session):
        """Function to delete batch of persons."""
        match data.method:
            case ActionMethod.All:
                persons = PersonModel.find(
                    PersonModel.project.id == data.project_id,
                    session=session,
                )
            case ActionMethod.Not_in:
                persons = PersonModel.find(
                    PersonModel.project.id == data.project_id,
                    NotIn(PersonModel.id, data.person_ids),
                    session=session,
                )
            case ActionMethod.In:
                persons = PersonModel.find(
                    PersonModel.project.id == data.project_id,
                    In(PersonModel.id, data.person_ids),
                    session=session,
                )
            case _:
                persons = None

        if persons:
            count = await persons.count()
            await persons.update(
                Set({PersonModel.project: None}),
                session=session,
            )
            return count

    @with_transaction
    async def merge_persons(self,
                            merged_person,
                            user_info,
                            project_id,
                            person_ids,
                            session):
        person = await self.create_without_search(merged_person,
                                                  user_info,
                                                  project_id,
                                                  session)
        ids = [uuid.UUID(pid) for pid in person_ids]
        delete_data = PersonDeleteBatch(
            method=ActionMethod.In,
            person_ids=ids,
            project_id=uuid.UUID(project_id)
        )
        await reassign_candidates_to_merged_person(ids, person, session)
        await self.delete_many(delete_data, session)
        return person
