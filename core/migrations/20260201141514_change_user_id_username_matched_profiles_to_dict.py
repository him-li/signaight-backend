from core.models.utils.followers_mapping import ONLINE_SIGNATURE_MAPPING
from pymongo import UpdateOne
from beanie import free_fall_migration

BATCH_SIZE = 300


def ensure_list_dict(data: dict | None) -> dict:
    result = {}
    for k, v in (data or {}).items():
        if not v:
            continue

        # already list
        if isinstance(v, list):
            cleaned = [item for item in v if item]
            if cleaned:
                result[k] = cleaned
            continue

        # single value → wrap
        result[k] = [v]

    return result


def extract_first(data: dict | None) -> dict:
    result = {}
    for k, v in (data or {}).items():
        if isinstance(v, list) and v:
            result[k] = v[0]
        elif isinstance(v, str):
            result[k] = v
    return result


class Forward:
    use_transaction = False

    @free_fall_migration(document_models=[])
    async def migrate_uid_uname_url_mp_primary_to_dict(self, session):

        db = session.client.get_default_database()
        bulk_ops = []
        persons_batch = []

        async for person in db.persons.find({}):

            persons_batch.append(person)

            if len(persons_batch) >= BATCH_SIZE:
                await process_batch(db, persons_batch, bulk_ops)
                persons_batch = []

        if persons_batch:
            await process_batch(db, persons_batch, bulk_ops)

        if bulk_ops:
            await db.persons.bulk_write(bulk_ops)


async def process_batch(db, persons_batch, bulk_ops):

    # collect candidate ids needed in this batch
    candidate_ids = set()

    for person in persons_batch:
        mp = (person.get("network_signature") or {}).get("matched_profiles") or {}
        for value in mp.values():
            if not isinstance(value, dict):
                continue
            primary = value.get("primary_candidate")
            if primary and not isinstance(primary, dict):
                candidate_ids.add(primary)

    for person in persons_batch:

        network_signature = person.get("network_signature") or {}
        if not network_signature:
            continue

        user_id = ensure_list_dict(network_signature.get("user_id"))
        username = ensure_list_dict(network_signature.get("username"))
        url = ensure_list_dict(network_signature.get("url"))

        matched_profiles = network_signature.get("matched_profiles") or {}
        new_mp = {}

        for key, value in matched_profiles.items():
            if not isinstance(value, dict):
                continue
            primary_candidate = value.get("primary_candidate")
            candidates_count = value.get("candidates_count")
            if not primary_candidate and not candidates_count:
                continue
            
            if not primary_candidate:
                new_mp[key] = {
                    **value,
                    "primary_candidate": None,
                }
                continue

            candidate_model = await db.candidates.find_one(
                {"_id": primary_candidate},
            )

            if not candidate_model:
                continue

            candidate_info = extract_candidate_info(candidate_model, person)

            new_mp[key] = {
                **value,
                "primary_candidate": {str(primary_candidate): candidate_info},
            }

        _set = {
            "network_signature": {
                **network_signature,
                "user_id": user_id,
                "username": username,
                "url": url,
                "matched_profiles": new_mp,
            }
        }

        bulk_ops.append(UpdateOne({"_id": person["_id"]}, {"$set": _set}, upsert=False))

    if bulk_ops:
        print(
            f"Processing batch of {len(persons_batch)} persons with {len(bulk_ops)} updates..."
        )
        await db.persons.bulk_write(bulk_ops)
        bulk_ops.clear()

    class Backward:

        @free_fall_migration(document_models=[])
        async def migrate_uid_uname_url_mp_primary_to_single_entity(self, session):

            db = session.client.get_default_database()
            bulk_ops = []

            async for person in db.persons.find({}):

                network_signature = person.get("network_signature") or {}
                if not network_signature:
                    continue

                user_id = extract_first(network_signature.get("user_id"))
                username = extract_first(network_signature.get("username"))
                url = extract_first(network_signature.get("url"))
                m_prof = network_signature.get("matched_profiles") or {}

                matched_profiles = {}

                for key, value in m_prof.items():
                    if not isinstance(value, dict):
                        continue
                   
                    primary_raw = value.get("primary_candidate") or {}
                    primary_id = next(iter(primary_raw), None)

                    matched_profiles[key] = {
                        "primary_candidate": primary_id,
                        "candidates_count": value.get("candidates_count", 0),
                    }

                _set = {
                    "network_signature": {
                        **network_signature,
                        "user_id": user_id,
                        "username": username,
                        "url": url,
                        "matched_profiles": matched_profiles,
                    }
                }

                bulk_ops.append(
                    UpdateOne(
                        {"_id": person["_id"]},
                        {"$set": _set},
                        upsert=False,
                    )
                )

                if len(bulk_ops) >= BATCH_SIZE:
                    await db.persons.bulk_write(bulk_ops)
                    bulk_ops = []

            if bulk_ops:
                await db.persons.bulk_write(bulk_ops)
                
def extract_bio_from_biographic_details(candidate: dict, source:str):
    if not candidate:
        return None

    biographic_details = candidate.get("biographic_details") or {}
    bio_intro = biographic_details.get("description_bio_intro") or {}

    if not bio_intro:
        return None

    # --- Special cases ---

    if source == "twitter":
        twitter_desc = bio_intro.get("twitter_description") or {}
        return twitter_desc.get("description_text")

    if source == "facebook":
        fb_intro = bio_intro.get("fb_profile_intro") or {}
        return fb_intro.get("fb_profile_intro_text")

    if source == "linkedin":
        return (
            bio_intro.get("linkedin_profile_description")
            or bio_intro.get("linkedin_headline")
        )

    # --- Generic ---
    return bio_intro.get(f"{source}_bio")


def _extract_online_counts(candidate: dict, source:str) -> dict:
    network_signature = candidate.get("network_signature") or {}
    online = network_signature.get("online_signature") or {}

    if not online:
        return {
            "followers": None,
            "following": None,
            "friends": None,
        }

    mapping = ONLINE_SIGNATURE_MAPPING.get(source, {})

    def get_value(field_name):
        if not field_name:
            return None
        return online.get(field_name)

    return {
        "followers": get_value(mapping.get("followers")),
        "following": get_value(mapping.get("following")),
        "friends": get_value(mapping.get("friends")),
    }


def extract_candidate_info(candidate: dict, person: dict = {}) -> dict:
    if not candidate:
        return {}

    source = candidate.get("source")
    counts = _extract_online_counts(person, source)
    bio = extract_bio_from_biographic_details(person, source)

    personal_details = candidate.get("personal_details") or {}
    network_signature = candidate.get("network_signature") or {}

    def deep_get(obj: dict, *keys):
        """Safely get nested dict value."""
        for key in keys:
            if not isinstance(obj, dict):
                return None
            obj = obj.get(key)
        return obj

    return {
        "f_name": deep_get(personal_details, "name", "first_name", f"{source}_f_name"),
        "l_name": deep_get(personal_details, "name", "last_name", f"{source}_l_name"),
        "full_name": deep_get(
            personal_details, "name", "full_name", f"{source}_full_name"
        ),
        "profile_id": deep_get(network_signature, "user_id", f"{source}_user_id"),
        "profile_url": deep_get(network_signature, "url", f"{source}_profile_url"),
        "profile_username": deep_get(
            network_signature, "username", f"{source}_username"
        ),
        "profile_picture": deep_get(
            personal_details, "visuals", "profile_photo", f"{source}_profile_picture"
        ),
        "creation_date": deep_get(network_signature, "misc", f"{source}_creation_date"),
        "location": deep_get(personal_details, "location", f"{source}_location"),
        "birthdate": deep_get(
            personal_details,
            "birth_year_birthday",
            "birthday",
            f"{source}_birthdate",
        ),
        "followers": counts.get("followers") if counts else None,
        "following": counts.get("following") if counts else None,
        "friends": counts.get("friends") if counts else None,
        "bio": bio,
    }
