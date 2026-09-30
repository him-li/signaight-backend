# flake8: noqa
import uuid
from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_flags_model(self,
                                  session):
        db = session.client.get_default_database()
        flag_delete_ids = []

        async for person in db.persons.find({}, session=session):
            person_id = person.get("_id")
            flags = await db.person_flags.find(
                {"person.$id": person_id}).to_list()
            if flags:
                _set = {
                    "illegal_immigration": None,
                    "extremism": None,
                    "substance": None,
                    "sexual_misconduct": None,
                    "bragging_exceptional_lifestyle": None,
                    "activism": None,
                    "terror_conviction": None,
                    "online_radicalization": None,
                    "pro_palestinian_statements": None,
                    "suicidal_ideation": None,
                    "watchlist_countries": None,
                    "_id": uuid.uuid4()
                }
                for flag in flags:
                    _set['person'] = flag.get("person")
                    match flag.get("category"):
                        case "Illegal Immigration":
                            _set['illegal_immigration'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Extremism":
                            _set['extremism'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Substance":
                            _set['substance'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Sexual Misconduct":
                            _set['sexual_misconduct'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Bragging: Exceptional Lifestyle":
                            _set['bragging_exceptional_lifestyle'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Activism":
                            _set['activism'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Terror Conviction":
                            _set['terror_conviction'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Online Radicalization":
                            _set['online_radicalization'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Pro-Palestinian Statements":
                            _set['pro_palestinian_statements'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "Suicidal Ideation":
                            _set['suicidal_ideation'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case "WatchList Countries":
                            _set['watchlist_countries'] = flag
                            flag_delete_ids.append(flag.get("_id"))
                        case _:
                            _set['extremism'] = flag
                            flag_delete_ids.append(flag.get("_id"))

                if any(value is not None and key not in ('person', '_id') for key, value in _set.items()):
                    await db.person_flags.insert_one(_set, session=session)

        await db.person_flags.delete_many(
            {"_id": {"$in": flag_delete_ids}}, session=session)

        async for flag in db.person_flags.find({}, session=session):
            flag_person_id = flag.get("person").id
            flag_person = await db.persons.find({"_id": flag_person_id}, session=session).to_list()
            if not flag_person:
                await db.person_flags.delete_one({"_id": flag.get("_id")}, session=session)


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_revert_flags_migration(self,
                                             session):
        db = session.client.get_default_database()
        async for flag in db.person_flags.find(
                {},
                session=session):
            flag_person = flag.get("person")
            for key, value in flag.items():
                await db.person_flags.insert_one({
                    **value,
                    "person": flag_person,
                    "_id": uuid.uuid4()
                })
            await db.person_flags.delete_one({"_id": flag.get("_id")})
