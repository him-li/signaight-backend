import uuid
from beanie.operators import In
from api.v1.persons.schemas import PersonListView
from api.v1.projects.schemas import ProjectIdView
from core.models.flags import PersonFlag
from core.models.project import ProjectModel
from fastapi import HTTPException

from core.models import FlagModel, PersonModel
from api.pagination import paginate
from .schemas import FlagRead, RedFlagStats


class FlagsCRUD:

    async def _pagination_transformer(self, items):
        return [FlagRead(**item.model_dump()) for item in items]

    async def create(self, data):
        flag = FlagModel(**data)
        result = await flag.insert()
        return result

    async def list(self, params, filter):
        query = FlagModel.find_all(fetch_links=True)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        flag = await FlagModel.get(id)
        if not flag:
            raise HTTPException(status_code=404,
                                detail="Flag does not exist!")
        return flag

    async def read_all_flags_by_person(self, params, filter, person_id):
        query = FlagModel.find_many(
            FlagModel.person.id == uuid.UUID(person_id)
        )
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def update(self, id, data):
        await FlagModel.find_one(FlagModel.id == id).update(
            {"$set": data}
        )
        flag = await self.read(id)
        return flag

    async def statistics(self, params, filter):
        user_project_ids = await self._adopt_persons_filter_for_list(filter)

        query = PersonModel.find(
            In(PersonModel.project.id, user_project_ids),
        ).project(PersonListView)

        query = filter.filter(query)
        query = filter.sort(query)

        return await self._red_flag_stats_from_query(query)

    async def _red_flag_stats_from_query(self, query) -> RedFlagStats:
        """
        Counts how many filtered persons have each selected red flag.
        Uses EXACTLY the same filters as the paginated query.
        """
        ALL_RED_FLAGS = list(PersonFlag.model_fields.keys())

        mongo_filter = query.get_filter_query()

        pipeline = [
            {"$match": mongo_filter},

            {
                "$lookup": {
                    "from": "person_flags",
                    "localField": "_id",
                    "foreignField": "person.$id",
                    "as": "flags"
                }
            },
            {"$unwind": "$flags"},

            {
                "$lookup": {
                    "from": "persons",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "person_data"
                }
            },
            {"$unwind": "$person_data"},

            {
                "$project": {
                    "flags_array": {"$objectToArray": "$flags"},
                    "flag_obj": "$flags",
                    "person_id": "$_id",
                    "profile_picture": "$person_data.personal_details.visuals.profile_photo.profile_picture"
                }
            },

            {"$unwind": "$flags_array"},

            {
                "$match": {
                    "flags_array.k": {"$in": ALL_RED_FLAGS},
                    "flags_array.v": {"$ne": None}
                }
            },

            {"$unwind": "$flags_array.v.sub_categories"},
            {"$unwind": "$flags_array.v.sub_categories.factors"},

            {
                "$project": {
                    "flag_name": "$flags_array.k",
                    "person_id": 1,
                    "profile_picture": 1,
                    "flag_photo": "$flags_array.v.sub_categories.factors.source.photo"
                }
            },

            {
                "$group": {
                    "_id": "$flag_name",
                    "count": {"$sum": 1},
                    "persons": {
                        "$addToSet": {
                            "id": "$person_id",
                            "profile_picture": "$profile_picture",
                            "flag_photo": "$flag_photo"
                        }
                    }
                }
            }
        ]

        cursor = PersonModel.aggregate(pipeline)

        raw = {
            doc["_id"]: {
                "count": doc["count"],
                "persons": doc["persons"],
            }
            async for doc in cursor
        }

        final = {}

        for flag in ALL_RED_FLAGS:
            doc = raw.get(flag)

            if not doc:
                final[flag] = {"count": 0, "persons": []}
                continue

            persons_map = {}

            for p in doc["persons"]:
                pid = str(p["id"])

                if pid not in persons_map:
                    persons_map[pid] = {
                        "id": pid,
                        "profile_picture": p.get("profile_picture", None),
                        "flag_images": []
                    }

                flag_photo = p.get("flag_photo")
                if flag_photo:
                    persons_map[pid]["flag_images"].append(flag_photo)

            final[flag] = {
                "count": len(persons_map),
                "persons": list(persons_map.values())
            }

        return RedFlagStats(**final)

    async def _adopt_persons_filter_for_list(self, filter):
        query = ProjectModel.find_all()
        user_projects = await query.project(ProjectIdView).to_list()
        user_project_ids = [project.id for project in user_projects]
        if filter.project__id:
            if filter.project__id in user_project_ids:
                user_project_ids = [filter.project__id]
            else:
                user_project_ids = []
        if filter.project__id:
            filter.project__id = None
        if filter.project__project_platform:
            filter.project__project_platform = None
        if filter.project__project_platform:
            filter.project__project_platform = None
        return user_project_ids
