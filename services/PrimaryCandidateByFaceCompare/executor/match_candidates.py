from datetime import datetime, date
import decimal
import enum
from pathlib import PurePath
from core.dotty_dictionary import dotty
from typing import List, Dict, Mapping, Sequence
import uuid

from core.clients.ds_app import api as ds_app_api
from core.logging import logger
from core.models import PersonModel, CandidateModel
from core.utils.urn import build_person_urn

from collections.abc import Mapping, Sequence
from typing import Any


def remove_none_recursive(obj: Any, seen=None) -> Any:
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return None
    seen.add(obj_id)

    # Handle primitives
    if isinstance(obj, (str, int, float, bool)):
        return obj

    # Handle UUIDs, paths, datetimes, decimals
    if isinstance(obj, (uuid.UUID, PurePath, datetime, date, decimal.Decimal)):
        return str(obj)

    # Handle Enums
    if isinstance(obj, enum.Enum):
        return obj.value

    # Handle custom types like S3Path
    if hasattr(obj, "__str__") and obj.__class__.__name__ in {
        "S3Path",
        "RecruitingSource",
    }:
        return str(obj)

    # Handle mappings (dict-like)
    if isinstance(obj, Mapping):
        return {
            k: remove_none_recursive(v, seen.copy())
            for k, v in obj.items()
            if v is not None
        }

    # Handle sequences (list-like)
    if isinstance(obj, Sequence) and not isinstance(obj, str):
        return [remove_none_recursive(v, seen.copy()) for
                v in obj if v is not None]

    # Fallback for other objects
    return str(obj)


async def match_candidates(
    person: PersonModel, candidates: List[CandidateModel], service: str
) -> Dict[str, any]:
    if candidates:
        try:
            person_request = build_person_request(person)
            candidates_request = build_candidates_request(candidates)
            req_body = {
                "person": person_request,
                "candidates": candidates_request,
                "service": service,
                "hash": str(person.id) + service,
            }
            ds_response = await ds_app_api.async_ds_request.match_candidates(
                body=req_body,
                headers={"x-remote-context": build_person_urn(person.id)},
            )
            matched_id = next(
                (
                    item["id"]
                    for item in ds_response.body.get("candidates")
                    if item["match"] is True
                ),
                None,
            )
            if matched_id:
                matched_candidate = next(
                    (c for c in candidates_request if c["id"] == matched_id), None
                )
                if matched_candidate:
                    matched_candidate = dotty(matched_candidate)
                    return matched_candidate
        except Exception as e:
            logger.error(e)
        return None
    return None


def build_candidates_request(candidates: List[CandidateModel]):
    return [
        {
            "data": remove_none_recursive(
                c.model_dump(
                    exclude_unset=True,
                    exclude={"person": ..., "personal_details": {"email"}},
                )
            ),
            "id": str(c.id),
        }
        for c in candidates
    ]


def build_person_request(person: PersonModel):
    clean_dict = remove_none_recursive(
        person.model_dump(exclude_unset=True, exclude={"person"})
    )
    return {"data": clean_dict, "id": str(person.id)}
