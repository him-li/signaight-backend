from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_create_search_state_field(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("search_ready"):
                search_state = {
                    "is_done": True,
                    "status": "Success"
                }
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {'search_state': search_state}},
                    upsert=False,
                    session=session
                    )
            else:
                search_state = {
                    "is_done": False,
                    "status": "Error",
                    "description": "Search Error"
                }
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {'search_state': search_state}},
                    upsert=False,
                    session=session
                    )
            await db.persons.update_one(
                {'_id': person.get("_id")},
                {'$unset': {'search_ready': None}},
                upsert=False,
                session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_search_state_field(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("search_state").get("is_done"):
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {'search_ready': True}},
                    upsert=False,
                    session=session
                    )
            else:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {'search_ready': False}},
                    upsert=False,
                    session=session
                    )
            await db.persons.update_one(
                {'_id': person.get("_id")},
                {'$unset': {'search_state': None}},
                upsert=False,
                session=session
                )
