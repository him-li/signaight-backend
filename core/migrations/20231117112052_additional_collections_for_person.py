import asyncio
import uuid
from beanie import free_fall_migration
from bson.dbref import DBRef

evaluation_fields = ['resilience', 'flexibility', 'work_under_pressure', 'curiosity',
                'decision_making', 'courage', 'independent_team_player', 
                'volunteering', 'foreign_languages', 'interpersonal_skills', 
                'wisdom_common_sense']
alerts_fields = ['strong_affinity_with_israel', 'long_stay_in_israel', 
                'occupational_instability']

def forward_remap_evaluation(evaluation):
    for field in evaluation_fields:
        if ev_category := evaluation.get(field):
            _ev_category = {
                'score': ev_category.get('evaluation_score')
            }
            if ev_title := evaluation.get('evaluation_title'):
                _ev_category['title'] = ev_title
            evaluation[field] = _ev_category
    return evaluation

def forward_remap_alerts(alerts):
    for field in alerts_fields:
        if alert := alerts.get(field):
            alert_notes = alert.pop('alert_notes', [])
            heuristics = []
            for alert_note in alert_notes:
                heuristics.append({
                    'title': alert_note.pop('alert_subtitle'),
                    'description': alert_note.pop('alert_note'),
                    'score': alert.get('alert_score', 0)
                })
            if heuristics:
                alert['heuristics'] = heuristics
            alert['score'] = alert.pop('alert_score', 0)

            alerts[field] = alert
    return alerts


class Forward:
    @free_fall_migration(document_models=[])
    async def alerts_evaluations_flags_from_person(self, session):
        db = session.client.get_default_database()
        data = {
            "person_alerts": [],
            "person_evaluations": [],
            "person_flags": [],
        }
        async for person in db.persons.find({}, session=session):
            collection_rel = {
                "person": DBRef('persons', person.get("_id"))
            }
            # many
            if flags := person.get('red_flags', []):
                for flag in flags:
                    flag["_id"] = str(uuid.uuid4())
                    data["person_flags"].append({**flag, **collection_rel})
            # one
            if evaluation := person.get('evaluation', {}):
                evaluation = forward_remap_evaluation(evaluation)
                evaluation["_id"] = str(uuid.uuid4())
                data["person_evaluations"].append({**evaluation, **collection_rel})
            # one
            if alerts := person.get('alerts', {}):
                alerts = forward_remap_alerts(alerts)
                alerts["_id"] = str(uuid.uuid4())
                data["person_alerts"].append({**alerts, **collection_rel})

        try:
            for collection, items in data.items():
                if items:
                    await db[collection].insert_many(items, session=session)
        except Exception as e:
            print(str(e))
            return

        await db.persons.update_many(
            {},
            {"$unset": {"alerts": 1, "evaluation": 1, "red_flags": 1,}},
            session=session
        )
    

def backward_remap_evaluation(evaluation):
    for field in evaluation_fields:
        if ev_category := evaluation.get(field):
            _ev_category = {
                'evaluation_score': ev_category.get('score')
            }
            if ev_title := evaluation.get('title'):
                _ev_category['evaluation_title'] = ev_title
            evaluation[field] = _ev_category
    return evaluation

def backward_remap_alerts(alerts):
    for field in alerts_fields:
        if alert := alerts.get(field):
            alert_notes = alert.pop('heuristics', [])
            heuristics = []
            for alert_note in alert_notes:
                heuristics.append({
                    'alert_subtitle': alert_note.pop('title'),
                    'alert_note': alert_note.pop('description'),
                })
            if heuristics:
                alert['alert_notes'] = heuristics
            alert['alert_score'] = alert.pop('score', 0)

            alerts[field] = alert
    return alerts


class Backward:
    @free_fall_migration(document_models=[])
    async def alerts_evaluations_flags_to_person(self, session):
        db = session.client.get_default_database()
        editor_data = {
            'id': None,
            'email': None,
            'firstname': "SignAIght",
            'lastname': "System"
        }
        async for person in db.persons.find({}):
            person_id = person.get("_id")
            data = {}
            # many
            red_flags = await db.person_flags.find({"person.$id": person_id}).to_list(length=10000)
            if red_flags:
                for red_flag in red_flags:
                    red_flag.pop("_id", None)
                    red_flag.pop("project", None)
                data["red_flags"] = red_flags
            # one
            evaluation = await db.person_evaluations.find_one({"person.$id": person_id})
            if evaluation:
                evaluation.pop("_id", None)
                evaluation.pop("project", None)
                data["evaluation"] = backward_remap_evaluation(evaluation)
            # one
            alerts = await db.person_alerts.find_one({"person.$id": person_id})
            if alerts:
                alerts.pop("_id", None)
                alerts.pop("project", None)
                data["alerts"] = backward_remap_alerts(alerts)

            try:
                await db.persons.update_one(
                    {"_id": person_id},
                    {"$set": data},
                    upsert=False, 
                    session=session
                )
            except Exception as e:
                print(str(e))
                return
            
        await db.person_flags.drop()
        await db.person_evaluations.drop()
        await db.person_alerts.drop()
