from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_counters_for_alerts_evalation_red_flags(self,
                                                                  session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, session=session):
            person_id = person.get("_id")
            alerts = await db.person_alerts.find_one(
                {"person.$id": person_id})
            evaluation = await db.person_evaluations.find_one(
                {"person.$id": person_id})
            flags = await db.person_flags.find(
                {"person.$id": person_id}).to_list()
            flags_count = len(flags)
            alert_count = 0
            evaluation_count = 0
            if alerts:
                alert_count = sum(
                    1 for key, value in alerts.items() if
                    value is not None and key != "_id"
                    and key != "person"
                )
            if evaluation:
                evaluation_count = sum(
                    1 for key, value in evaluation.items() if
                    value is not None and key != "_id"
                    and key != "person"
                )
            _set = {}
            _set['alerts_count'] = alert_count
            _set['evaluation_count'] = evaluation_count
            _set['red_flags_count'] = flags_count

            if _set:
                await db.persons.update_one(
                    {'_id': person_id},
                    {'$set': _set},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_counters_for_alerts_evalation_red_flags(self,
                                                                     session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                session=session):
            await db.persons.update_one(
                {'_id': person.get("_id")},
                {'$unset': {'alerts_count': None,
                            'evaluation_count': None,
                            'red_flags_count': None}},
                upsert=False,
                session=session
            )
