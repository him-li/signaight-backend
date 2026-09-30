from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_activity_type(self, session):
        db = session.client.get_default_database()
        await db.persons.update_many(
            {'posts': {'$ne': None}},
            {'$set': {"posts.$[].activity_type": "post"}},
            upsert=False
        )

class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_activity_type(self, session):
        db = session.client.get_default_database()
        await db.persons.update_many(
            {'posts': {'$ne': None}},
            {'$unset': {"posts.$[].activity_type": 1}},
            upsert=False
        )
