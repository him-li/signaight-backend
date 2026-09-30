from beanie import free_fall_migration
from dotty_dictionary import dotty

class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_language_name_to_language_and_normalize_fb_checkins(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, session=session):
            if not (personal_details := person.get("personal_details", {})):
                continue
            _set = {}
            personal_details = dotty(personal_details)
            if languages := personal_details.get("languages.languages", []):
                if not languages:
                    continue
                for language in languages:
                    language['language'] = language.pop('name', 'English')
                _set["personal_details.languages.languages"] = languages
            if check_ins := personal_details.get("location.check_ins", {}):
                if not check_ins:
                    continue
                for check_in_type, values in check_ins.items():
                    if not values:
                        continue
                    for i, value in enumerate(values):
                            if isinstance(value, str):
                                check_ins[check_in_type][i] = {
                                    "title": value
                                }
                _set["personal_details.location.check_ins"] = check_ins
                            
            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set},
                    upsert=False,
                    session=session
                )

class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_language_language_to_name(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {"personal_details": 1},
                session=session):
            try:
                if languages := person.get(
                        "personal_details", {}).get(
                            "languages", {}).get(
                                "languages", {}):
                    for language in languages:
                        language['name'] = language.pop('language', 'English')
                    await db.persons.update_one(
                        {'_id': person.get("_id")},
                        {'$set': {"personal_details.languages.languages": languages}},
                        upsert=False,
                        session=session
                    )
            except Exception as e:
                pass 
