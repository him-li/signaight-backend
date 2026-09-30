import asyncio
import uuid

from asyncer import asyncify
from business_rules import run_all
from beanie import After, Before
from beanie.operators import Or, Exists
from datetime import datetime, timedelta
from taskiq import (
    Context,
    TaskiqDepends,
    TaskiqEvents,
    TaskiqState
)
from typing import Annotated, List

from core.database import client as mongo_client, init_db
from core.models import (SearchEventModel, PersonModel, CandidateModel,
                         AlertsModel, EvaluationModel, FlagModel,
                         ProjectModel, ActiveSearchEventModel,
                         PersonModelAuditLog, RecalculationEventModel)
from core.models.event import Status
from core.flows import complex_search_flow, active_search_flow
from core.logging import logger
from core.socketio import MessageBuilder
from core.rules.person import (
    PersonVariables,
    PersonActions,
)
from core.rules.person.person_ruleset import (
    person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635 as
    original_person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635,
    person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04 as
    original_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04
)
from core.utils import (delete_none,
                        build_person_urn,
                        extract_score_compatibility_rules)

from .brokers import broker, scheduler  # noqa
from .config import settings
from .redis import send_notification



@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    db_initialized = False
    while not db_initialized:
        logger.info("Beanie(MongoDB) connection attempt")
        try:
            await init_db()
            db_initialized = True
        except Exception:
            await asyncio.sleep(5)
    logger.info("Beanie(MongoDB) started")


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await mongo_client.close()
    logger.info("Beanie(MongoDB) shutdown")


@broker.task(schedule=[{"cron": "15 4 * * *"}])
async def persons_without_project_cleanup() -> None:
    persons = PersonModel.find(
        Or(
            Exists(PersonModel.project, False),
            PersonModel.project == None
        ),
        PersonModel.created_at <= datetime.now()-timedelta(
            seconds=settings.TASKIQ_GARBAGE_COLLECTOR_DELTA),
        Or(
            PersonModel.last_update <= datetime.now()-timedelta(
                seconds=settings.TASKIQ_GARBAGE_COLLECTOR_DELTA),
            PersonModel.last_update == None,
            Exists(PersonModel.last_update, False),
        ),
        lazy_parse=True,
    )
    persons_count = await persons.count()
    logger.info(f"Persons to delete: {persons_count}")
    async for person in persons:
        # NOTE: set transaction individually for person cause limit of
        # 30 seconds and process falldown after transaction overlimit
        async with mongo_client.start_session() as session:
            async with await session.start_transaction():
                logger.info(f"Person: {person.id}")
                candidates = CandidateModel.find(
                    CandidateModel.person.id == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for candidate in candidates:
                    logger.info(f"Candidate: {candidate.id}")
                    await candidate.delete(skip_actions=[Before, After])
                alerts = AlertsModel.find(
                    AlertsModel.person.id == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for alert in alerts:
                    logger.info(f"Alert: {alert.id}")
                    await alert.delete(skip_actions=[Before, After])
                evaluations = EvaluationModel.find(
                    EvaluationModel.person.id == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for evaluation in evaluations:
                    logger.info(f"Evaluation: {evaluation.id}")
                    await evaluation.delete(skip_actions=[Before, After])
                flags = FlagModel.find(
                    FlagModel.person.id == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for flag in flags:
                    logger.info(f"Flag: {flag.id}")
                    await flag.delete(skip_actions=[Before, After])
                search_events = SearchEventModel.find(
                    SearchEventModel.persons_list == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for search_event in search_events:
                    logger.info(f"Search event: {search_event.id}")
                    await search_event.delete(skip_actions=[Before, After])
                auditlogs = PersonModelAuditLog.find(
                    PersonModelAuditLog.entity == person.id,
                    lazy_parse=True,
                    session=session
                )
                async for auditlog in auditlogs:
                    logger.info(f"Auditlog: {auditlog.id}")
                    await auditlog.delete(skip_actions=[Before, After])
                await person.delete(skip_actions=[Before, After])

'''
# NOTE: DEPRECATED cause we introduce better timouts processing
@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def check_stuck_person_search() -> None:
    # Note previous timeout for search before error was 120 minutes
    persons = PersonModel.find(
        Not(PersonModel.project == None),
        PersonModel.created_at <= datetime.now()-timedelta(
            seconds=settings.TASKIQ_BROKEN_SEARCHED_ITEMS_DELTA),
        Or(
            PersonModel.last_update <= datetime.now()-timedelta(
                seconds=settings.TASKIQ_BROKEN_SEARCHED_ITEMS_DELTA),
            PersonModel.last_update == None,
            Exists(PersonModel.last_update, False),
        ),
        And(
            Or(
                PersonModel.search_state.is_done == False,
                Exists(PersonModel.search_state.is_done, False)
            ),
            Or(
                PersonModel.search_state.status == 'In progress',
                Exists(PersonModel.search_state.status, False)
            )
        ),
        lazy_parse=True,
    )
    persons_count = await persons.count()
    logger.info(f"Persons to state fix: {persons_count}")
    async for person in persons:
        # NOTE: set transaction individually for person cause limit of
        # 30 seconds and process falldown after transaction overlimit
        async with mongo_client.start_session() as session:
            async with await session.start_transaction():
                logger.info(f"Person: {person.id}")
                await person.update(
                    {
                        "$set": {
                            PersonModel.search_state: {
                                "is_done": True,
                                "status": "Error",
                                "description": "Person search timeout"
                            }
                        }
                    },
                    session=session
                )
'''


async def person_search_status_to_db(
    person_id: uuid.UUID | str,
    status: str,
    description: str
):
    if not isinstance(person_id, uuid. UUID):
        person_id = uuid.UUID(person_id)
    person = await PersonModel.get(person_id)
    person.search_state.status = status
    person.search_state.description = description
    await person.save_changes()


@broker.task(
    priority=5,
    timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT+600,
    retry_on_error=settings.TASKIQ_TASK_RETRY_ON_ERRORS,
    max_retries=settings.TASKIQ_TASK_MAX_RETRIES
)
async def run_complex_search_flow(
    person_ids: List,
    user_id: str,
    context: Annotated[Context, TaskiqDepends()]
):
    person_ids_uuid = [uuid.UUID(person_id) for person_id in person_ids]
    events = await SearchEventModel.find(
        SearchEventModel.user_id == user_id,
        SearchEventModel.persons_list == person_ids_uuid,
    ).sort(
        -SearchEventModel.created_at
    ).to_list()
    if not events or len(events) == 0:
        search = SearchEventModel(**{
            "user_id": user_id,
            "flows_list": [],  # TODO: list of flows???
            "persons_list": person_ids,
            "retries": 0,
        })
        now = datetime.now()
        search.updated_at = now
        search.status = Status.started
        await search.insert()
    else:
        search = events[0]

    try:
        for person_id in person_ids:
            person_id = uuid.UUID(person_id)
            person = await PersonModel.get(person_id)
            person.search_state.status = "In progress"
            person.search_state.is_done = False
            await person.extend()
            await person.replace()
            send_notification(
                str(search.user_id),
                MessageBuilder.search_message(search.id, "started")
            )
    except Exception as e:
        for person_id in person_ids:
            await person_search_status_to_db(person_id, "Error", str(e))
        send_notification(
            str(search.user_id),
            MessageBuilder.search_message(search.id, "error")
        )
        return

    if not search:
        # TODO: make messages delivery through redis Pub/Sub
        return
    try:
        done = await asyncio.wait_for(
            complex_search_flow(person_ids, search.id),
            timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT
        )
        now = datetime.now()
        search_duration = now - search.created_at
        search.updated_at = now
        if done:
            search.status = Status.done
            search.percent_completed = 100
            search.duration = search_duration
            await search.replace()
            send_notification(
                str(search.user_id),
                MessageBuilder.search_message(search.id, "finished")
            )
            return
        else:
            retry_on_error = context.message.labels.get(
                'retry_on_error',
                settings.TASKIQ_TASK_RETRY_ON_ERRORS
            )
            max_retries = context.message.labels.get(
                'max_retries',
                settings.TASKIQ_TASK_MAX_RETRIES
            )
            if (not retry_on_error
                    or max_retries >= context.message.labels.get("_retries", 0)):
                for person_id in person_ids:
                    await person_search_status_to_db(person_id, "Error",
                                                     "Data error in search")
                logger.error(
                    f"Probably flow communication error for person search with person id {','.join(person_ids)}, rejecting task due task queue config!")
                # proper way to reject task but it do not allow
                # to set custom message
                # await context.reject()
                return
            else:
                search.retries = int(search.retries) + 1
                await search.replace()
                await asyncio.sleep(30)
                logger.error(
                    f"Probably flow communication error for person search with person id {','.join(person_ids)}, retrying!")
                # Maybe proper way to requeue task
                # await context.requeue()
                return
    except asyncio.TimeoutError as e:
        for person_id in person_ids:
            await person_search_status_to_db(person_id, "Timeout", str(e))
        return
    except Exception as e:
        for person_id in person_ids:
            await person_search_status_to_db(person_id, "Error", str(e))
        return


async def calculate_person_score(person,
                                 person_ruleset,
                                 full_recalculation=False):
    try:
        alerts = await AlertsModel.find_one(
            AlertsModel.person.id == person.id
        )
        evaluation = await EvaluationModel.find_one(
            EvaluationModel.person.id == person.id
        )
        flags = await FlagModel.find_one(
            FlagModel.person.id == person.id
        )
        if full_recalculation:
            await evaluation.delete()
            await alerts.delete()
            await flags.delete()
        if not alerts:
            alerts = AlertsModel(person=person)
        if not evaluation:
            evaluation = EvaluationModel(person=person)
        if not flags:
            flags = FlagModel(person=person)
        await asyncify(run_all)(
            rule_list=person_ruleset,
            defined_variables=PersonVariables(
                person,
                alerts,
                evaluation,
                flags
            ),
            defined_actions=PersonActions(
                person,
                alerts,
                evaluation,
                flags
            )
        )
        logger.info("calc is done!")
        try:
            await alerts.save()
        except Exception:
            pass
        try:
            await flags.save()
        except Exception:
            pass
        try:
            await evaluation.save()
        except Exception:
            pass
        try:
            await PersonModel.find_one(PersonModel.id == person.id).update(
                {
                    "$set": {
                        "search_state": {
                            "is_done": True,
                            "status": "Success",
                        },
                        "last_update": datetime.now(),
                        "risk_score": person.risk_score,
                        "compatibility": person.compatibility,
                        "signaight_score": person.signaight_score,
                        "scores": person.scores
                    }
                }
            )
        except Exception as e:
            logger.error(e)
    except Exception as e:
        logger.error(e)


@broker.task(
    timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT,
    retry_on_error=settings.TASKIQ_TASK_RETRY_ON_ERRORS,
    max_retries=settings.TASKIQ_TASK_MAX_RETRIES
)
async def recalculate_project_persons_score_heuristics(project_id):
    project_id = uuid.UUID(project_id)
    project = await ProjectModel.get(project_id)
    user_id = project.user_id
    project = project.model_dump()
    person_ruleset = project.get(
        "person_ruleset")
    if not person_ruleset:
        person_ruleset = original_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04  # noqa
    person_ruleset = [delete_none(
        ruleset) for ruleset in person_ruleset]
    project_persons = await PersonModel.find(
        PersonModel.project.id == project_id
    ).to_list()
    recalc_data = {
        "project_id": project_id,
        "user_id": user_id
    }
    recalc = RecalculationEventModel(**recalc_data)
    now = datetime.now()
    recalc.updated_at = now
    recalc.status = "Started"
    await recalc.insert()
    for person in project_persons:
        try:
            await calculate_person_score(person, person_ruleset,
                                         full_recalculation=True)
        except Exception as e:
            logger.info(e)
    now = datetime.now()
    recalc.updated_at = now
    recalc.status = "Done"
    await recalc.replace()
    send_notification(
        str(user_id),
        MessageBuilder.recalculation_message(
            str(recalc.id), "finished")
    )


@broker.task(
    timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT,
    retry_on_error=settings.TASKIQ_TASK_RETRY_ON_ERRORS,
    max_retries=settings.TASKIQ_TASK_MAX_RETRIES
)
async def recalculate_project_persons_score(project_id):
    project_id = uuid.UUID(project_id)
    project = await ProjectModel.get(project_id)
    user_id = project.user_id
    project = project.model_dump()
    person_ruleset = project.get(
        "person_ruleset")
    if not person_ruleset:
        person_ruleset = original_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04  # noqa
    person_ruleset = [delete_none(
        ruleset) for ruleset in person_ruleset]
    try:
        score_compatibility_ruleset = (
            extract_score_compatibility_rules(
                person_ruleset))
    except Exception:
        score_compatibility_ruleset = (
            extract_score_compatibility_rules(
                original_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04))  # noqa
    project_persons = await PersonModel.find(
        PersonModel.project.id == project_id
    ).to_list()
    recalc_data = {
        "project_id": project_id,
        "user_id": user_id
    }
    recalc = RecalculationEventModel(**recalc_data)
    now = datetime.now()
    recalc.updated_at = now
    recalc.status = "Started"
    await recalc.insert()
    for person in project_persons:
        try:
            await calculate_person_score(person, score_compatibility_ruleset,
                                         full_recalculation=False)
        except Exception as e:
            logger.info(e)
    now = datetime.now()
    recalc.updated_at = now
    recalc.status = "Done"
    await recalc.replace()
    send_notification(
        str(user_id),
        MessageBuilder.recalculation_message(
            str(recalc.id), "finished")
    )


@broker.task(
    timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT,
    retry_on_error=settings.TASKIQ_TASK_RETRY_ON_ERRORS,
    max_retries=settings.TASKIQ_TASK_MAX_RETRIES
)
async def recalculate_person_score(person_id):
    person_id = uuid.UUID(person_id)
    person = await PersonModel.get(person_id)
    await person.fetch_link(PersonModel.project)
    project = person.project.model_dump()
    person_ruleset = project.get("person_ruleset")
    person_ruleset = [delete_none(
        ruleset) for ruleset in person_ruleset]
    await calculate_person_score(person, person_ruleset)
    send_notification(
        str(person.project.user_id),
        MessageBuilder.person_message(str(person.id), "search finished")
    )
'''
# TODO: inspect search operations log
async def recalculate_person_score(person_id, user_id):
    search_data = {
        "user_id": user_id,
        "flows_list": [],  # TODO: list of flows???
        "persons_list": [person_id],
        "retries": 0,
    }
    search = SearchEventModel(**search_data)
    now = datetime.now()
    search.updated_at = now
    search.status = "Started"
    await search.insert()
    try:
        send_notification(
            str(search.user_id),
            MessageBuilder.search_message(search.id, "started")
        )
        person_id = uuid.UUID(person_id)
        person = await PersonModel.get(person_id)
        await person.fetch_link(PersonModel.project)
        project = person.project.model_dump()
        person_ruleset = project.get("person_ruleset")
        person_ruleset = [delete_none(
            ruleset) for ruleset in person_ruleset]
        await calculate_person_score(person, person_ruleset)
        now = datetime.now()
        search_duration = now - search.created_at
        search.updated_at = now
        search.status = Status.done
        search.percent_completed = 100
        search.duration = search_duration
        await search.replace()
        send_notification(
            str(search.user_id),
            MessageBuilder.search_message(search.id, "finished")
        )
        send_notification(
            str(person.project.id),
            MessageBuilder.project_message(person.project.id, "finished")
        )
    except Exception as e:
        person_id = uuid.UUID(person_id)
        person = await PersonModel.get(person_id)
        person.search_state.status = "Error"
        person.search_state.description = str(e)
        person.save_changes()
        send_notification(
            str(search.user_id),
            MessageBuilder.search_message(search.id, "error")
        )
'''


@broker.task(
    timeout=settings.TASKIQ_TASK_DEFAULT_TIMEOUT,
    retry_on_error=settings.TASKIQ_TASK_RETRY_ON_ERRORS,
    max_retries=settings.TASKIQ_TASK_MAX_RETRIES
)
async def run_active_search(active_search_id):
    active_search_id = uuid.UUID(active_search_id)
    active_search = await ActiveSearchEventModel.get(active_search_id)
    try:
        send_notification(
            str(active_search.user_id),
            MessageBuilder.active_search_message(active_search.id, "started")
        )
    except Exception as e:
        print(str(e))
        return

    host = (settings.JINA_REMOTE_FLOW_LINKEDIN
            if settings.JINA_REMOTE_FLOW_LINKEDIN else None)

    await active_search_flow(active_search_id,
                             active_search.title,
                             active_search.education,
                             active_search.location,
                             host)

    now = datetime.now()
    active_search = await ActiveSearchEventModel.get(active_search_id)
    search_duration = now - active_search.created_at
    active_search.updated_at = now
    active_search.status = Status.done
    active_search.percent_completed = 100
    active_search.duration = search_duration
    await active_search.save()

    send_notification(
        str(active_search.user_id),
        MessageBuilder.active_search_message(active_search.id, "finished")
    )
