import uuid
from datetime import datetime
from pydantic import (
    Field,
    AnyHttpUrl,
    model_validator,
    field_serializer
)
from pymongo import IndexModel, DESCENDING
from typing import Any, Optional, Union, List

from core.config import settings
from core.fields import S3Path, s3path_serializer
from core.rules.person import person_ruleset

from .base import SignAIghtSchema, Document
from .rule import Rule
from .pnr_data import ProjectPNRData


class Project(SignAIghtSchema):
    title: str = Field(..., examples=["Project Title"])
    created_at: datetime = Field(
        default_factory=datetime.now,
        examples=[str(datetime.now().isoformat())]
    )
    updated_at: Optional[datetime] = Field(
        None, examples=[str(datetime.now().isoformat())]
    )
    user_id: Optional[str] = Field(None, help="Project User ID")
    user_email: Optional[str] = Field(None, help="Project User Email")
    image: Optional[Union[S3Path, AnyHttpUrl]] = None
    description: Optional[str] = Field(None, help="Project Description")
    person_ruleset: List[Rule]
    project_platform: str = settings.APP_DATA_CONTEXT
    pnr_data: Optional[ProjectPNRData] = None

    # validators
    @model_validator(mode="before")
    @classmethod
    def populate_ruleset_if_empty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not (ruleset := data.get('person_ruleset')):
                ruleset = getattr(
                    person_ruleset,
                    "person_ruleset_for_{}".format(data.get("project_platform",
                                                            settings.APP_DATA_CONTEXT)),
                    None)
                if person_ruleset and isinstance(ruleset, list):
                    data['person_ruleset'] = [Rule(**rule)
                                              for rule in ruleset
                                              if isinstance(rule, dict)]
        return data

    # serializers
    @field_serializer("image", when_used="json-unless-none")
    def serialize_project_image_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class ProjectModel(Project, Document):

    class Settings:
        name = "projects"
        indexes = [
            IndexModel(
                [
                    ("created_at", DESCENDING),
                ],
                name="projects_created_at",
                background=True,
                sparse=True
            ),
        ]
        use_revision = False
