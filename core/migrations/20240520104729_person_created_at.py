from datetime import datetime
from beanie import free_fall_migration


class Forward:
    @free_fall_migration(
        document_models=[]
    )
    async def change_from_independent_team_player_to_teamwork(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, {
                "last_update": 1, "created_at": 1}):
            if not person.get('created_at'):
                last_update = person.get('last_update', datetime.now())
                await db.persons.update_one(
                    {'_id': person.get('_id')},
                    {'$set': {'created_at': last_update}},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(
        document_models=[]
    )
    async def change_from_teamwork_to_independent_team_player(self, session):
        db = session.client.get_default_database()
        await db.persons.update_many(
            {},
            {'$unset': {"created_at": None}},
            upsert=False,
            session=session
        )
