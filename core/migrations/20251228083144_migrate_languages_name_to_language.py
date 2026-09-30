from beanie import free_fall_migration
from core.dotty_dictionary import dotty


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_languages_name_to_language(self, session):
        db = session.client.get_default_database()

        async for person in db.persons.find({}, session=session):
            personal_details = person.get("personal_details")
            if not personal_details:
                continue

            details = dotty(personal_details)
            languages = details.get("languages.languages", [])

            if not isinstance(languages, list) or not languages:
                continue

            updated_languages = []
            changed = False

            for lang in languages:
                # Already migrated → skip
                if "language" in lang:
                    updated_languages.append(lang)
                    continue

                # Old format
                if "name" in lang:
                    updated_languages.append({
                        "language": lang.get("name", "English"),
                        "proficiency": None
                    })
                    changed = True
                else:
                    updated_languages.append(lang)

            if changed:
                await db.persons.update_one(
                    {"_id": person["_id"]},
                    {"$set": {
                        "personal_details.languages.languages": updated_languages
                    }},
                    session=session
                )
                
class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_languages_language_to_name(self, session):
        db = session.client.get_default_database()

        async for person in db.persons.find({}, session=session):
            languages = (
                person.get("personal_details", {})
                      .get("languages", {})
                      .get("languages", [])
            )

            if not isinstance(languages, list) or not languages:
                continue

            updated_languages = []
            changed = False

            for lang in languages:
                if "language" in lang:
                    updated_languages.append({
                        "name": lang.get("language", "English")
                    })
                    changed = True
                else:
                    updated_languages.append(lang)

            if changed:
                await db.persons.update_one(
                    {"_id": person["_id"]},
                    {"$set": {
                        "personal_details.languages.languages": updated_languages
                    }},
                    session=session
                )


