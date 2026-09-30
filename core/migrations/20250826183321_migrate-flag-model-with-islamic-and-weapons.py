# flake8: noqa
import uuid
from beanie import free_fall_migration

class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_flags_model(self, session):
        db = session.client.get_default_database()
        flag_delete_ids = []
        flags_to_instert = []

        async for person in db.persons.find({}, session=session):
            person_id = person.get("_id")
            flags = await db.person_flags.find({"person.$id": person_id}).to_list()
            if flags:

                for flag in flags:
                    _set = {
                        "illegal_immigration": None,
                        "islamic_extremism": None,
                        "substance": None,
                        "sexual_misconduct": None,
                        "bragging_exceptional_lifestyle": None,
                        "activism": None,
                        "terror_conviction": None,
                        "online_radicalization": None,
                        "pro_palestinian_statements": None,
                        "suicidal_ideation": None,
                        "watchlist_countries": None,
                        "weapons": None,
                        "_id": uuid.uuid4(),
                    }
                    _set["person"] = flag.get("person")
                    flag_delete_ids.append(flag.get("_id"))
                    for key, value in flag.items():
                        if(value is not None and key not in ('person', '_id')):
                            oldFlag = value
                            updated_flag = {}
                            category = oldFlag.get('category')
                            sub_category = oldFlag.get('sub_category')
                            updated_flag['category'] = category
                            updated_flag['severity'] = oldFlag.get('severity') if oldFlag.get('severity') else 0
                            updated_flag['description'] = oldFlag.get('description')  if oldFlag.get('description') else ''
                            updated_flag['created_at'] = oldFlag.get('created_at')
                            updated_flag['updated_at'] = oldFlag.get('updated_at')
                            updated_flag['sub_categories'] = [{
                                'sub_category': oldFlag.get("sub_category"),
                                'description' : oldFlag.get('description')  if oldFlag.get('description') else '',
                                'factors' : oldFlag.get("factors"),
                                'severity' : oldFlag.get('severity') if oldFlag.get('severity') else 0,
                            }]
                            if(key == 'extremism' and sub_category != 'Weapons'):
                                updated_flag['category'] = 'Islamic Extremism'
                                updated_flag['description'] = 'Terms suspected as Salafi-Jihadist terms detected. Frequent use of such terms may indicate radicalization and potential security risk.'
                                updated_flag['sub_categories'] = [{
                                    'sub_category': oldFlag.get("sub_category"),
                                    'description' : 'Terms suspected as Salafi-Jihadist terms detected. Frequent use of such terms may indicate radicalization and potential security risk.',
                                    'factors' : oldFlag.get("factors"),
                                    'severity' : oldFlag.get('severity') if oldFlag.get('severity') else 0,
                                }]
                                _set['islamic_extremism'] = updated_flag
                            elif (key == 'extremism' and sub_category == 'Weapons'):
                                updated_flag['category'] = 'Weapons'
                                updated_flag['description'] = 'Weapon imagery detected. Prominent display may indicate potential risk or violent behavioral patterns.'
                                updated_flag['sub_categories'] = [{
                                    'sub_category': oldFlag.get("sub_category"),
                                    'description' : 'Weapon imagery detected. Prominent display may indicate potential risk or violent behavioral patterns.',
                                    'factors' : oldFlag.get("factors"),
                                    'severity' : oldFlag.get('severity') if oldFlag.get('severity') else 0,
                                }]
                                _set['weapons'] = updated_flag
                            else:
                                _set[key] = updated_flag
                    flags_to_instert.append(_set)
                await  db.person_flags.delete_many({"_id": {"$in": flag_delete_ids}}, session=session)
        for data in flags_to_instert:
            await db.person_flags.insert_one(data, session=session)

        async for flag in db.person_flags.find({}, session=session):
            flag_person_id = flag.get("person").id
            flag_person = await db.persons.find(
                {"_id": flag_person_id}, session=session
            ).to_list()
            if not flag_person:
                await db.person_flags.delete_one(
                    {"_id": flag.get("_id")}, session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_revert_flags_migration(self, session):
        db = session.client.get_default_database()
        async for flag in db.person_flags.find({}, session=session):
            flag_person = flag.get("person")
            for key, value in flag.items():
                await db.person_flags.insert_one(
                    {**value, "person": flag_person, "_id": uuid.uuid4()}
                )
            await db.person_flags.delete_one({"_id": flag.get("_id")})
