# flake8: noqa
import uuid
from beanie import free_fall_migration
from core.rules.person.person_ruleset import (
    person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04)


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_new_person_ruleset_watchlist_countries(self,
                                                             session):
        db = session.client.get_default_database()
        async for project in db.projects.find(
                {"project_platform": "50736d2841224eae663630a6ef12028ac95f4c04"},
                session=session):
            project_platform = project.get("project_platform")
            if project_platform == "50736d2841224eae663630a6ef12028ac95f4c04":
                await db.projects.update_one(
                    {'_id': project.get("_id")},
                    {'$set': {
                        "person_ruleset": person_ruleset_for_50736d2841224eae663630a6ef12028ac95f4c04}},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_person_ruleset(self,
                                            session):
        db = session.client.get_default_database()
        async for project in db.projects.find(
                {"project_platform": "50736d2841224eae663630a6ef12028ac95f4c04"},
                session=session):
            project_platform = project.get("project_platform")
            if project_platform == "50736d2841224eae663630a6ef12028ac95f4c04":
                await db.projects.update_one(
                    {'_id': project.get("_id")},
                    {'$unset': {"person_ruleset": None}},
                    upsert=False,
                    session=session
                )
