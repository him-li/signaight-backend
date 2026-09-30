from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_ds_filter(self, session):
        db = session.client.get_default_database()
        await db.candidates.update_many(
            {},
            {'$set': {"ds_filter": False}},
            upsert=False
        )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_ds_filter(self, session):
        db = session.client.get_default_database()
        await db.candidates.update_one(
            {},
            {'$unset': {"ds_filter": None}},
            upsert=False
        )
