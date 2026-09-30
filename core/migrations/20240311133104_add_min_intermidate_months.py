from beanie import free_fall_migration
from core.rules.person.person_ruleset import (
    person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635)


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_create_project_person_ruleset(self, session):
        db = session.client.get_default_database()
        async for project in db.projects.find(
                {}, session=session):
            await db.projects.update_one(
                {'_id': project.get("_id")},
                {'$set': {
                    "person_ruleset": person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635}},  # noqa
                upsert=False,
                session=session
            )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_project_person_ruleset(self, session):
        db = session.client.get_default_database()
        async for project in db.projects.find(
                {}, session=session):
            await db.projects.update_one(
                {'_id': project.get("_id")},
                {'$unset': {"person_ruleset": None}},
                upsert=False,
                session=session
            )
