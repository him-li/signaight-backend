from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_create_comments_from_remark(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("remark"):
                comments = [
                    {
                        "text": person.get("remark"),
                        "created_by": person.get("last_edited_by", {}),
                        "created_at": person.get("last_update")
                    }
                ]

                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"comments": comments},
                     '$unset': {'remark': None},
                     },
                    upsert=False,
                    session=session
                )


class Backward:
    async def migrate_create_remark_from_last_comment(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("comments"):
                comments = person.get("comments")
                comments.sort(key=lambda created_at: created_at)
                comments.reverse()
                remark = comments[0].text

                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"remark": remark},
                     '$unset': {'comments': None}},
                    upsert=False,
                    session=session
                )
