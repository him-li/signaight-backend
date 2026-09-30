from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_project_platform(self, session):
        db = session.client.get_default_database()
        await db.projects.update_many(
            {
                "$or": [
                    {'project_platform': None},
                    {'project_platform': {"$exists": True}}
                ]
            },
            {
                '$set': {
                    "project_platform": "7505d64a54e061b7acd54ccd58b49dc43500b635"
                }
            },   # noqa
            upsert=False,
            session=session
        )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_project_platform(self, session):
        db = session.client.get_default_database()
        await db.projects.update_many(
            {},
            {'$unset': {"project_platform": None}},
            upsert=False,
            session=session
        )
