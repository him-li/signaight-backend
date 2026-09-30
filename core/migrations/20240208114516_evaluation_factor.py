from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_create_evaluation_factor(self, session):
        db = session.client.get_default_database()
        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            for key in evaluation.keys():
                if evaluation.get(key) and key != '_id' and key != 'person':
                    category = {
                        'factors': [{
                            'title': evaluation.get(key, {}).get('title'),
                            'score': evaluation.get(key, {}).get('score')
                        }],
                        'score': evaluation.get(key, {}).get('score')
                    }
                    await db.person_evaluations.update_one(
                        {'_id': evaluation.get("_id")},
                        {'$set': {key: category}},
                        upsert=False,
                        session=session
                        )


class Backward:
    async def migrate_remove_evaluation_factor(self, session):
        db = session.client.get_default_database()
        async for evaluation in db.person_evaluations.find(
                {}, session=session):
            for key in evaluation.keys():
                if evaluation.get(key) and key != '_id' and key != 'person':
                    category = {
                        'title': evaluation.get(key, {}).get('factors')[0].get(
                            'title'),
                        'score': evaluation.get(key, {}).get('score')
                    }
                    await db.person_evaluations.update_one(
                        {'_id': evaluation.get("_id")},
                        {'$set': {key: category}},
                        upsert=False,
                        session=session
                        )
