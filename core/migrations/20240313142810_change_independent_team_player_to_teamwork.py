from beanie import free_fall_migration
from core.rules.person.person_ruleset import (
    person_ruleset_for_7505d64a54e061b7acd54ccd58b49dc43500b635)


class Forward:
    @free_fall_migration(
        document_models=[]
    )
    async def change_from_independent_team_player_to_teamwork(self, session):
        db = session.client.get_default_database()
        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            independent_team_player = evaluation.get("independent_team_player")
            await db.person_evaluations.update_one(
                {'_id': evaluation.get("_id")},
                {
                    '$set': {'teamwork': independent_team_player},
                    '$unset': {'independent_team_player': None},
                },
                upsert=False,
                session=session
            )

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
    @free_fall_migration(
        document_models=[]
    )
    async def change_from_teamwork_to_independent_team_player(self, session):
        db = session.client.get_default_database()
        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            teamwork = evaluation.get("teamwork")
            await db.person_evaluations.update_one(
                {'_id': evaluation.get("_id")},
                {
                    '$set': {'independent_team_player': teamwork},
                    '$unset': {'teamwork': None},
                },
                upsert=False,
                session=session
            )
        async for project in db.projects.find(
                {}, session=session):
            await db.projects.update_one(
                {'_id': project.get("_id")},
                {'$unset': {"person_ruleset": None}},
                upsert=False,
                session=session
            )
