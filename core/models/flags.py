from beanie import (Link, after_event, before_event,
                    Insert, ValidateOnSave, Update, Replace)
from datetime import datetime
from pydantic import (
    Field,
    AnyHttpUrl,
    field_validator,
    field_serializer
)
from pymongo import IndexModel, ASCENDING
from typing import Optional, Any, List, Union

from core.fields import S3Path, s3path_serializer
from core.models.geo_trace import Features

from .base import WithVerifiedFieldSchema, Document, SignAIghtSchema
from .person import PersonModel


class FactorSource(WithVerifiedFieldSchema):
    id: Optional[str] = None
    insight: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
    photo: Optional[Union[AnyHttpUrl, S3Path]] = None
    text: Optional[str] = None
    date: Optional[datetime] = Field(
        None, examples=[str(datetime.utcnow().isoformat())])
    location: Optional[Features] = None

    @field_serializer("photo", when_used="json-unless-none")
    def serialize_factor_source_photo_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)

class Factor(WithVerifiedFieldSchema):
    field: Optional[str] = None
    platform: Optional[str] = None
    source: Optional[FactorSource] = None
    check: Optional[Any] = None
    success: Optional[bool] = None
    ratio: Optional[int] = Field(None, ge=0, le=100)

class FlagSubCategory(WithVerifiedFieldSchema):
    sub_category: Optional[str] = None
    description: Optional[str] = None
    severity: float = Field(..., ge=0.01)
    factors: Optional[List[Factor]] = None


class Flag(WithVerifiedFieldSchema):
    category: Optional[str] = None
    sub_categories: List[FlagSubCategory]
    description: Optional[str] = None
    severity: float = Field(..., ge=0.01)
    created_at: datetime = Field(
        default_factory=datetime.now,
        examples=[str(datetime.now().isoformat())]
    )
    updated_at: Optional[datetime] = Field(
        None, examples=[str(datetime.now().isoformat())]
    )

    @field_validator('severity')
    @classmethod
    def check_severity_decimal_places(cls, v):
        if not str(v).isdigit():
            decimal_places = len(str(v).split('.')[1])
            if decimal_places > 1:
                raise ValueError('severity must have only one decimal place')
        return v


class PersonFlag(SignAIghtSchema):
    illegal_immigration: Optional[Flag] = None
    islamic_extremism: Optional[Flag] = None
    substance: Optional[Flag] = None
    sexual_misconduct: Optional[Flag] = None
    bragging_exceptional_lifestyle: Optional[Flag] = None
    activism: Optional[Flag] = None
    terror_conviction: Optional[Flag] = None
    online_radicalization: Optional[Flag] = None
    pro_palestinian_statements: Optional[Flag] = None
    suicidal_ideation: Optional[Flag] = None
    watchlist_countries: Optional[Flag] = None
    anti_israel_statements:  Optional[Flag] = None
    anti_usa_statements:  Optional[Flag] = None
    weapons: Optional[Flag] = None


class FlagModel(Document, PersonFlag):
    person: Link[PersonModel]

    class Settings:
        name = "person_flags"
        indexes = [
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                ],
                name="flags_person",
                background=True,
                sparse=True
            ),
        ]
        use_revision = False

    async def _get_flag_person(self):
        person_id = None
        try:
            if isinstance(self.person, Link):
                person_id = self.person.ref.id
            elif isinstance(self.person, PersonModel):
                person_id = self.person.id
        except Exception:
            pass
        if person_id:
            return await PersonModel.get(person_id)
        return None

    @after_event(ValidateOnSave, Update, Replace, Insert)
    async def update_flags(self):
        person = await self._get_flag_person()
        if person:
            flag_fields = [
                "illegal_immigration",
                "islamic_extremism",
                "substance",
                "sexual_misconduct",
                "bragging_exceptional_lifestyle",
                "activism",
                "terror_conviction",
                "online_radicalization",
                "pro_palestinian_statements",
                "suicidal_ideation",
                "watchlist_countries",
                "anti_israel_statements",
                "anti_usa_statements",
                "weapons"
            ]
            flags = await self.find_one(
                FlagModel.person.id == person.id,
                fetch_links=True
            )
            if flags:
                flag_count = sum(
                    1 for field in flag_fields if
                    getattr(flags, field) is not None
                )

                if flag_count:
                    person.red_flags_count = flag_count
                    await person.save_changes()

    @before_event(ValidateOnSave)
    async def validate_not_all_none(self):
        """Prevent saving if all flag categories are None"""
        alert_fields = [
            self.illegal_immigration,
            self.islamic_extremism,
            self.substance,
            self.sexual_misconduct,
            self.bragging_exceptional_lifestyle,
            self.activism,
            self.terror_conviction,
            self.online_radicalization,
            self.pro_palestinian_statements,
            self.suicidal_ideation,
            self.watchlist_countries,
            self.anti_israel_statements,
            self.anti_usa_statements,
            self.weapons
        ]

        # If all categories are None, raise a validation error
        if all(field is None for field in alert_fields):
            raise ValueError(
                "At least one category must be set before saving.")
