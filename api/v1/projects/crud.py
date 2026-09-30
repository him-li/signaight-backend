from typing import Iterable, List, Union
import uuid
from beanie import PydanticObjectId
from fastapi import HTTPException
from bson.binary import Binary as uuidBinary
from beanie.operators import In

from api.crud import BasicCRUD
from api.local_authorization import require_active_user, require_project_access
from api.pagination import paginate
from core.models import ProjectModel, PersonModel
from .schemas import (
    PersonsRiskmatrixWidgets,
    ProjectListRead,
    ProjectListView,
    PersonsLeaderboardInfo,
    PersonBasicInfoView,
    PersonRankingView,
    PersonsLeaderboardWidgets
)


class ProjectsCRUD(BasicCRUD):

    kind = "api.v1.projects"

    async def _pagination_transformer(self, items):
        return [ProjectListRead(**item.model_dump())
            for item in items]

    async def create(self, data, user_id):
        await self.authorized('create')
        project = ProjectModel(**data)
        project.user_id = user_id
        result = await project.insert()
        return result

    async def list(self, params, filter):
        query = ProjectModel.find_all()
        query = await self.authorized(
            'list',
            query,
            {
                "request.resource.attr.owner_id": "user_id"
            }
        )
        query = query.project(ProjectListView)
        query = filter.filter(query)
        query = filter.sort(query)
        #projects = await query.to_list()
        #for project in projects:
        #    print(project.model_dump_json())
        #raise HTTPException(status_code=404,
        #                    detail="Project does not exist!")
        projects = await paginate(query,
                                  transformer=self._pagination_transformer)
        project_ids = [project.id for project in projects.items]
        projects_person_count = await self.read_person_count_by_projects(
            project_ids)
        lookup = {item['_id']: item for item in projects_person_count}
        for project in projects.items:
            if project.id in lookup:
                project.person_count = lookup.get(
                    project.id, {}).get("person_count")
        return projects

    async def read_list_ids(self, user_id):
        require_active_user(self.principal)
        if self.principal.is_admin:
            return [project.id for project in await ProjectModel.find_all().to_list()]
        return [project.id for project in await ProjectModel.find(
                ProjectModel.user_id == self.principal.id).to_list()]

    async def read(self, id):
        project = await ProjectModel.get(id)
        if not project:
            raise HTTPException(status_code=404,
                                detail="Project does not exist!")
        require_project_access(self.principal, project.user_id)
        return project

    async def update(self, id, data):
        project = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            setattr(project, k, v)
        if not project.person_ruleset:
            raise HTTPException(
                status_code=422,
                detail="Projects need to have person_ruleset")
        await project.save()
        return project

    async def delete(self, id):
        project = await self.read(id)
        # TODO: used here cause there is circular imports in models package
        await PersonModel.find(
            PersonModel.project.id == project.id
        ).delete()
        await project.delete()

    async def cleanup(self, id):
        await self.read(id)
        # safe cleanup project with demo data 0364782b-bb0b-48f9-97da-6577dfde81f0 # noqa
        persons = await PersonModel.find(
            {'project.$id': uuidBinary.from_uuid(id)}
        ).to_list()
        demo_ids = []
        if persons:
            shortened = []
            for i, person in enumerate(persons):
                shortened.append({
                    "f_name": person.personal_details.name.first_name.f_name,
                    "l_name": person.personal_details.name.last_name.l_name,
                    "email": person.personal_details.email.email_address,
                })
            for item in shortened:
                _persons = await PersonModel.find({
                    'project.$id': uuidBinary.from_uuid(
                        uuid.UUID('0364782b-bb0b-48f9-97da-6577dfde81f0')),
                    'personal_details.name.first_name.f_name': item.get(
                        'f_name'),
                    'personal_details.name.last_name.l_name': item.get(
                        'l_name'),
                    'personal_details.email.email_address': item.get('email'),
                }).to_list()
                for i, person in enumerate(_persons):
                    if i == 0:
                        demo_ids.append(person.id)
                        person.demo_data = True
                        await person.save()
                    else:
                        await person.delete()

        all_persons = await PersonModel.find().to_list()
        for person in all_persons:
            if person.id not in demo_ids:
                person.demo_data = False
                await person.save()

    # TODO: review this function cause hard query.

    def _normalize_ids(self, project_ids: Iterable[Union[str, uuid.UUID]]):
        out: List[Union[uuid.UUID]] = []
        for pid in project_ids:
            if isinstance(pid, (uuid.UUID)):
                out.append(pid)
                continue
            s = str(pid)
            try:
                out.append(uuid.UUID(s))
                continue
            except Exception:
                pass
            out.append(pid)
        return out

    async def read_leaderboard_info_by_projects(self, project_ids):
        proj_ids = self._normalize_ids(project_ids)
        pipeline = [
            {
                "$match": {
                    "project.$id": {"$in": proj_ids}
                }
            },
            {
                "$group": {
                    "_id": "$_id",  # person id
                    "project_id": { "$first": "$project.$id" },
                    "last_update": { "$first": "$last_update" },
                    "search_state": { "$first": "$search_state" },
                    "red_flags_count": {
                        "$max": { "$ifNull": ["$red_flags_count", 0] }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$project_id",
                    "analyzed": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$ne": ["$last_update", None]},
                                        {"$eq": ["$search_state.status", "Success"]},
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    },
                    "risks": {
                        "$sum": {
                            "$cond": [
                                { "$gt": ["$red_flags_count", 0] },
                                1,
                                0
                            ]
                        }
                    },
                    "red_flags": {
                        "$sum": "$red_flags_count"
                    },
                    "total_subjects": { "$sum": 1 }
                }
            }
        ]

        result = await PersonModel.aggregate(pipeline).to_list()

        if not result:
            return PersonsLeaderboardInfo(
                id=project_ids[0] if len(project_ids) == 1 else None,
                analyzed=0,
                risks=0,
                total_subjects=0,
                red_flags=0
            )

        # If multiple projects, aggregate totals in Python (fast, small data)
        if len(result) > 1:
            total_analyzed = sum(r.get("analyzed", 0) for r in result)
            total_risks = sum(r.get("risks", 0) for r in result)
            total_subjects = sum(r.get("total_subjects", 0) for r in result)
            red_flags = sum(r.get("red_flags", 0) for r in result)

            return PersonsLeaderboardInfo(
                id=project_ids[0] if len(project_ids) == 1 else None,
                analyzed=total_analyzed,
                risks=total_risks,
                total_subjects=total_subjects,
                red_flags=red_flags
            )

        result[0]["id"] = result[0].pop("_id", None)
        return PersonsLeaderboardInfo(**result[0])

    def _to_uuid_list(self, project_ids: Iterable[str | uuid.UUID | PydanticObjectId]):
        uuids: list[uuid.UUID] = []
        for pid in project_ids:
            if isinstance(pid, uuid.UUID):
                uuids.append(pid)
            else:
                try:
                    uuids.append(uuid.UUID(str(pid)))
                except Exception:
                    pass
        return uuids

    async def read_person_count_by_projects(self, project_ids):

        # Beanie documented filtering with linked models
        try:
            project_id_values = self._to_uuid_list(project_ids)
            pipeline = [
                {"$set": {"projectId": {"$ifNull": ["$project.$id", "$project._id"]}}},
                {"$match": {"projectId": {"$in": project_id_values}}},
                {"$group": {"_id": "$projectId", "person_count": {"$sum": 1}}},
            ]
            cursor = PersonModel.aggregate(pipeline, allowDiskUse=True)
            result = await cursor.to_list(length=None)
            return result
        except Exception:
            return []

    # TODO: review this function cause hard query.
    async def read_leaderboard_widgets_by_projects(self, project_ids):
        # Beanie documented filtering with linked models
        try:
            project_ids_uuid_binary = [
                uuid.UUID(project_id) for project_id in project_ids
            ]
        except Exception:
            project_ids_uuid_binary = [
                project_id for project_id in project_ids
            ]
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "high_compatibility": {"$sum": {"$cond": [{
                        "$eq": ["$compatibility", "High Compatibility"]}, 1, 0
                    ]}},
                    "medium_compatibility": {"$sum": {"$cond": [{
                        "$eq": ["$compatibility", "Medium Compatibility"]},
                        1, 0]}},
                    "low_compatibility": {"$sum": {"$cond": [{
                        "$eq": ["$compatibility", "Low Compatibility"]}, 1, 0
                    ]}},
                    "disqualified": {"$sum": {"$cond": [{
                        "$eq": ["$compatibility", "Disqualified"]}, 1, 0
                    ]}},
                    "score_0_10": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 0]},
                                        {"$lt": ["$signaight_score", 10]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_10_20": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 10]},
                                        {"$lt": ["$signaight_score", 20]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_20_30": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 20]},
                                        {"$lt": ["$signaight_score", 30]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_30_40": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 30]},
                                        {"$lt": ["$signaight_score", 40]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_40_50": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 40]},
                                        {"$lt": ["$signaight_score", 50]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_50_60": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 50]},
                                        {"$lt": ["$signaight_score", 60]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_60_70": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 60]},
                                        {"$lt": ["$signaight_score", 70]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_70_80": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 70]},
                                        {"$lt": ["$signaight_score", 80]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_80_90": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 80]},
                                        {"$lt": ["$signaight_score", 90]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "score_90_100": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$and": [
                                        {"$gte": ["$signaight_score", 90]},
                                        {"$lte": ["$signaight_score", 100]},
                                    ]
                                }, 1, 0,
                            ]
                        }
                    },
                    "search_running": {
                        "$sum": {"$cond": [
                            {"$eq": ['$search_state.status', "In progress"]},
                            1, 0]}
                    },
                    "search_timeout": {
                        "$sum": {"$cond": [
                            {"$eq": ['$search_state.status', "Timeout"]},
                            1, 0]}
                    },
                    "search_done": {
                        "$sum": {"$cond": [
                            {"$eq": ['$search_state.status', "Success"]},
                            1, 0]}
                    },
                    "search_error": {
                        "$sum": {"$cond": [
                            {"$eq": ['$search_state.status', "Error"]},
                            1, 0]}
                    },
                    "total": {"$sum": 1},
                }
            },
        ]
        result = await PersonModel.find(
            In(PersonModel.project.id, project_ids_uuid_binary)
        ).aggregate(pipeline).to_list(None)
        if result:
            return PersonsLeaderboardWidgets(**result[0])
        else:
            return PersonsLeaderboardWidgets(
                _id=None,
                high_compatibility=0,
                medium_compatibility=0,
                low_compatibility=0,
                disqualified=0,
                score_0_10=0,
                score_10_20=0,
                score_20_30=0,
                score_30_40=0,
                score_40_50=0,
                score_50_60=0,
                score_60_70=0,
                score_70_80=0,
                score_80_90=0,
                score_90_100=0,
                search_running=0,
                search_done=0,
                search_error=0,
                total=0,
                search_timeout=0,
            )
            
    async def read_riskmatrix_widgets_by_projects(self, project_ids):
        # Beanie documented filtering with linked models
        try:
            project_ids_uuid_binary = [
                uuid.UUID(project_id) for project_id in project_ids
            ]
        except Exception:
            project_ids_uuid_binary = [
                project_id for project_id in project_ids
            ]
        pipeline = [
                {
                    "$match": {
                        "project.$id": {"$in": project_ids_uuid_binary}
                    }
                },

                {
                    "$group": {
                        "_id": "$_id",  # person id
                        "project_id": { "$first": "$project.$id" },
                        "last_update": { "$first": "$last_update" },
                        "search_state": { "$first": "$search_state" },
                        "compatibility": { "$first": "$compatibility" },
                        "risk_score": { "$first": "$risk_score" },
                        "red_flags_count": {
                            "$max": { "$ifNull": ["$red_flags_count", 0] }
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$project_id",
                        "analyzed": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$ne": ["$last_update", None]},
                                            {"$eq": ["$search_state.status", "Success"]},
                                        ]
                                    },
                                    1,
                                    0
                                ]
                            }
                        },
                        "risks": {
                            "$sum": {
                                "$cond": [
                                    { "$gt": ["$red_flags_count", 0] },
                                    1,
                                    0
                                ]
                            }
                        },
                        "red_flags": {
                            "$sum": "$red_flags_count"
                        },
                        "total_persons": { "$sum": 1 },
                        "score_0_10": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 0]},
                                            {"$lt": ["$risk_score", 10]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_10_20": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 10]},
                                            {"$lt": ["$risk_score", 20]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_20_30": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 20]},
                                            {"$lt": ["$risk_score", 30]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_30_40": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 30]},
                                            {"$lt": ["$risk_score", 40]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_40_50": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 40]},
                                            {"$lt": ["$risk_score", 50]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_50_60": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 50]},
                                            {"$lt": ["$risk_score", 60]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_60_70": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 60]},
                                            {"$lt": ["$risk_score", 70]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_70_80": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 70]},
                                            {"$lt": ["$risk_score", 80]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_80_90": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 80]},
                                            {"$lt": ["$risk_score", 90]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                        "score_90_100": {
                            "$sum": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {"$gte": ["$risk_score", 90]},
                                        ]
                                    }, 1, 0,
                                ]
                            }
                        },
                    }
                },
        ]
        result = await PersonModel.find(
            In(PersonModel.project.id, project_ids_uuid_binary)
        ).aggregate(pipeline).to_list(None)
        if result:
            total_analyzed = sum(r.get("analyzed", 0) for r in result)
            total_risks = sum(r.get("risks", 0) for r in result)
            total_persons = sum(r.get("total_persons", 0) for r in result)
            score_0_10 = sum(r.get("score_0_10", 0) for r in result)
            red_flags = sum(r.get("red_flags", 0) for r in result)
            score_10_20 = sum(r.get("score_10_20", 0) for r in result)
            score_20_30 = sum(r.get("score_20_30", 0) for r in result)
            score_30_40 = sum(r.get("score_30_40", 0) for r in result)
            score_40_50 = sum(r.get("score_40_50", 0) for r in result)
            score_50_60 = sum(r.get("score_50_60", 0) for r in result)
            score_60_70 = sum(r.get("score_60_70", 0) for r in result)
            score_70_80 = sum(r.get("score_70_80", 0) for r in result)
            score_80_90 = sum(r.get("score_80_90", 0) for r in result)
            score_90_100 = sum(r.get("score_90_100", 0) for r in result)

            return PersonsRiskmatrixWidgets(
                _id=result[0].pop("_id", None),
                score_0_10=score_0_10,
                score_10_20=score_10_20,
                score_20_30=score_20_30,
                score_30_40=score_30_40,
                score_40_50=score_40_50,
                score_50_60=score_50_60,
                score_60_70=score_60_70,
                score_70_80=score_70_80,
                score_80_90=score_80_90,
                score_90_100=score_90_100,
                red_flags=red_flags,
                risks=total_risks,
                analyzed=total_analyzed,
                total_persons=total_persons
            )
        else:
            return PersonsRiskmatrixWidgets(
                _id=None,
                score_0_10=0,
                score_10_20=0,
                score_20_30=0,
                score_30_40=0,
                score_40_50=0,
                score_50_60=0,
                score_60_70=0,
                score_70_80=0,
                score_80_90=0,
                score_90_100=0,
                red_flags=0,
                risks=0,
                analyzed=0,
                total_persons=0
            )


    async def read_basic_data_by_projects(self, project_ids):
        # Beanie documented filtering with linked models
        try:
            project_ids_uuid_binary = [
                uuid.UUID(project_id) for project_id in project_ids
            ]
        except Exception:
            project_ids_uuid_binary = [
                project_id for project_id in project_ids
            ]
        query = (
            await PersonModel.find(
                In(PersonModel.project.id, project_ids_uuid_binary)
            )
            .project(PersonBasicInfoView)
            .to_list()
        )
        return query

    async def read_ranking_by_projects(self, project_ids):
        # Beanie documented filtering with linked models
        try:
            project_ids_uuid_binary = [
                uuid.UUID(project_id) for project_id in project_ids
            ]
        except Exception:
            project_ids_uuid_binary = [
                project_id for project_id in project_ids
            ]
        query = (
            await PersonModel.find(
                In(PersonModel.project.id, project_ids_uuid_binary)
            )
            .project(PersonRankingView)
            .sort(["-signaight_score",
                   "+personal_details.name.first_name.f_name"])
            .to_list()
        )
        return query
