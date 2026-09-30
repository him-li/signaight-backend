import uuid
import pendulum
import asyncio
from core.utils.image_utils import compare_images_with_cache, get_image_quality_cached
from jina import Executor, requests
from docarray import DocList
from typing import Dict, List
from core.clients.ds_app import api as ds_app_api
from core.documents import (
    EnrichRequestDoc,
    EnrichResponseDoc
)
from core.dotty_dictionary import dotty
from core.database import init_db
from core.logging import logger
from core.storage import init_storage
from core.models import CandidateModel, PersonModel
from core.utils import (
    parse_urn,
    SignAIghtURN,
    build_person_urn,
    check_urn_resource,
)

from core.models.utils import post_service_log
from services.PrimaryCandidateByFaceCompare.executor import compare_names
from services.PrimaryCandidateByFaceCompare.executor.constants import ALLOWED_EXTENSIONS, MIN_FACE_QUALITY, MIN_FACE_SIMILARITY, SUPPORTED_SERVICES
from core.utils.get_names_list import name_resolution



class PrimaryCandidateByFaceCompare(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        init_storage()
        # NOTE: run async init db in sync init
        # syncify function from asyncer work only in anyio loops
        # which not compatibel with jina
        loop = asyncio.get_event_loop()
        task = loop.create_task(init_db())
        if not loop.is_running():
            loop.run_until_complete(task)

    @requests(on='/enrich')
    async def compare_candidate_faces(
        self,
        docs: DocList[EnrichRequestDoc],
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
                        executor="PrimaryCandidateByFaceCompare",
                        search_step="enrich",
                        message="Initiated",
                        docs_count=len(docs),
                        step_point="entry"
                    )
                except Exception as e:
                    logger.error(f"Unable to send service log: {str(e)}")
        _docs = DocList[EnrichResponseDoc]()
        flow_step = parameters.get('flow_step')
        if (flow_step == 'linkage_accuracy_compare'):
            _docs = await self.linkage_accuracy_compare(docs)
        else:
            for doc in docs:
                source_photo = None
                person_id = parse_urn(doc.urn)
                self.logger.info(f"PrimaryCandidateByFaceCompare /enrich "
                                 f"id:{doc.search_id} urn:{doc.urn}")
                urn_resource = check_urn_resource(doc.urn)
                if not urn_resource == 'persons':
                    continue
                person = await PersonModel.get(person_id)
                person_dict = dotty(person.model_dump())
                try:
                    profile_photo = person.personal_details.visuals.profile_photo
                    destinations = [
                        picture for picture in profile_photo.model_dump().values()
                        if picture]
                    data = {
                        "destination": [str(p) for p in destinations]
                    }
                    try:
                        logger.info(f"Image quality for {data}")
                        response = await get_image_quality_cached(
                            data,
                            headers={
                                'x-remote-context': build_person_urn(person_id)
                            }
                        )
                        logger.info(response)
                        sorted_pics_by_quality = sorted(
                            response.items(),
                            key=lambda x: (
                                x[1].get('scores', {}).get('face_score', -1),
                                x[1].get('scores', {}).get(
                                    'artifact_score', -1)
                            ),
                            reverse=True
                        )
                        logger.info(sorted_pics_by_quality)
                        pic, metadata = sorted_pics_by_quality[0]
                        quality = metadata.get(
                            'scores', {}).get('face_score', -1)

                        if pic and quality >= MIN_FACE_QUALITY:
                            source_photo = pic
                        else:
                            source_photo = (person.personal_details.visuals.
                                            profile_photo.profile_picture)
                    except Exception:
                        linkedin_photo = (person.personal_details.visuals.
                                          profile_photo.linkedin_profile_picture)
                        if linkedin_photo:
                            source_photo = linkedin_photo
                        else:
                            source_photo = (person.personal_details.visuals.
                                            profile_photo.profile_picture)
                except Exception:
                    self.logger.info(
                        "Unable to get photo for person {}. "
                        "Ommiting compare".format(
                            person_dict.get(
                                "personal_details.name.full_name.full_name")
                        ))
                    continue
                if not source_photo:
                    self.logger.info(
                        "No source photo for person {}. Ommiting compare".format(
                            person_dict.get(
                                "personal_details.name.full_name.full_name")
                        ))
                self.logger.info("{} - {}".format(
                    person_dict.get(
                        "personal_details.name.full_name.full_name"),
                    person_dict.get("personal_details.visuals.profile_photo")
                ))
                primary_candidates = await CandidateModel.find(
                            CandidateModel.primary == True,  # noqa
                            CandidateModel.person.id == uuid.UUID(person_id),
                            CandidateModel.search_id == doc.search_id,
                        ).to_list()
                for service in SUPPORTED_SERVICES:
                    try:
                        if person_dict.get(f"network_signature.matched_profiles.{service}.primary_candidate"):
                            logger.info(
                                f"Skipping compare for {service} - primary already exists"
                            )
                            continue

                    except Exception:
                        pass
                    try:
                        print(f"Processing service: {service} for person {person_id}", person_dict.get(
                            f"network_signature.matched_profiles.{service}"), person_dict.get(f"network_signature.matched_profiles.{service}.primary_candidate"))
                        candidates = await CandidateModel.find(
                            CandidateModel.search_id == doc.search_id,
                            CandidateModel.source == service,
                            CandidateModel.person.id == uuid.UUID(person_id),
                            CandidateModel.primary == False,
                            fetch_links=True,
                        ).to_list()
                        if not candidates:
                            continue
                        await self._ds_filter_candidates(person_dict.to_dict(),
                                                         candidates)
                    except Exception as e:
                        logger.error(
                            f"Unable to get proper {service} candidates for person"
                            f"{str(person_id)} Error: {str(e)}")
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="PrimaryCandidateByFaceCompare",
                            search_step="enrich",
                            message=(f"Error during getting {service} "
                                     f"candidates: {str(e)}"),
                            docs_count=1,
                            step_point="error"
                        )
                        continue

                    try:
                        match service:
                            case "facebook":
                                same_l_name_candidates = [
                                    candidate
                                    for candidate in candidates
                                    if candidate.resource != "grayfox"
                                    and candidate.personal_details.name.full_name.facebook_full_name
                                    and (
                                        candidate.personal_details.name.last_name.l_name.lower()
                                    )
                                    in (
                                        candidate.personal_details.name.full_name.facebook_full_name.lower()
                                    )
                                ]
                            case "instagram":
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    candidate.personal_details.name.full_name.
                                    instagram_full_name and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                     instagram_full_name.lower())]
                            case "twitter":
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    candidate.personal_details.name.full_name.
                                    twitter_full_name and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                     twitter_full_name.lower())]
                            case 'xing':
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    (candidate.personal_details.name.full_name.
                                        xing_full_name) and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                        xing_full_name.lower())]
                            case 'eumw':
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    (candidate.personal_details.name.full_name.
                                        eumw_full_name) and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                        eumw_full_name.lower())]
                            case 'interpol':
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    (candidate.personal_details.name.full_name.
                                        interpol_full_name) and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                        interpol_full_name.lower())]
                            case 'linkedin':
                                same_l_name_candidates = [
                                    candidate for candidate in candidates if
                                    (candidate.personal_details.name.full_name.
                                        linkedin_full_name) and
                                    (candidate.personal_details.name.last_name.
                                     l_name.lower()) in
                                    (candidate.personal_details.name.full_name.
                                        linkedin_full_name.lower())]
                            case _:
                                same_l_name_candidates = candidates
                    except Exception:
                        same_l_name_candidates = candidates

                    if not same_l_name_candidates:
                        same_l_name_candidates = candidates
                    pic_similarity_dict = None
                    chosen_pics = None
                    chosen_similarities = None
                    pic_similarity_dict = None
                    if source_photo:
                        similarity_dict = await self._check_similarity(
                            person_id,
                            same_l_name_candidates,
                            service,
                            source_photo)
                        chosen_pics = similarity_dict.get('chosen_pics')
                        chosen_similarities = similarity_dict.get(
                            'chosen_similarities', {})
                        pic_similarity_dict = similarity_dict.get(
                            'pic_similarity_dict', {})

                    if chosen_pics:
                        _docs = await self._update_candidates(
                            candidates,
                            service,
                            chosen_pics,
                            chosen_similarities,
                            doc,
                            pic_similarity_dict,
                            _docs)
                        primary_candidates = await CandidateModel.find(
                            CandidateModel.primary == True,  # noqa
                            CandidateModel.person.id == uuid.UUID(person_id),
                            CandidateModel.search_id == doc.search_id,
                        ).to_list()

                    if not chosen_pics:
                        if primary_candidates:
                            for primary_candidate in primary_candidates:
                                if primary_candidate:
                                    candidate_source = primary_candidate.source

                                    primary_dict = dotty(
                                        primary_candidate.model_dump())

                                    source_photo = None
                                    destination_photo = primary_dict.get(
                                        f"personal_details.visuals.profile_photo.{candidate_source}_profile_picture")  # noqa
                                    data = {
                                        "destination": [str(destination_photo) if destination_photo else None]
                                    }
                                    if not destination_photo:
                                        continue
                                    try:
                                        logger.info(
                                            f"Image quality for {data}")
                                        response = await get_image_quality_cached(
                                            data,
                                            headers={
                                                'x-remote-context': build_person_urn(person_id)
                                            }
                                        )
                                        logger.info(response)
                                        sorted_pics_by_quality = sorted(
                                            response.items(),
                                            key=lambda x: (
                                                x[1].get('scores', {}).get(
                                                    'face_score', -1),
                                                x[1].get('scores', {}).get(
                                                    'artifact_score', -1)
                                            ),
                                            reverse=True
                                        )
                                        logger.info(sorted_pics_by_quality)
                                        pic, metadata = sorted_pics_by_quality[0]
                                        quality = metadata.get(
                                            'scores', {}).get('face_score', -1)

                                        if pic and quality >= MIN_FACE_QUALITY:
                                            source_photo = pic
                                        else:
                                            continue
                                    except Exception:
                                        source_photo = primary_dict.get(
                                            f"personal_details.visuals.profile_photo.{candidate_source}_profile_picture")

                                    if not source_photo:
                                        continue
                                    similarity_dict = await self._check_similarity(
                                        person_id,
                                        candidates,
                                        service,
                                        source_photo)
                                    chosen_pics = similarity_dict.get(
                                        'chosen_pics')
                                    chosen_similarities = similarity_dict.get(
                                        'chosen_similarities', {})
                                    pic_similarity_dict = similarity_dict.get(
                                        'pic_similarity_dict', {})
                                    if chosen_pics:
                                        _docs = await self._update_candidates(
                                            candidates,
                                            service,
                                            chosen_pics,
                                            chosen_similarities,
                                            doc,
                                            pic_similarity_dict,
                                            _docs)
                                        primary_candidates = await CandidateModel.find(
                                            CandidateModel.primary == True,  # noqa
                                            CandidateModel.person.id == uuid.UUID(
                                                person_id),
                                            CandidateModel.search_id == doc.search_id,
                                        ).to_list()
                                        break

                    if not chosen_pics:
                        unmapped_images = (
                            person_dict.get("personal_details", {})
                            .get("visuals", {})
                            .get("unmapped_photos")
                            or []
                        )
                        for image in unmapped_images:
                            if not image:
                                continue
                            similarity_dict = await self._check_similarity(
                                person_id,
                                candidates,
                                service,
                                image)
                            chosen_pics = similarity_dict.get('chosen_pics')
                            chosen_similarities = similarity_dict.get(
                                'chosen_similarities', {})
                            pic_similarity_dict = similarity_dict.get(
                                'pic_similarity_dict', {})
                            if chosen_pics:
                                _docs = await self._update_candidates(
                                    candidates,
                                    service,
                                    chosen_pics,
                                    chosen_similarities,
                                    doc,
                                    pic_similarity_dict,
                                    _docs)
                                primary_candidates = await CandidateModel.find(
                                    CandidateModel.primary == True,  # noqa
                                    CandidateModel.person.id == uuid.UUID(
                                        person_id),
                                    CandidateModel.search_id == doc.search_id,
                                ).to_list()
                                break

            end_time = pendulum.now()
            for i, doc in enumerate(_docs):
                if i == 0:
                    try:
                        post_service_log(
                            search_id=doc.search_id,
                            urn=doc.urn,
                            executor="PrimaryCandidateByFaceCompare",
                            search_step="enrich",
                            message="Finished in {:.2f} seconds".format(
                                end_time.int_timestamp - start_time.int_timestamp),
                            docs_count=len(_docs),
                            step_point="out",
                            step_duration_microseconds=end_time.diff(
                                start_time)._to_microseconds()
                        )
                    except Exception as e:
                        logger.error(f"Unable to send service log: {str(e)}")
        return _docs

    async def linkage_accuracy_compare(
        self,
        docs: DocList[EnrichRequestDoc]
    ):
        _docs = DocList[EnrichResponseDoc]()
        for doc in docs:
            source_photo = None
            person_id = parse_urn(doc.urn)
            self.logger.info(f"PrimaryCandidateByFaceCompare /linkage_accuracy_compare"
                             f"id:{doc.search_id} urn:{doc.urn}")
            urn_resource = check_urn_resource(doc.urn)
            if not urn_resource == 'persons':
                continue
            person = await PersonModel.get(person_id)
            person_dict = dotty(person.model_dump())
            try:
                profile_photo = person.personal_details.visuals.profile_photo
                destinations = [
                    picture for picture in profile_photo.model_dump().values()
                    if picture]
                data = {
                    "destination": [str(p) for p in destinations]
                }
                try:
                    logger.info(f"Image quality for {data}")
                    response = await get_image_quality_cached(
                        data,
                        headers={
                            'x-remote-context': build_person_urn(person_id)
                        }
                    )
                    logger.info(response)
                    sorted_pics_by_quality = sorted(
                        response.items(),
                        key=lambda x: (
                            x[1].get('scores', {}).get('face_score', -1),
                            x[1].get('scores', {}).get('artifact_score', -1)
                        ),
                        reverse=True
                    )
                    logger.info(sorted_pics_by_quality)
                    pic, metadata = sorted_pics_by_quality[0]
                    quality = metadata.get('scores', {}).get('face_score', -1)

                    if pic and quality >= MIN_FACE_QUALITY:
                        source_photo = pic
                    else:
                        source_photo = (person.personal_details.visuals.
                                        profile_photo.profile_picture)
                except Exception:
                    linkedin_photo = (person.personal_details.visuals.
                                      profile_photo.linkedin_profile_picture)
                    if linkedin_photo:
                        source_photo = linkedin_photo
                    else:
                        source_photo = (person.personal_details.visuals.
                                        profile_photo.profile_picture)
            except Exception:
                self.logger.info(
                    "Unable to get photo for person {}. "
                    "Ommiting compare".format(
                        person_dict.get(
                            "personal_details.name.full_name.full_name")
                    ))
                # continue
            self.logger.info("{} - {}".format(
                person_dict.get("personal_details.name.full_name.full_name"),
                person_dict.get("personal_details.visuals.profile_photo")
            ))
            candidates_list = []
            grouped = {}
            try:
                candidates_list = await CandidateModel.find(
                    CandidateModel.search_id == doc.search_id,
                    CandidateModel.person.id == uuid.UUID(person_id),
                    CandidateModel.primary == False,
                    fetch_links=True
                ).to_list()
            except Exception as e:
                logger.error(
                    f"Unable to get proper non primary candidates for person"
                    f"{str(person_id)} Error: {str(e)}")
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="PrimaryCandidateByFaceCompare",
                    search_step="linkage_accuracy_compare",
                    message=(f"Error during getting non primary "
                                f"candidates: {str(e)}"),
                    docs_count=1,
                    step_point="error"
                )
                continue

            for c in candidates_list:
                grouped.setdefault(c.source, []).append(c)
            for service, candidates in grouped.items():
                pic_similarity_dict = {}
                chosen_pics = []
                chosen_similarities = {}
                if source_photo:
                    similarity_dict = await self._check_similarity(
                        person_id,
                        candidates,
                        service,
                        source_photo)
                    chosen_pics = similarity_dict.get('chosen_pics') or (
                        [similarity_dict.get('chosen_pic')] if similarity_dict.get('chosen_pic') else [])
                    chosen_similarities = similarity_dict.get(
                        'chosen_similarities', {})
                    pic_similarity_dict = similarity_dict.get(
                        'pic_similarity_dict', {})
                if not chosen_pics:
                    unmapped_images = (
                        person_dict.get("personal_details", {})
                        .get("visuals", {})
                        .get("unmapped_photos")
                        or []
                    )
                    for image in unmapped_images:
                        if not image:
                            continue
                        similarity_dict = await self._check_similarity(
                            person_id,
                            candidates,
                            service,
                            image)
                        chosen_pics = similarity_dict.get('chosen_pics') or (
                            [similarity_dict.get('chosen_pic')] if similarity_dict.get('chosen_pic') else [])
                        chosen_similarities = similarity_dict.get(
                            'chosen_similarities', {})
                        chosen_pic = similarity_dict.get('chosen_pic', None)
                        pic_similarity_dict = similarity_dict.get(
                            'pic_similarity_dict', {})
                        if chosen_pics:
                            _docs = await self._update_candidates(
                                candidates,
                                service,
                                chosen_pics,
                                chosen_similarities,
                                doc,
                                pic_similarity_dict,
                                _docs)
                            primary_candidates = await CandidateModel.find(
                                CandidateModel.primary == True,  # noqa
                                CandidateModel.person.id == uuid.UUID(
                                    person_id),
                                CandidateModel.search_id == doc.search_id,
                            ).to_list()
                            break
                if not chosen_pic:
                    primary_candidates = await CandidateModel.find(
                        CandidateModel.primary == True,  # noqa
                        CandidateModel.person.id == uuid.UUID(person_id),
                        CandidateModel.search_id == doc.search_id,
                    ).to_list()
                    if primary_candidates:
                        for primary_candidate in primary_candidates:
                            if primary_candidate:
                                candidate_source = primary_candidate.source

                                primary_dict = dotty(
                                    primary_candidate.model_dump())

                                source_photo = None
                                destination_photo = primary_dict.get(
                                    f"personal_details.visuals.profile_photo.{candidate_source}_profile_picture")  # noqa
                                data = {
                                    "destination": [destination_photo if destination_photo else None]
                                }
                                if not destination_photo:
                                    continue
                                try:
                                    logger.info(f"Image quality for {data}")
                                    response = await get_image_quality_cached(
                                        data,
                                        headers={
                                            "x-remote-context": build_person_urn(
                                                person_id
                                            )
                                        },
                                    )
                                    logger.info(response)
                                    sorted_pics_by_quality = sorted(
                                        response.items(),
                                        key=lambda x: (
                                            x[1].get('scores', {}).get(
                                                'face_score', -1),
                                            x[1].get('scores', {}).get(
                                                'artifact_score', -1)
                                        ),
                                        reverse=True
                                    )
                                    logger.info(sorted_pics_by_quality)
                                    pic, metadata = sorted_pics_by_quality[0]
                                    quality = metadata.get(
                                        'scores', {}).get('face_score', -1)

                                    if pic and quality >= 0.70:
                                        source_photo = pic
                                    else:
                                        continue
                                except Exception:
                                    source_photo = primary_dict.get(
                                        f"personal_details.visuals.profile_photo.{candidate_source}_profile_picture")
                                if not source_photo:
                                    continue
                                similarity_dict = await self._check_similarity(
                                    person_id,
                                    candidates,
                                    service,
                                    source_photo)
                                chosen_pics = similarity_dict.get('chosen_pics') or (
                                    [similarity_dict.get('chosen_pic')] if similarity_dict.get('chosen_pic') else [])
                                chosen_similarities = similarity_dict.get(
                                    'chosen_similarities', {})
                                chosen_pic = similarity_dict.get(
                                    'chosen_pic', None)
                                pic_similarity_dict = similarity_dict.get(
                                    'pic_similarity_dict', {})
                                if chosen_pics:
                                    break
                normalized_person_name = await name_resolution(person_dict)
                for candidate in candidates:
                    candidate_dict = dotty(candidate.model_dump())
                    candidate_name = candidate_dict.get(
                        f"personal_details.name.full_name.{service}_full_name")
                    first_part = "tgm" if service == "telegram" else service
                    candidate_name = (
                        candidate_name if candidate_name else
                        (f"{candidate_dict.get(f'personal_details.name.first_name.{first_part}_f_name')} {candidate_dict.get(f'personal_details.name.last_name.{first_part}_l_name')}") if
                        candidate_dict.get(f'personal_details.name.last_name.{first_part}_l_name') else '')
                    is_matched_names, ratio = compare_names.compare_names_data(
                        normalized_person_name, candidate_name if candidate_name else '')
                    print('email--name-matched', normalized_person_name,
                          candidate_name, is_matched_names, ratio)
                    if chosen_pics:
                        _docs = await self._update_candidates(
                            candidates,
                            service,
                            chosen_pics,
                            chosen_similarities,
                            doc,
                            pic_similarity_dict,
                            _docs)
                    if is_matched_names:
                        candidate = await self._set_primary_candidate(
                            candidate,
                            chosen_similarity=ratio)
                        if service == 'facebook':
                            await self._build_response_docs(
                                candidate,
                                doc,
                                service,
                                _docs
                            )
        return _docs

    async def _check_similarity(self,
                                person_id,
                                candidates: List[CandidateModel],
                                service,
                                source_photo):
        id_pic_dict = {}
        for candidate in candidates:
            match service:
                case "facebook":
                    try:
                        dest_pic = (
                            candidate.personal_details.visuals.profile_photo.facebook_profile_picture
                        )
                    except Exception:
                        dest_pic = None
                case "instagram":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                instagram_profile_picture)
                case "twitter":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                twitter_profile_picture)
                case "xing":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                xing_profile_picture)
                case "eumw":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                eumw_profile_picture)
                case "interpol":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                interpol_profile_picture)
                case "linkedin":
                    try:
                        dest_pic = (candidate.personal_details.
                                    visuals.profile_photo.
                                    linkedin_profile_picture)
                    except Exception:
                        dest_pic = None
                case _:
                    continue
            try:
                ext = str(dest_pic).split(".")[-1]
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    continue
            except Exception:
                continue
            id_pic_dict[candidate.id] = dest_pic
        destinations = [str(destination) for destination in
                        id_pic_dict.values() if destination]
        if not destinations:
            self.logger.info(f"Compare result {service}: Destination list is empty. Skip compare action")  # noqa
            similarity_dict = {}
            return similarity_dict
        data = {
            "source": str(source_photo),
            "destination": destinations
        }
        chosen_pics = []
        chosen_similarities = {}
        try:
            self.logger.info(f"Compare result {service}")
            self.logger.info(
                f"source: {data.get('source')}, destinations: {data.get('destination')}")
            response = await compare_images_with_cache(
                data,
                headers={
                    'x-remote-context': build_person_urn(person_id)
                }
            )
            pic_similarity_dict = response.get(
                'sorted', {}) if isinstance(response, dict) else {}
            # collect all destination images with similarity above threshold
            try:
                for image, sim in pic_similarity_dict.items():
                    try:
                        similarity_value = float(sim)
                    except Exception:
                        # if sim is a dict like { 'similarity': value }
                        similarity_value = pic_similarity_dict.get(
                            image, {}).get('similarity', -1)
                    if similarity_value >= MIN_FACE_SIMILARITY:
                        chosen_pics.append(image)
                        chosen_similarities[image] = similarity_value
            except Exception:
                chosen_pics = []
                chosen_similarities = {}
        except Exception as e:
            self.logger.error(f'Compare finished with error {str(e)}')
            pic_similarity_dict = {}

        similarity_dict = {
            "pic_similarity_dict": pic_similarity_dict,
            "chosen_pics": chosen_pics,
            "chosen_similarities": chosen_similarities,
        }

        return similarity_dict

    async def _update_candidates(self,
                                 candidates: List[CandidateModel],
                                 service,
                                 chosen_pics,
                                 chosen_similarities,
                                 doc,
                                 pic_similarity_dict,
                                 _docs):
        # chosen_pics: list of destination image urls selected by similarity
        # chosen_similarities: mapping dest -> similarity value
        for candidate in candidates:
            match service:
                case "facebook":
                    dest_pic = (
                        candidate.personal_details.visuals.profile_photo.facebook_profile_picture
                    )
                case "instagram":
                    dest_pic = (candidate.personal_details.visuals.
                                profile_photo.
                                instagram_profile_picture)
                case "twitter":
                    dest_pic = (candidate.personal_details.visuals.
                                profile_photo.
                                twitter_profile_picture)
                case "xing":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                xing_profile_picture)
                case "eumw":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                eumw_profile_picture)
                case "interpol":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                interpol_profile_picture)
                case "linkedin":
                    dest_pic = (candidate.personal_details.
                                visuals.profile_photo.
                                linkedin_profile_picture)
                case _:
                    break
                    # profile_photo = dotty(candidate.personal_details.
                    #             visuals.profile_photo.model_dump())
                    # dest_pic = profile_photo.get(f"{service}_profile_picture", "")
            try:
                dest_str = str(dest_pic)
            except Exception:
                dest_str = None
            if chosen_pics and dest_str and any(dest_str == str(cp) for cp in chosen_pics):
                # get similarity value: prefer chosen_similarities then pic_similarity_dict
                similarity_value = chosen_similarities.get(
                    dest_str, pic_similarity_dict.get(dest_pic, {}).get('similarity', -1))
                candidate = await self._set_primary_candidate(
                    candidate,
                    similarity_value)
                candidate_dict = dotty(candidate.model_dump())
                await self._build_response_docs(
                    candidate,
                    doc,
                    service,
                    _docs
                )
                self.logger.info("{} - {}".format(
                    candidate_dict.get(
                        'personal_details.name.full_name.full_name'),
                    candidate_dict.get(
                        'personal_details.visuals.profile_photo')
                ))
            else:
                candidate.similarity = pic_similarity_dict.get(
                    dest_pic, {}).get('similarity', -1)
                await candidate.replace()
        return _docs

    async def _set_primary_candidate(self,
                                     candidate: CandidateModel,
                                     chosen_similarity):
        candidate.similarity = chosen_similarity
        candidate.primary = True
        candidate.ds_filter = True
        candidate = await candidate.save()
        return candidate

    async def _build_response_docs(self, candidate, doc, service, _docs):
        candidate_dict = dotty(candidate.model_dump())
        candidate_dict['urn'] = SignAIghtURN.build('candidates',
                                                 candidate.id)
        candidate_dict['search_id'] = doc.search_id
        candidate_dict['source'] = service
        match service:
            case "facebook":
                _docs.append(EnrichResponseDoc(**candidate_dict.to_dict()))
            case "instagram":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict()))
            case "twitter":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict()))
            case "xing":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict())
                )
            case "eumw":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict())
                )
            case "interpol":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict())
                )
            case "linkedin":
                _docs.append(
                    EnrichResponseDoc(**candidate_dict.to_dict())
                )
            case _:
                pass

        return _docs

    async def _ds_filter_candidates(self,
                                    person_dict,
                                    candidates: List[CandidateModel]):
        candidates_list = []
        for candidate in candidates:
            id = candidate.id
            name = candidate.personal_details.name
            visuals = candidate.personal_details.visuals
            match candidate.source:
                case "facebook":
                    profile_name = (
                        name.full_name.facebook_full_name
                        if name.full_name.facebook_full_name
                        else (
                            name.first_name.facebook_f_name
                            + name.last_name.facebook_l_name
                            if name.first_name.facebook_f_name
                            and name.last_name.facebook_l_name
                            else None
                        )
                    )
                    profile_picture = (
                        visuals.profile_photo.facebook_profile_picture
                        if visuals
                        else None
                    )
                case 'instagram':
                    profile_name = (
                        name.full_name.instagram_full_name if
                        name.full_name.instagram_full_name else None)
                    profile_picture = (
                        visuals.profile_photo.instagram_profile_picture if
                        visuals else None)
                case 'twitter':
                    profile_name = (
                        name.full_name.twitter_full_name if
                        name.full_name.twitter_full_name else None)
                    profile_picture = (
                        visuals.profile_photo.twitter_profile_picture if
                        visuals else None)
                case 'xing':
                    profile_name = (
                        name.full_name.xing_full_name if
                        name.full_name.xing_full_name else None)
                    profile_picture = (
                        visuals.profile_photo.xing_profile_picture if
                        visuals else None)
                case 'eumw':
                    profile_name = (
                        name.full_name.eumw_full_name if
                        name.full_name.eumw_full_name else None)
                    profile_picture = (
                        visuals.profile_photo.eumw_profile_picture if
                        visuals else None)
                case 'interpol':
                    profile_name = (
                        name.full_name.interpol_full_name if
                        name.full_name.interpol_full_name else
                        name.first_name.interpol_f_name +
                        name.last_name.interpol_l_name if
                        name.first_name.interpol_f_name and
                        name.last_name.interpol_l_name else None)
                    profile_picture = (
                        visuals.profile_photo.interpol_profile_picture if
                        visuals else None)
                case 'linkedin':
                    profile_name = (
                        name.full_name.linkedin_full_name if
                        name.full_name.linkedin_full_name else
                        name.first_name.linkedin_f_name +
                        name.last_name.linkedin_l_name if
                        name.first_name.linkedin_f_name and
                        name.last_name.linkedin_l_name else None)
                    profile_picture = (
                        visuals.profile_photo.linkedin_profile_picture if
                        visuals else None)
                case _:
                    profile_name = None
                    profile_picture = None
            req_dict = {
                "id": str(id),
                "profile_name": profile_name,
                "profile_picture": str(profile_picture)
            }
            if (profile_name or
                    (profile_picture and str(profile_picture).startswith('s3://'))):
                candidates_list.append(req_dict)

        if candidates_list:
            req_body = {
                "hash": str(person_dict),
                "person": person_dict,
                "candidates": candidates_list
            }
            ds_response = ds_app_api.ds_request.filter_candidates(
                body=req_body,
                headers={'x-remote-context': person_dict.get('id', None)}
            )
            res_body = ds_response.body
            filtered_candidates = res_body.get("candidates", [])
            for candidate in filtered_candidates:
                if candidate.get("keep"):
                    candidate_model = await CandidateModel.find_one(
                        CandidateModel.id == uuid.UUID(candidate.get("id")))
                    if candidate_model:
                        candidate_model.ds_filter = True
                        await candidate_model.save()
