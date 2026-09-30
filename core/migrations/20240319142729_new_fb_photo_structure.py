from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_new_fb_photo_structure(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("posts"):
                for post in person.get("posts"):
                    if post.get("fb_post_photo"):
                        url = post.get("fb_post_photo")
                        post['fb_post_photo'] = {
                            "fb_photo": {
                                "url": url
                            }
                        }

                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"posts": person.get("posts")}},
                    upsert=False,
                    session=session
                )


class Backward:
    async def migrate_old_fb_photo_structure(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {}, session=session):
            if person.get("posts"):
                for post in person.get("posts"):
                    if post.get("fb_post_photo"):
                        post['fb_post_photo'] = post.get(
                            "fb_post_photo").get("fb_photo").get("fb_photo")

                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': {"posts": person.get("posts")}},
                    upsert=False,
                    session=session
                )
