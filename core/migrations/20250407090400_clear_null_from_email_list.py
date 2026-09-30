from beanie import free_fall_migration
from dotty_dictionary import dotty


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_clear_null_from_email_list(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, session=session):
            if not (personal_details := person.get("personal_details", {})):
                continue
            _set = {}
            personal_details = dotty(personal_details)
            if emails := personal_details.get("email.email_address", []):
                if not emails:
                    continue
                if not isinstance(emails, list):
                    continue
                for i, email in enumerate(emails):
                    if not email or '@' not in email:
                        emails.pop(i)
                _set["personal_details.email.email_address"] = emails

            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_email_list(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {"personal_details": 1},
                session=session):
            try:
                if not (personal_details := person.get("personal_details",
                                                       {})):
                    continue
                _set = {}
                personal_details = dotty(personal_details)
                if emails := personal_details.get("email.email_address", []):
                    if not emails:
                        continue
                    if not isinstance(emails, list):
                        continue
                    for i, email in enumerate(emails):
                        if not email or '@' not in email:
                            emails.pop(i)
                    _set["personal_details.email.email_address"] = emails

                if _set:
                    await db.persons.update_one(
                        {'_id': person.get("_id")},
                        {'$set': _set},
                        upsert=False,
                        session=session
                    )
            except Exception:
                pass
