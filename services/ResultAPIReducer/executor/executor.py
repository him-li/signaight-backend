import asyncio
import uuid
from beanie.operators import In, Or
from core.flows.complex_search.utils import apply_primary_rules
from core.utils.constants.primary_candidates import COMMON_PRIMARY_CANDIDATE_SOURCES
from core.utils.socials_list import SOCIALS
import pendulum
from business_rules import run_all, async_run_all
from datetime import datetime
from docarray import DocList
from jina import Executor
from jina import requests
from mergedeep import merge, Strategy
from typing import Optional, List, Dict

from core.documents import (SearchResponseDoc,
                            EnrichResponseDoc,
                            ActiveSearchResponseDoc)
from core.database import init_db
from core.storage import init_storage
from core.models import (
    CandidateModel,
    PersonModel,
    AlertsModel,
    EvaluationModel,
    Candidate,
    ActiveSearchEventModel,
    FlagModel,
    NetworkSignature
)
from core.models.utils import dedupe_posts
from core.rules.person import (PersonVariables, PersonActions)
from core.utils import (parse_urn, SignAIghtURN,
                        delete_none, extract_score_compatibility_rules
                        )
from core.models.utils import post_service_log
from core.logging import logger
from core.rules.person.person_ruleset import (
    person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635 as
    base_person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635,
    person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04 as
    base_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04)

from .schemas import PersonUpdate
from .config import settings



class ResultAPIReducer(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        init_storage()
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio
        # loops which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    @requests(on="/search")
    async def search_enrich_reducer(
        self,
        docs: DocList[SearchResponseDoc],
        parameters: Dict,
        docs_matrix: Optional[List[DocList[SearchResponseDoc]]],
        **kwargs
    ) -> DocList[SearchResponseDoc]:
        flow_step = parameters.get('flow_step')
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry",
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from ResultAPIReducer "
                        f"search saving candidates entry: {str(e)}")

        now = datetime.now()
        if len(docs) == 0:
            return DocList[SearchResponseDoc]()
        start_time = pendulum.now()
        saved_count = 0

        async def docs_aiter(docs, logger):
            for i, doc in enumerate(docs):
                if i == 0:
                    logger.info(f"ResultAPIReducer /search id:{doc.search_id} "
                                f"urn:{doc.urn} - {len(docs)} candidates")
                yield doc

        async for doc in docs_aiter(docs, self.logger):
            if not doc.source:
                continue
            data = doc.model_dump()
            # cleanup doc.id cause different formats with beanie
            data.pop('id')
            # Probably bug here with error
            # 'NoneType' object has no attribute 'find_one'
            try:
                # person_id is available without model instance for DBRef
                data["person"] = parse_urn(doc.urn)
                data["searched_at"] = now
                data["last_update"] = now
                candidate_exists = await self._is_candidate_exists(
                    data, doc, docs)
                if not candidate_exists:
                    person_id = uuid.UUID(data.get('person'))
                    candidate_source = data.get("source")
                    candidate_person = await PersonModel.get(
                        person_id, fetch_links=False)
                    matched_profiles = getattr(
                        candidate_person.network_signature,
                        "matched_profiles",
                        None) if candidate_person.network_signature else None

                    source_matched = (
                        getattr(
                            matched_profiles, candidate_source, None) if
                        matched_profiles else None)

                    if (source_matched and
                            source_matched.candidates_count >=
                            settings.REDUCER_SEARCH_RESULTS_PER_SOURCE_LIMIT):
                        continue
                    candidate = CandidateModel(**data)
                    flow_step = parameters.get('flow_step')
                    apply_primary_rules(
                        candidate=candidate,
                        flow_step=flow_step,
                        request_params=parameters,
                        rules=parameters.get(
                            "primary_candidate_sources",
                            COMMON_PRIMARY_CANDIDATE_SOURCES,
                        ),
                    )
                    # if (candidate.resource == 'grayfox' and
                    #         candidate.source not in ['web',
                    #                                  'deepweb',
                    #                                  'darkweb']):
                    #     candidate.primary = True
                    #     candidate.ds_filter = True

                    await CandidateModel.insert(candidate)

                    saved_count += 1
            except Exception as e:
                print(str(e))
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="ResultAPIReducer",
                    search_step="search",
                    message=(f"Error during candidate saving: {str(e)}"),
                    docs_count=len(docs),
                    step_point="error"
                )
                # TODO: maybe telemetry log here
                pass
        end_time = pendulum.now()
        logger.info("{} docs prepared and saved in {:.2f} seconds from {}"
                    " docs".format(
                        saved_count, end_time.int_timestamp -
                        start_time.int_timestamp, len(docs)
                    ))
        self.logger.debug(
            "{} docs prepared and saved in {:.2f} seconds from {}"
            " docs".format(
                saved_count, end_time.int_timestamp -
                start_time.int_timestamp, len(docs)
            ))
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="search",
                        message=(
                            "Finished saving {} candidates in {:.2f} "
                            "seconds".format(
                                saved_count,
                                end_time.int_timestamp -
                                start_time.int_timestamp)),
                        docs_count=len(docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from ResultAPIReducer "
                        f"finished savind candidates: {str(e)}")

        return docs
        '''
        if no_enrich is True:
        else:
            for candidate in saved_candidates:
                source_ids = build_source_ids_dict(candidate)
                source_usernames = build_usernames_dict(candidate)
                enrich_request_doc = build_enrich_docarray(
                    candidate.id,
                    source_ids,
                    sources_resources,
                    source_usernames,
                    "candidates"
                    )
                out_docs.extend(enrich_request_doc)
            return DocList[EnrichRequestDoc](out_docs)
        '''

    # NOTE: Deprecated method
    # async def search_reducer(
    #     self,
    #     docs: DocList[SearchResponseDoc],
    #     **kwargs
    # ) -> DocList[SearchResponseDoc] | None:
    #     now = datetime.now()
    #     if len(docs) == 0:
    #         return DocList[SearchResponseDoc]()
    #     out_docs = []
    #     start_time = pendulum.now()
    #     # for doc in docs:
    #     #    print(doc)
    #     for doc in docs:
    #         data = doc.dict()
    #         # cleanup doc.id cause different formats with beanie
    #         data.pop('id')
    #         # Probably bug here with error
    #         # 'NoneType' object has no attribute 'find_one'
    #         # try:
    #         # person_id is available without model instance for DBRef
    #         data["person"] = parse_urn(doc.urn)
    #         data["searched_at"] = now
    #         data["last_update"] = now
    #         candidate = CandidateModel(**data)
    #         out_docs.append(candidate)
    #         # except Exception as e:
    #         #    print(str(e))
    #         #    # TODO: maybe telemetry log here
    #         #    pass
    #     end_time = pendulum.now()
    #     self.logger.debug(
    #         "{} docs prepared for saving in {:.2f} seconds".format(
    #             len(out_docs), end_time.int_timestamp -
    #             start_time.int_timestamp
    #         ))

    #     if out_docs:
    #         start_time = pendulum.now()
    #         try:
    #             for _candidate in out_docs:
    #                 candidate_exists = await self._is_candidate_exists(
    #                     _candidate)
    #                 if not candidate_exists:
    #                     await CandidateModel.insert(_candidate)
    #         except Exception as e:
    #             logger.error(str(e))
    #         end_time = pendulum.now()
    #         self.logger.info("Saved {} docs into db in {:.2f} seconds".format(
    #             len(out_docs), end_time.int_timestamp -
    #             start_time.int_timestamp
    #         ))
    #     return out_docs

    @requests(on="/enrich")
    async def enrich_reducer(
        self,
        docs: DocList[EnrichResponseDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[EnrichResponseDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry",
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        if len(docs) == 0:
            return DocList[EnrichResponseDoc]()

        async def docs_aiter(docs, logger):
            for i, doc in enumerate(docs):
                if i == 0:
                    logger.info(f"ResultAPIReducer /search id:{doc.search_id} "
                                f"urn:{doc.urn}")
                yield doc

        async for doc in docs_aiter(docs, self.logger):
            urn = SignAIghtURN(doc.urn)
            if urn.resource == "candidates":
                candidate_saving_start_time = pendulum.now()
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="enrich",
                        message="Saving candidate started",
                        docs_count=len(docs),
                        step_point="processing",
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from"
                        f" ResultAPIReducer enrich saving candidate: {str(e)}")

                now = datetime.now()
                try:

                    data = doc.model_dump()
                    for field in ["id", "_id"]:
                        data.pop(field, None)
                    data = delete_none(data)

                    candidate_id = urn.id
                    candidate = await CandidateModel.get(candidate_id)
                    candidate_dict = candidate.model_dump()
                    candidate_dict["last_update"] = now

                    update_candidate = merge(candidate_dict,
                                            data,
                                            strategy=Strategy.REPLACE)
                    # cleanup blank values
                    update_candidate = delete_none(update_candidate)
                    update_candidate = {k: v for k, v in
                                        update_candidate.items() if v}
                    updated_candidate = CandidateModel(**update_candidate)
                    await updated_candidate.save()
                    candidate_saving_end_time = pendulum.now()
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="ResultAPIReducer",
                            search_step="enrich",
                            message="Saving candidate finished in {:.2f} seconds".format(  # noqa
                                candidate_saving_end_time.int_timestamp -
                                candidate_saving_start_time.int_timestamp),
                            docs_count=len(docs),
                            step_point="processing",
                            step_duration_microseconds=(
                                candidate_saving_end_time.diff(
                                    candidate_saving_start_time
                                    )._to_microseconds())
                        )
                    except Exception as e:
                        logger.error(
                            f"Unable to send service log from ResultAPIReducer"
                            f" enrich saving candidate finished: {str(e)}")
                except Exception as e:
                    self.logger.error(f'Unable to enrich candidate: {str(e)}')
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="enrich",
                        message=f'Unable to enrich candidate: {str(e)}',
                        docs_count=len(docs),
                        step_point="error"
                    )

            # TODO: save person data in aggregation executor instead of reducer
            elif urn.resource == "persons":
                now = datetime.now()

                try:
                    data = doc.model_dump()

                    person_id = parse_urn(doc.urn)
                    person = await PersonModel.get(person_id, fetch_links=True)
                    if not person:
                        continue

                    # Remove document id cause it do not compatible with
                    # mongo UUID primary key
                    fileds_to_cleanup = ['id', 'resource', 'source',
                                        'urn', 'dcotype', 'revision_id',
                                        'recruiting_source', 'search_id']
                    for filed_to_cleanup in fileds_to_cleanup:
                        data.pop(filed_to_cleanup, None)
                    # Merge data from model and from enrichment here
                    data_posts = {'posts': data.pop('posts', [])}
                    data = merge(person.model_dump(), data,
                                strategy=Strategy.REPLACE)
                    data = merge(data, data_posts, strategy=Strategy.ADDITIVE)
                    data_posts_with_dupes = data.get('posts', [])
                    unduped_posts = dedupe_posts(data_posts_with_dupes)
                    data = merge(data, {'posts': unduped_posts},
                                strategy=Strategy.REPLACE)
                    # cleanup blank values
                    data = delete_none(data)
                    # we need to make update correct with preserve
                    # document version key in classic api operation way
                    saving_start_time = pendulum.now()
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="ResultAPIReducer",
                            search_step="enrich",
                            message="Saving person started",
                            docs_count=len(docs),
                            step_point="processing",
                        )
                    except Exception as e:
                        logger.error(
                            f"Unable to send service log from ResultAPIReducer"
                            f" enrich saving person started: {str(e)}")
                    update = PersonUpdate(**data)
                    update = {k: v for k,
                              v in update.model_dump().items() if v}
                    for k, v in update.items():
                        setattr(person, k, v)
                    person.last_update = now
                    await person.save_changes()
                    saving_end_time = pendulum.now()
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="ResultAPIReducer",
                            search_step="enrich",
                            message="Saving person finished in {:.2f} seconds".format(  # noqa
                                saving_end_time.int_timestamp -
                                saving_start_time.int_timestamp),
                            docs_count=len(docs),
                            step_point="processing",
                            step_duration_microseconds=saving_end_time.diff(
                                saving_start_time)._to_microseconds()
                        )
                    except Exception as e:
                        logger.error(
                            f"Unable to send service log from ResultAPIReducer"
                            f" enrich saving person finished: {str(e)}")
                except Exception as e:
                    self.logger.error(f'Unable to enrich person: {str(e)}')
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="enrich",
                        message=f'Unable to enrich person: {str(e)}',
                        docs_count=len(docs),
                        step_point="error"
                    )
                    return None
                # apply heuristic rules only after success save for person
                try:
                    ruleset_run_start_time = pendulum.now()
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="ResultAPIReducer",
                            search_step="enrich",
                            message="Applying person ruleset started",
                            docs_count=len(docs),
                            step_point="processing",
                        )
                    except Exception as e:
                        logger.error(
                            f"Unable to send service log from ResultAPIReducer"
                            f" applying person ruleset started: {str(e)}")
                    person_project = person.project.model_dump()
                    person_ruleset = person_project.get("person_ruleset")
                    person_ruleset = [delete_none(
                        ruleset) for ruleset in person_ruleset]
                except Exception:
                    person_ruleset = base_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04  # noqa
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
                    if not alerts:
                        alerts = AlertsModel(person=person)
                    if not evaluation:
                        evaluation = EvaluationModel(person=person)
                    if not flags:
                        flags = FlagModel(person=person)
                    await async_run_all(
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
                    try:
                        score_compatibility_ruleset = (
                            extract_score_compatibility_rules(
                                person_ruleset))
                    except Exception:
                        score_compatibility_ruleset = (
                            extract_score_compatibility_rules(
                                base_person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04))  # noqa
                    run_all(
                        rule_list=score_compatibility_ruleset,
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
                    await person.save()
                    try:
                        await alerts.save()
                    except Exception:
                        pass
                    try:
                        await flags.save()
                    except Exception:
                        pass
                    await evaluation.save()
                    ruleset_run_end_time = pendulum.now()
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="ResultAPIReducer",
                            search_step="enrich",
                            message="Applying person ruleset finished in {:.2f} seconds".format(  # noqa
                                ruleset_run_end_time.int_timestamp -
                                ruleset_run_start_time.int_timestamp),
                            docs_count=len(docs),
                            step_point="processing",
                            step_duration_microseconds=ruleset_run_end_time.diff(
                                ruleset_run_start_time)._to_microseconds()
                        )
                    except Exception as e:
                        logger.error(
                            f"Unable to send service log from ResultAPIReducer"
                            f" applying person ruleset finished: {str(e)}")
                except Exception as e:
                    logger.error(f"Error in ResultAPIReducer {str(e)}")
        end_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="ResultAPIReducer",
                        search_step="enrich",
                        message="Finished saving in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds()
                    )
                except Exception as e:
                    logger.error(
                        f"Unable to send service log from"
                        f" ResultAPIReducer finished saving person: {str(e)}")
        return docs

    @requests(on="/active_search")
    async def active_search_reducer(
        self,
        docs: DocList[ActiveSearchResponseDoc],
        parameters: Dict,
        docs_matrix: Optional[List[DocList[ActiveSearchResponseDoc]]],
        **kwargs
    ) -> DocList[ActiveSearchResponseDoc]:
        now = datetime.now()
        if len(docs) == 0:
            return DocList[ActiveSearchResponseDoc]()
        start_time = pendulum.now()
        saved_count = 0
        for doc in docs:
            if not doc.source:
                continue
            data = doc.model_dump()
            # cleanup doc.id cause different formats with beanie
            data.pop('id')
            try:
                active_search = await ActiveSearchEventModel.find_one(
                    ActiveSearchEventModel.id == uuid.UUID(doc.search_id))
                data["searched_at"] = now
                data["last_update"] = now
                candidate = Candidate(**data)
                active_search.search_results.append(candidate)
                await active_search.save()
                saved_count += 1

            except Exception as e:
                print(str(e))
                # TODO: maybe telemetry log here
                pass
        end_time = pendulum.now()
        self.logger.debug(
            "{} docs prepared and saved in {:.2f} seconds from {}"
            " docs".format(
                saved_count, end_time.int_timestamp -
                start_time.int_timestamp, len(docs)
            ))

        return docs

    async def _is_candidate_exists(self, _candidate: Dict, doc, docs):
        try:
            conditions = []

            _candidate_network_sig = NetworkSignature(
                **_candidate.get("network_signature")
            )

            signature_groups = {
                "user_id": _candidate_network_sig.user_id,
                "username": _candidate_network_sig.username,
                "url": _candidate_network_sig.url,
            }

            for group_name, group_obj in signature_groups.items():

                if not group_obj:
                    continue

                for field_name, values in group_obj.model_dump(exclude_none=True).items():

                    if not values:
                        continue

                    conditions.append(
                        In(
                            getattr(
                                getattr(CandidateModel.network_signature, group_name),
                                field_name,
                            ),
                            values,
                        )
                    )

            if not conditions:
                return False

            same_candidate = await CandidateModel.find(
                CandidateModel.search_id == _candidate.get("search_id"),
                Or(*conditions),
            ).to_list()

            if same_candidate:
                return True

        except Exception as e:
            self.logger.debug("Error when checking duplicated candidate")
            self.logger.debug(e)

            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="search",
                message=f"Error during candidate saving: {str(e)}",
                docs_count=len(docs),
                step_point="error",
            )

        return False
