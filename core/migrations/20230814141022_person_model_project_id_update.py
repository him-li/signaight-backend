from bson.dbref import DBRef
from beanie import free_fall_migration


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_project_link_into_person(self, session):
        db = session.client.get_default_database()
        # get list of projects
        async for project in db.projects.find(
                {}, {'_id': 1, 'persons': 1}, session=session):
            project_id = project.get('_id')
            # walktrogh each person in list of DBRef's
            for person_ref in project.get('persons', []):
                # inject project id into person as DBRef
                await db.persons.update_one(
                    {'_id': person_ref.id},
                    {'$set': {'project': DBRef('projects', project_id)}},
                    upsert=False,
                    session=session
                )
            # cleanup list of DBRef's in project
            await db.projects.update_one(
                {'_id': project_id},
                {'$unset': {'persons': ''}},
                upsert=False,
                session=session
            )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_persons_link_into_project(self, session):
        db = session.client.get_default_database()
        # walktrogh each person in db
        async for person in db.persons.find(
                {}, {'_id': 1, 'project': 1}, session=session):
            project_ref = person.get('project')
            # check DBRef link to project
            if not project_ref:
                continue
            # check project presence in db and skip iteration if not exists
            project = await db.projects.find_one(
                {'_id': project_ref.id},
                {'_id': 1, 'persons': 1},
                session=session
            )
            if not project:
                continue
            # inject person DBRef into list
            person_id = person.get('_id')
            persons = project.get('persons', [])
            persons.append(DBRef('persons', person_id))
            # save project with updated list if DBRef's
            await db.projects.update_one(
                {'_id': project.get('_id')},
                {'$set': {'persons': persons}},
                upsert=False,
                session=session
            )
            await db.persons.update_one(
                {'_id': person_id},
                {'$unset': {'project': ''}},
                upsert=False,
                session=session
            )
