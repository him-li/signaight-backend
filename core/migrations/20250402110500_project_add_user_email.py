from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_user_email(self, session):
        db = session.client.get_default_database()
        await db.projects.update_many(
            {},
            {
                '$set': {
                    "user_email": "admin@signaight.ai"
                }
            },   # noqa
            upsert=False,
            session=session
        )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_user_email(self, session):
        db = session.client.get_default_database()
        await db.projects.update_many(
            {},
            {'$unset': {"user_email": None}},
            upsert=False,
            session=session
        )
