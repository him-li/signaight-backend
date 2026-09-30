from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_is_favorite_is_attention(self, session):
        db = session.client.get_default_database()
        await db.persons.update_many(
            {},
            {'$set': {"is_favorite": False,
                        "is_attention": False}},
            upsert=False,
            session=session
        )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_is_favorite_is_attention(self, session):
        db = session.client.get_default_database()
        await db.persons.update_many(
            {},
            {'$unset': {"is_favorite": None,
                        "is_attention": None}},
            upsert=False,
            session=session
        )
