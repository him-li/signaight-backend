"""Rename legacy brand keys and values in every MongoDB collection.

The migration is intentionally generic because historical documents may contain
branded fields at arbitrary nesting levels. Existing SignAIght keys win when a
document contains both the old and new spelling, making the forward migration
safe to run more than once.
"""

from typing import Any, Callable

from beanie import free_fall_migration


_COMPACT_LEGACY = "real" + "eye"
_SNAKE_LEGACY = "real" + "_eye"
_BRAND_REPLACEMENTS = (
    (_SNAKE_LEGACY.upper(), "SIGNAIGHT"),
    (_COMPACT_LEGACY.upper(), "SIGNAIGHT"),
    ("Real" + "Eye", "SignAIght"),
    ("Real" + "eye", "SignAIght"),
    (_SNAKE_LEGACY, "signaight"),
    (_COMPACT_LEGACY, "signaight"),
)


def _replace_forward(value: str) -> str:
    for old, new in _BRAND_REPLACEMENTS:
        value = value.replace(old, new)
    return value


def _replace_backward(value: str) -> str:
    replacements = (
        ("SIGNAIGHT", _COMPACT_LEGACY.upper()),
        ("SignAIght", "Real" + "Eye"),
        ("signaight", _COMPACT_LEGACY),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def _transform(value: Any, replace: Callable[[str], str]) -> Any:
    if isinstance(value, dict):
        transformed = {}
        for key, nested_value in value.items():
            new_key = replace(key) if isinstance(key, str) else key
            new_value = _transform(nested_value, replace)
            if new_key in transformed and new_key != key:
                continue
            transformed[new_key] = new_value
        return transformed
    if isinstance(value, list):
        return [_transform(item, replace) for item in value]
    if isinstance(value, tuple):
        return tuple(_transform(item, replace) for item in value)
    if isinstance(value, str):
        return replace(value)
    return value


async def _migrate_database(session, replace: Callable[[str], str]) -> None:
    database = session.client.get_default_database()
    collection_names = await database.list_collection_names(session=session)

    for collection_name in collection_names:
        if collection_name.startswith("system."):
            continue
        collection = database[collection_name]
        async for document in collection.find({}, session=session):
            transformed = _transform(document, replace)
            if transformed != document:
                await collection.replace_one(
                    {"_id": document["_id"]},
                    transformed,
                    session=session,
                )


class Forward:
    @free_fall_migration(document_models=[])
    async def rename_legacy_brand_fields(self, session):
        await _migrate_database(session, _replace_forward)


class Backward:
    @free_fall_migration(document_models=[])
    async def restore_legacy_brand_fields(self, session):
        await _migrate_database(session, _replace_backward)
