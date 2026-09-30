from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_demo_data_signaight_score_to_risk_score(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find({}, session=session):
            if not person.get("demo_data", False):
                continue
            _set = {}
            if signaight_score := person.get("signaight_score"):
                _set['risk_score'] = signaight_score

            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set, '$unset': {'signaight_score': None}},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_demo_data_risk_score_to_signaight_score(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {},
                {"personal_details": 1},
                session=session):
            if not person.get("demo_data", False):
                continue
            _set = {}
            if risk_score := person.get("risk_score"):
                _set['signaight_score'] = risk_score

            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set, '$unset': {'risk_score': None}},
                    upsert=False,
                    session=session
                )
