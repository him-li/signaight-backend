from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_turn_fb_nicknames_to_list(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {"personal_details": 1},
                session=session):
            if nickname := person.get(
                    "personal_details", {}).get(
                        "name", {}).get(
                            "nickname", {}):
                if (nickname.get("fb_nicknames") is not None and
                        isinstance(nickname.get("fb_nicknames"), str)):
                    person['personal_details']['name']['nickname'][
                        'fb_nicknames'] = [nickname.get("fb_nicknames")]
                    await db.persons.update_one(
                        {'_id': person.get("_id")},
                        {'$set': {"personal_details": person.get(
                            "personal_details")}},
                        upsert=False,
                        session=session
                    )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_turn_fb_nicknames_to_str(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {"personal_details": 1},
                session=session):
            if nickname := person.get(
                    "personal_details", {}).get(
                        "name", {}):
                if (nickname.get("fb_nicknames") is not None and
                        isinstance(nickname.get("fb_nicknames"), list)):
                    person['personal_details']['name']['nickname'][
                        'fb_nicknames'] = str(nickname.get("fb_nicknames"))
                    await db.persons.update_one(
                        {'_id': person.get("_id")},
                        {'$set': {"personal_details": person.get(
                            "personal_details")}},
                        upsert=False,
                        session=session
                    )
