from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_create_search_ready_field(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            await db.persons.update_one(
                {'_id': person.get("id")},
                {'$set': {'search_ready': True}},
                upsert=False,
                session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_search_ready_field(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            await db.persons.update_one(
                {'_id': person.get("id")},
                {'$unset': {'search_ready': None}},
                upsert=False,
                session=session
                )
