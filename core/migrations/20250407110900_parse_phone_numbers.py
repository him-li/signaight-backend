import phonenumbers
from beanie import free_fall_migration
from dotty_dictionary import dotty


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_parse_phone_numbers(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, session=session):
            if not (personal_details := person.get("personal_details", {})):
                continue
            _set = {}
            personal_details = dotty(personal_details)
            if phones := personal_details.get("phone.phones", []):
                if not phones:
                    continue
                if not isinstance(phones, list):
                    continue
                for i, phone in enumerate(phones):
                    if not phone:
                        phones.pop(i)
                    try:
                        phone = phonenumbers.parse(phone, None)
                        phone = f'+{phone.country_code}{phone.national_number}'
                    except Exception:
                        phone_str = f'+{phone}'
                        phone = phonenumbers.parse(phone_str, None)
                        phone = f'+{phone.country_code}{phone.national_number}'
                    phones[i] = phone

                _set["personal_details.phone.phones"] = phones

            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_phone_numbers(self, session):
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
                if phones := personal_details.get("phone.phones", []):
                    if not phones:
                        continue
                    if not isinstance(phones, list):
                        continue
                    for i, phone in enumerate(phones):
                        if not phone:
                            phones.pop(i)
                        phone = phonenumbers.parse(phone, None)
                    _set["personal_details.phone.phones"] = []

                if _set:
                    await db.persons.update_one(
                        {'_id': person.get("_id")},
                        {'$set': _set},
                        upsert=False,
                        session=session
                    )
            except Exception:
                pass
