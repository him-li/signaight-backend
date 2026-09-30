import asyncio
import uuid
from beanie import free_fall_migration
from bson.dbref import DBRef


class Forward:

    @free_fall_migration(document_models=[])
    async def create_initial_log(self, session):
        editor_data = {
            'id': None,
            'email': None,
            'firstname': "SignAIght",
            'lastname': "System"
        }
        # Schemaless migration
        db = session.client.get_default_database()
        data = []
        async for person in db.persons.find({}, session=session):
            person_id = person.get('_id')
            data.append({
                "_id": str(uuid.uuid4()),
                "entity": DBRef('persons', person_id),
                "_class_id": "PersonAuditLog",
                "editor": editor_data,
                "revision_id": person.get('revision_id'),
                "action": "Insert",
                "changes": person
            })
        if data:
            try:
                db.audit_logs.insert_many(data, session=session)
                db.persons.update_many(
                    {},
                    {"$set": {'last_edited_by': editor_data}},
                    session=session
                )
            except Exception:
                return
        await asyncio.sleep(5)


class Backward:
    @free_fall_migration(document_models=[])
    async def title_to_name(self, session):
        db = session.client.get_default_database()
        db.persons.update_many(
            {},
            {"$unset": {'last_edited_by': ''}},
            session=session
        )
