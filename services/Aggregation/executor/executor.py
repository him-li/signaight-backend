import asyncio
import uuid
import pendulum
from datetime import datetime
from core.utils.image_utils import get_image_quality_cached
from jina import Executor, requests
from docarray import DocList
from typing import Dict, Any
from business_rules import run_all, async_run_all
from mergedeep import merge, Strategy

from core.documents import (
    AggregateRequestDoc,
    SearchRequestDoc,
    SearchResponseDoc,
)
from core.models import (
    PersonModel,
    AlertsModel,
    CandidateModel,
    EvaluationModel,
    FlagModel
)
from core.logging import logger
from core.models.utils import post_service_log
from core.database import init_db
from core.dotty_dictionary import dotty
from core.rules.person import (
    PersonVariables,
    PersonActions
)
from core.models.utils import dedupe_posts
from core.rules.person.person_ruleset import (
    person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635,
    person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04)
from core.utils import (build_search_docarray, delete_none,
                        extract_score_compatibility_rules, build_person_urn)
from core.utils.get_names_list import name_resolution

from .mappers import *  # noqa
from .schemas import PersonUpdate
from .config import settings



def safe_network_signature_merge(
    base: Dict[str, Any] | None,
    incoming: Dict[str, Any] | None
) -> Dict[str, Any]:
    base = base or {}
    incoming = incoming or {}

    cleaned_incoming = delete_none(incoming)

    merge(base, cleaned_incoming, strategy=Strategy.ADDITIVE)
    return base


class Aggregation(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio
        # loops which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    @requests(on="/enrich")
    async def update_person_from_candidate(
        self,
        docs: DocList[AggregateRequestDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[AggregateRequestDoc]:
        rule_set_skipping = parameters.get(
            "rule_set_skipping", False)
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="Aggregation",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        for doc in docs:
            self.logger.info(f"Aggregation /enrich "
                             f"id:{doc.search_id} urn:{doc.urn}")
            person_id = uuid.UUID(doc.person_id)
            candidate_id = uuid.UUID(
                doc.candidate_id) if doc.candidate_id else None

            person = await PersonModel.get(person_id, fetch_links=True)
            if not person:
                continue
            if candidate_id:
                candidates = await CandidateModel.find(
                    CandidateModel.person.id == person.id,
                    CandidateModel.id == candidate_id,
                    fetch_links=False
                ).to_list()
            else:
                candidates = await CandidateModel.find(
                    CandidateModel.person.id == person.id,
                    CandidateModel.primary == True,  # noqa
                    fetch_links=False
                ).to_list()

            best_by_source = {
                src: max(
                    (c for c in candidates if c.source == src),
                    key=lambda c: c.similarity
                )
                for src in {c.source for c in candidates}
            }
            candidates = list(best_by_source.values())

            update = person.model_dump()

            original_matched_profiles = None

            network_signature_update = update.get("network_signature")
            if isinstance(network_signature_update, dict):
                original_matched_profiles = network_signature_update.get(
                    "matched_profiles", None
                )
            for candidate in candidates:
                candidate_dict = candidate.model_dump()
                for field in ["id", "_id", "recruiting_source", "search_id"]:
                    candidate_dict.pop(field, None)
                candidate_dict = delete_none(candidate_dict)
                candidate_posts = {'posts': candidate_dict.pop('posts', [])}
                candidate_dict_network_signature = candidate_dict.pop(
                    'network_signature', None)
                update = merge(update, candidate_dict)
                update = merge(update,
                               candidate_posts,
                               strategy=Strategy.ADDITIVE)
                if not update.get("network_signature"):
                    update["network_signature"] = {}
                update["network_signature"] = safe_network_signature_merge(
                    network_signature_update,
                    candidate_dict_network_signature
                )
                update_posts_with_dupes = update.get('posts', [])
                unduped_posts = dedupe_posts(update_posts_with_dupes)
                update = merge(update, {'posts': unduped_posts},
                               strategy=Strategy.REPLACE)
                if original_matched_profiles is not None:
                    if not update.get("network_signature"):
                        update["network_signature"] = {}
                    update["network_signature"]["matched_profiles"] = original_matched_profiles
                update = delete_none(update)
                # update = self.aggregate_candidate(update,
                #                                   candidate.model_dump())
            # TODO: something wrong with marital_status_relatives dict.
            # Does not pass validation # noqa
            try:
                if biographic_details := update.get('biographic_details', {}):
                    biographic_details.pop(
                        'marital_status_relatives', None)
            except Exception as e:
                self.logger.error(str(e))
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="Aggregation",
                    search_step="enrich",
                    message=f"Error during aggregation: {str(e)}",
                    docs_count=len(docs),
                    step_point="error"
                )
            # TODO: maybe change process to avoid default picture
            # from different sources and make it configurable
            metadata_candidate = await CandidateModel.find(
                CandidateModel.person.id == person.id,
                CandidateModel.source == 'metadata',
                CandidateModel.primary == True,
                fetch_links=False
            ).first_or_none()
            if metadata_candidate:
                metadata_candidate_dotty = metadata_candidate.model_dump()
                for field in ["id", "_id", "recruiting_source", "search_id"]:
                    metadata_candidate_dotty.pop(field, None)
                candidate_dict = delete_none(metadata_candidate_dotty)
                update = merge(update, metadata_candidate_dotty)
                if original_matched_profiles is not None:
                    if not update.get("network_signature"):
                        update["network_signature"] = {}
                    update["network_signature"]["matched_profiles"] = original_matched_profiles
            update_dotty = dotty(update)
            try:
                profile_photo = update_dotty.get(
                    "personal_details.visuals.profile_photo")
                destinations = [
                    picture for picture in (profile_photo or {}).values() if picture]
                data = {
                    "destination": [str(p) for p in destinations]
                }
                try:
                    response = await get_image_quality_cached(
                        data,
                        headers={
                            'x-remote-context': build_person_urn(person_id)
                        }
                    )
                    sorted_pics_by_quality = sorted(
                        response.items(),
                        key=lambda x: (
                            x[1].get('scores', {}).get('face_score', -1),
                            x[1].get('scores', {}).get('artifact_score', -1)
                        ),
                        reverse=True
                    )
                    pic, metadata = sorted_pics_by_quality[0]
                    quality = metadata.get('scores', {}).get('face_score', -1)

                    if pic and quality >= 0.70:
                        update['personal_details']['visuals'][
                            'profile_photo']['profile_picture'] = pic
                except Exception as e:
                    logger.error(str(e))
            except Exception as e:
                logger.error(str(e))
            person_f_name = None
            person_l_name = None
            person_full_name = None

            try:
                person_f_name = person.personal_details.name.first_name.f_name
            except Exception:
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="Aggregation",
                    search_step="enrich",
                    message="Error during aggregation first name fetch",
                    docs_count=len(docs),
                    step_point="error"
                )
                pass
            try:
                person_l_name = person.personal_details.name.last_name.l_name
            except Exception:
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="Aggregation",
                    search_step="enrich",
                    message="Error during aggregation last name fetch",
                    docs_count=len(docs),
                    step_point="error"
                )
                pass
            try:
                person_full_name = (
                    person.personal_details.name.full_name.full_name)
            except Exception:
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="Aggregation",
                    search_step="enrich",
                    message="Error during aggregation full name fetch",
                    docs_count=len(docs),
                    step_point="error"
                )
                pass

            try:
                normalized_person_name = await name_resolution(update_dotty)
                parts = normalized_person_name.strip().split() if normalized_person_name else []

                if len(parts) == 2:
                    person_f_name = parts[0]
                    person_l_name = parts[1]
                person_full_name = f"{person_f_name} {person_l_name}"
                if len(parts) > 2:
                    person_f_name = parts[0]
                    person_l_name = " ".join(parts[1:])
                    person_full_name = f"{person_f_name} {person_l_name}"
                update['personal_details']['name'][
                    'first_name']['f_name'] = person_f_name
                update['personal_details']['name'][
                    'last_name']['l_name'] = person_l_name
                update['personal_details']['name'][
                    'full_name']['full_name'] = person_full_name

            except Exception as e:
                self.logger.info(e)
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="Aggregation",
                    search_step="enrich",
                    message=f"Error during aggregation name fetch: {str(e)}",
                    docs_count=len(docs),
                    step_point="error"
                )
            update = PersonUpdate(**update)

            update = {k: v for k, v in update.model_dump().items()
                      if v is not None}
            # TODO: revision id trying to fix, needs to check
            person = await PersonModel.get(person_id, fetch_links=True)
            for k, v in update.items():
                setattr(person, k, v)
            person.last_update = datetime.now()
            await person.save_changes()
            await PersonModel.rebuild_graph_connections(person_id)

            if rule_set_skipping:
                continue

            # apply heuristic rules
            try:
                person_project = person.project.model_dump()
                person_ruleset = person_project.get("person_ruleset")
                person_ruleset = [delete_none(
                    ruleset) for ruleset in person_ruleset]
            except Exception:
                person_ruleset = person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04  # noqa
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
                    person, alerts, evaluation, flags),
                defined_actions=PersonActions(
                    person, alerts, evaluation, flags)
            )
            try:
                score_compatibility_ruleset = (
                    extract_score_compatibility_rules(
                        person_ruleset))
            except Exception:
                score_compatibility_ruleset = (
                    extract_score_compatibility_rules(
                        person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04))  # noqa
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
            await person.save_changes()
            try:
                await alerts.save()
            except Exception:
                pass
            try:
                await flags.save()
            except Exception:
                pass
            await evaluation.save()
        end_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="Aggregation",
                        search_step="enrich",
                        message="Finished saving in {:.2f} seconds".format(
                            end_time.int_timestamp - start_time.int_timestamp),
                        docs_count=len(docs),
                        step_point="out",
                        step_duration_microseconds=end_time.diff(
                            start_time)._to_microseconds())
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        return docs

    @requests(on='/search')
    async def aggregate_linkedin_first(
        self,
        docs: DocList[SearchResponseDoc],
        parameters: Dict,
        **kwargs
    ) -> DocList[SearchRequestDoc]:
        start_time = pendulum.now()
        for i, doc in enumerate(docs):
            if i == 0:
                try:
                    post_service_log(
                        search_id=doc.search_id,
                        urn=doc.urn,
                        executor="Aggregation",
                        search_step="search",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        sources_resources = parameters.get('sources_resources')
        first_candidate = await CandidateModel.get(docs[0].candidate_id)

        if first_candidate.source == 'linkedin' and len(docs) == 1:
            await self.update_person_from_candidate(docs, **kwargs)
            doc = docs[0]
            self.logger.info(f"Aggregation /search "
                             f"id:{doc.search_id} urn:{doc.urn}")

            person = await PersonModel.get(doc.person_id)

            search_docs = build_search_docarray(
                person_id=doc.person_id,
                name=person.personal_details.name.full_name.full_name,
                f_name=person.personal_details.name.first_name.f_name,
                l_name=person.personal_details.name.last_name.l_name,
                search_id=first_candidate.search_id,
                email_address=person.personal_details.email.email_address[0],
                sources_resources=sources_resources)
            end_time = pendulum.now()
            for i, doc in enumerate(docs):
                if i == 0:
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="Aggregation",
                            search_step="search",
                            message="Finished in {:.2f} seconds".format(
                                end_time.int_timestamp -
                                start_time.int_timestamp),
                            docs_count=len(docs),
                            step_point="out",
                            step_duration_microseconds=end_time.diff(
                                start_time)._to_microseconds()
                        )
                    except Exception as e:
                        logger.error(f"Unable to send service log: {str(e)}")
            return DocList[SearchRequestDoc](docs=search_docs)

        else:
            for doc in docs:
                self.logger.info(f"Aggregation /search "
                                 f"id:{doc.search_id} urn:{doc.urn}")
                await self.update_person_from_candidate([doc], **kwargs)
            end_time = pendulum.now()
            for i, doc in enumerate(docs):
                if i == 0:
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="Aggregation",
                            search_step="search",
                            message="Finished in {:.2f} seconds".format(
                                end_time.int_timestamp -
                                start_time.int_timestamp),
                            docs_count=len(docs),
                            step_point="out",
                            step_duration_microseconds=end_time.diff(
                                start_time)._to_microseconds()
                        )
                    except Exception as e:
                        logger.error(f"Unable to send service log: {str(e)}")
            return docs

    def aggregate_candidate(self, person, candidate):
        personal_details = PersonalDetails()  # noqa
        person = personal_details.update_personal_details(
            person,
            candidate)
        bio_details = BioDetails()  # noqa
        person = bio_details.update_bio_details(person, candidate)
        network_signature = NetworkSignature()  # noqa
        person = network_signature.update_network_signature(
            person,
            candidate)
        posts = Posts()  # noqa
        person = posts.update_posts(person, candidate)

        return person

    def _find_most_frequent(self, data):
        value_counts = {}

        for key, value in data.items():
            if value is not None:
                if value not in value_counts:
                    value_counts[value] = 0
                value_counts[value] += 1
        most_frequent_value = None
        max_count = 0

        for value, count in value_counts.items():
            if count > max_count:
                max_count = count
                most_frequent_value = value

        if max_count >= 2:
            return most_frequent_value

        social_priority = [
            "linkedin", "google", "youtube", "facebook", "instagram",
            "twitter", "github", "tgm", "microsoft", "apple", "dropbox",
            "notion", "medium", "wikipedia", "fitbit", "myfitnesspal",
            "duolingo", "strava", "edx", "teamtreehouse", "datacamp",
            "academia", "goodreads", "skype", "truecaller", "bitbucket",
            "telegram", "foursquare", "yelp", "wattpad", "scribd", "flickr",
            "runkeeper", "garminconnect", "adidas", "pulsstory", "vivino",
            "babelio", "interpol", "aboutme", "inkitt", "sporttracks", "icq",
            "eyecon", "cashapp", "bluesky", "etsy", "quora", "trello", "touchtunes"
        ]

        for platform in social_priority:
            for key, value in data.items():
                if key.startswith(platform) and value is not None:
                    return value

        for value in data.values():
            if value is not None:
                return value

        return None
