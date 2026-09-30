from pymongo import UpdateOne
from beanie import free_fall_migration

BATCH_SIZE = 300


def ensure_list_dict(data: dict | None) -> dict:
    """
    Convert values to list form safely:
    - string -> [string]
    - list -> cleaned list
    - None -> skipped
    """
    result = {}
    for k, v in (data or {}).items():
        if not v:
            continue

        if isinstance(v, list):
            cleaned = [item for item in v if item]
            if cleaned:
                result[k] = cleaned
            continue

        result[k] = [v]

    return result


def extract_first(data: dict | None) -> dict:
    """
    Convert list values back to single value.
    """
    result = {}
    for k, v in (data or {}).items():
        if isinstance(v, list) and v:
            result[k] = v[0]
        elif isinstance(v, str):
            result[k] = v
    return result


# =========================================
# FORWARD
# =========================================

class Forward:
    use_transaction = False

    @free_fall_migration(document_models=[])
    async def migrate_candidates_uid_uname_url_to_list(self, session):

        db = session.client.get_default_database()
        bulk_ops = []
        batch = []

        async for candidate in db.candidates.find({}):
            batch.append(candidate)

            if len(batch) >= BATCH_SIZE:
                await process_candidates_batch(db, batch, bulk_ops)
                batch = []

        if batch:
            await process_candidates_batch(db, batch, bulk_ops)

        if bulk_ops:
            await db.candidates.bulk_write(bulk_ops)


async def process_candidates_batch(db, candidates_batch, bulk_ops):

    for candidate in candidates_batch:

        network_signature = candidate.get("network_signature") or {}
        if not isinstance(network_signature, dict):
            continue

        user_id = ensure_list_dict(network_signature.get("user_id"))
        username = ensure_list_dict(network_signature.get("username"))
        url = ensure_list_dict(network_signature.get("url"))

        # Skip if nothing changed (idempotent behavior)
        if (
            user_id == network_signature.get("user_id")
            and username == network_signature.get("username")
            and url == network_signature.get("url")
        ):
            continue

        _set = {
            "network_signature": {
                **network_signature,
                "user_id": user_id,
                "username": username,
                "url": url,
            }
        }

        bulk_ops.append(
            UpdateOne(
                {"_id": candidate["_id"]},
                {"$set": _set},
                upsert=False,
            )
        )

    if bulk_ops:
        print(f"[Candidates] Batch size={len(candidates_batch)}, updates={len(bulk_ops)}")
        await db.candidates.bulk_write(bulk_ops)
        bulk_ops.clear()


# =========================================
# BACKWARD
# =========================================

class Backward:
    use_transaction = False

    @free_fall_migration(document_models=[])
    async def revert_candidates_uid_uname_url_to_single(self, session):

        db = session.client.get_default_database()
        bulk_ops = []

        async for candidate in db.candidates.find({}):

            network_signature = candidate.get("network_signature") or {}
            if not isinstance(network_signature, dict):
                continue

            user_id = extract_first(network_signature.get("user_id"))
            username = extract_first(network_signature.get("username"))
            url = extract_first(network_signature.get("url"))

            _set = {
                "network_signature": {
                    **network_signature,
                    "user_id": user_id,
                    "username": username,
                    "url": url,
                }
            }

            bulk_ops.append(
                UpdateOne(
                    {"_id": candidate["_id"]},
                    {"$set": _set},
                    upsert=False,
                )
            )

            if len(bulk_ops) >= BATCH_SIZE:
                await db.candidates.bulk_write(bulk_ops)
                bulk_ops = []

        if bulk_ops:
            await db.candidates.bulk_write(bulk_ops)
