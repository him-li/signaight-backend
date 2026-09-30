from mergedeep import merge, Strategy
from beanie.operators import In
from bson.dbref import DBRef
from typing import List
from uuid import UUID
from core.models import CandidateModel, PersonModel
from core.models.network_signature import NetworkSignature

def merge_candidate_data(existing: dict, new: dict):
    for key, value in new.items():

        if value is None:
            continue

        # LISTS (safe merge)
        if isinstance(value, list):
            existing_value = existing.get(key)

            if not isinstance(existing_value, list):
                existing_value = [] if existing_value is None else [existing_value]

            existing[key] = list(set(existing_value + value))
            continue

        # NUMBERS (sum)
        if isinstance(value, (int, float)):
            existing[key] = (existing.get(key) or 0) + value
            continue

        # STRINGS / OTHER
        if not existing.get(key):
            existing[key] = value

def _normalize_urls(urls):
    if not urls:
        return []
    if isinstance(urls, str):
        return [urls]
    return urls


def merge_matched_profiles(persons):
    merged_profiles = {}

    dedup = {}  # {platform: {"ids": set(), "urls": set()}}

    for person in persons:
        profiles = (
            person.network_signature.matched_profiles.model_dump()
            if person.network_signature
            and person.network_signature.matched_profiles
            else {}
        )

        if not profiles:
            continue

        if not isinstance(profiles, dict):
            profiles = profiles.model_dump()

        for platform, data in profiles.items():
            if not data:
                continue

            primary_candidates = data.get("primary_candidate", {})
            if not primary_candidates:
                continue

            if platform not in merged_profiles:
                merged_profiles[platform] = {
                    "candidates_count": 0,
                    "primary_candidate": {},
                }

            if platform not in dedup:
                dedup[platform] = {"ids": set(), "urls": set()}

            for candidate_id, candidate in primary_candidates.items():
                if not candidate:
                    continue

                profile_id = candidate.get("profile_id")
                profile_urls = _normalize_urls(candidate.get("profile_url"))

                already_seen = False

                if profile_id and profile_id in dedup[platform]["ids"]:
                    already_seen = True

                if any(url in dedup[platform]["urls"] for url in profile_urls):
                    already_seen = True

                if already_seen:
                    # find existing candidate and merge into it
                    for existing in merged_profiles[platform]["primary_candidate"].values():

                        same_id = profile_id and existing.get("profile_id") == profile_id
                        same_url = any(
                            url in (existing.get("profile_url") or [])
                            for url in profile_urls
                        )

                        if same_id or same_url:
                            merge_candidate_data(existing, candidate)
                            break

                    continue

                # mark as seen
                if profile_id:
                    dedup[platform]["ids"].add(profile_id)

                for url in profile_urls:
                    dedup[platform]["urls"].add(url)

                # merge ONLY unique candidates
                merge(
                    merged_profiles[platform]["primary_candidate"],
                    {candidate_id: candidate},
                    strategy=Strategy.ADDITIVE,
                )

            # sum counts (optional: you may want unique count instead)
            merged_profiles[platform]["candidates_count"] += data.get(
                "candidates_count", 0
            )

    return merged_profiles


async def reassign_candidates_to_merged_person(
    source_person_ids: List[UUID],
    merged_person: PersonModel,
    session=None,
):
    person_ref = DBRef("persons", merged_person.id)
    result = await CandidateModel.find(
        In(CandidateModel.person.id, source_person_ids),
        session=session,
    ).update_many(
        {
            "$set": {
                "person": person_ref,
            }
        }
    )
    
    persons = await PersonModel.find(
        In(PersonModel.id, source_person_ids)
    ).to_list()

    merged_profiles = merge_matched_profiles(persons)

    if not merged_person.network_signature:
        merged_person.network_signature = NetworkSignature()

    merged_person.network_signature.matched_profiles = merged_profiles

    await merged_person.save_changes(session=session)
    
    print(
        f"Reassigned {result.modified_count} candidates "
        f"to merged person {merged_person.id}"
    )
