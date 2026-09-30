from beanie import free_fall_migration


class Forward:
    @free_fall_migration(
        document_models=[]
    )
    async def new_alert_evaluation(self, session):
        db = session.client.get_default_database()
        async for alert in db.person_alerts.find(
                {}, session=session):
            if alert.get("long_stay_in_israel"):
                strong_affinity = {
                    **alert.get("strong_affinity_with_israel", {}),
                    **alert.get("long_stay_in_israel", {})
                }
                await db.person_alerts.update_one(
                    {'_id': alert.get("_id")},
                    {'$set': {'strong_affinity_with_israel': strong_affinity},
                     '$unset': {'long_stay_in_israel': None}},
                    upsert=False,
                    session=session
                    )
            else:
                await db.person_alerts.update_one(
                    {'_id': alert.get("_id")},
                    {'$unset': {'long_stay_in_israel': None}},
                    upsert=False,
                    session=session
                    )

        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            language_skills = evaluation.get("foreign_languages")
            moral_values = evaluation.get("volunteering")
            await db.person_evaluations.update_one(
                {'_id': evaluation.get("_id")},
                {
                 '$set': {'language_skills': language_skills,
                          'moral_values': moral_values},
                 '$unset': {'foreign_languages': None,
                            'volunteering': None,
                            'wisdom_common_sense': None},
                 },
                upsert=False,
                session=session
                )


class Backward:
    @free_fall_migration(
        document_models=[]
    )
    async def old_alert_evaluation(self, session):
        db = session.client.get_default_database()
        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            foreign_languages = evaluation.get("language_skills")
            volunteering = evaluation.get("moral_values")
            await db.person_evaluations.update_one(
                {'_id': evaluation.get("_id")},
                {
                 '$set': {'foreign_languages': foreign_languages,
                          'volunteering': volunteering},
                 '$unset': {'language_skills': None,
                            'moral_values': None},
                 },
                upsert=False,
                session=session
                )
