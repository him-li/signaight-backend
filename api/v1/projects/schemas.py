import uuid
from pydantic import Field, AnyHttpUrl
from typing import Optional, List, Union
from datetime import datetime

from core.fields import S3Path
from core.models import (UUIDModel, Project, ProjectModel, Rule,
    Person, PersonModel)


class ProjectRead(Project, UUIDModel):
    pass


class ProjectCreate(Project):
    person_ruleset: Optional[List[Rule]] = None


class ProjectUpdate(Project):
    title: Optional[str] = Field(default=None, examples=["Project Title"])
    created_at: Optional[datetime] = Field(
        default=None,
        examples=[str(datetime.now().isoformat())])
    updated_at: Optional[datetime] = Field(
        default=None,
        examples=[str(datetime.now().isoformat())])
    person_ruleset: Optional[List[Rule]] = None
    # TODO: review is there we have plans to save persons with project


class ProjectListRead(UUIDModel):
    title: str = Field(..., examples=["Project Title"])
    created_at: datetime = Field(
        default_factory=datetime.now,
        examples=[str(datetime.now().isoformat())]
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        examples=[str(datetime.now().isoformat())]
    )
    user_id: Optional[str] = Field(default=None, help="Project User ID")
    user_email: Optional[str] = Field(default=None, help="Project User Email")
    image: Optional[Union[S3Path, AnyHttpUrl]] = None
    description: Optional[str] = Field(
        default=None, help="Project Description")
    project_platform: str = Field(..., help="Project platform")
    person_count: Optional[int] = Field(
        default=None, help="Project Persons count")


class ProjectListView(ProjectListRead):
    # Workaround only for query projection schema.
    # WARNING: Do not use alias for fastapi output validation schema
    id: uuid.UUID = Field(..., alias="_id")


class ProjectIdRead(Project, UUIDModel):
    user_id: Optional[str] = Field(default=None, examples=["Project Title"])
    title: Optional[str] = None
    person_ruleset: Optional[List[Rule]] = None

    class Settings(ProjectModel.Settings):
        projection = {
            "user_id": 1
        }

class ProjectIdView(ProjectIdRead):
    # Workaround only for query projection schema.
    # WARNING: Do not use alias for fastapi output validation schema
    id: uuid.UUID = Field(..., alias="_id")


class PersonsLeaderboardInfo:
    id: Optional[str] = Field(None, alias="_id")
    risks: str
    total_subjects: str
    analyzed: str
    red_flags: str

    class Settings(PersonModel.Settings):
        projection = {"signaight_score": 1,
                      "last_update": 1,
                      "red_flags": 1,
                      "personal_details.name": 1,
                      "personal_details.email": 1
                      }

    # def __init__(self, _id, risks, total_subjects, red_flags, analyzed):
    def __init__(self, id, risks, total_subjects, analyzed, red_flags):
        self.id = id
        self.risks = risks
        self.total_subjects = total_subjects
        self.red_flags = red_flags
        self.analyzed = analyzed


class PersonsLeaderboardWidgets:
    high_compatibility: str
    medium_compatibility: str
    low_compatibility: str
    disqualified: str
    total: str
    score_0_10: str
    score_10_20: str
    score_20_30: str
    score_30_40: str
    score_40_50: str
    score_50_60: str
    score_60_70: str
    score_70_80: str
    score_80_90: str
    score_90_100: str
    search_running: str
    search_done: str
    search_error: str
    search_timeout: str

    class Settings(PersonModel.Settings):
        projection = {"signaight_score": 1,
                      "last_update": 1,
                      "red_flags": 1,
                      "personal_details.name": 1,
                      "personal_details.email": 1
                      }

    def __init__(self, _id,
                 high_compatibility,
                 medium_compatibility,
                 low_compatibility,
                 disqualified,
                 total,
                 score_0_10,
                 score_10_20,
                 score_20_30,
                 score_30_40,
                 score_40_50,
                 score_50_60,
                 score_60_70,
                 score_70_80,
                 score_80_90,
                 score_90_100,
                 search_running,
                 search_timeout,
                 search_done,
                 search_error,
                 ):
        self.high_compatibility = high_compatibility
        self.medium_compatibility = medium_compatibility
        self.low_compatibility = low_compatibility
        self.disqualified = disqualified
        self.total = total
        self.score_0_10 = score_0_10

        self.score_10_20 = score_10_20
        self.score_20_30 = score_20_30
        self.score_30_40 = score_30_40
        self.score_40_50 = score_40_50
        self.score_50_60 = score_50_60
        self.score_60_70 = score_60_70
        self.score_70_80 = score_70_80
        self.score_80_90 = score_80_90
        self.score_90_100 = score_90_100
        self.search_running = search_running
        self.search_done = search_done
        self.search_error = search_error
        self.search_timeout = search_timeout
        
class PersonsRiskmatrixWidgets:
    score_0_10: str
    score_10_20: str
    score_20_30: str
    score_30_40: str
    score_40_50: str
    score_50_60: str
    score_60_70: str
    score_70_80: str
    score_80_90: str
    score_90_100: str
    risks: str
    total_persons: str
    analyzed: str
    red_flags: str

    class Settings(PersonModel.Settings):
        projection = {"risk_score": 1,
                      "last_update": 1,
                      "red_flags": 1,
                      "personal_details.name": 1,
                      "personal_details.email": 1
                      }

    def __init__(self, _id,
                 score_0_10,
                 score_10_20,
                 score_20_30,
                 score_30_40,
                 score_40_50,
                 score_50_60,
                 score_60_70,
                 score_70_80,
                 score_80_90,
                 score_90_100,
                 risks,
                total_persons,
                analyzed,
                red_flags
                 ):
        self.id = _id
        self.score_0_10 = score_0_10
        self.score_10_20 = score_10_20
        self.score_20_30 = score_20_30
        self.score_30_40 = score_30_40
        self.score_40_50 = score_40_50
        self.score_50_60 = score_50_60
        self.score_60_70 = score_60_70
        self.score_70_80 = score_70_80
        self.score_80_90 = score_80_90
        self.score_90_100 = score_90_100
        self.risks = risks
        self.total_persons = total_persons
        self.analyzed = analyzed
        self.red_flags = red_flags


class PersonBasicInfoView(Person, UUIDModel):
    # Workaround only for query projection schema.
    # WARNING: Do not use alias for fastapi output validation schema
    id: uuid.UUID = Field(..., alias="_id")

    class Settings(PersonModel.Settings):
        projection = {"personal_details.name.full_name.full_name": 1,
                      "personal_details.name.first_name.f_name": 1,
                      "personal_details.name.last_name.l_name": 1,
                      "personal_details.email": 1,
                      "signaight_score": 1,
                      "compatibility": 1}


class PersonRankingView(Person, UUIDModel):
    # Workaround only for query projection schema.
    # WARNING: Do not use alias for fastapi output validation schema
    id: uuid.UUID = Field(..., alias="_id")

    class Settings(PersonModel.Settings):
        projection = {"signaight_score": 1}
