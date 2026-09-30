from beanie import free_fall_migration
from datetime import datetime


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_activity_type(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, 
                {'last_update': 1}, 
                session=session):
            try:
                last_update = datetime.fromisoformat(
                    person.get('last_update', datetime.now()))
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"last_update": last_update}},
                    upsert=False,
                    session=session
                )
            except Exception as e:
                continue


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_activity_type(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {'last_update': 1}, 
                session=session):
            try:
                last_update = person.get(
                    'last_update', None).isoformat()
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"last_update": last_update}},
                    upsert=False,
                    session=session
                )
            except Exception as e:
                continue
