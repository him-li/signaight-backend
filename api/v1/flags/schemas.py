import uuid
from beanie import Link
from pydantic import BaseModel, AnyHttpUrl, field_serializer, Field
from typing import List, Union, Optional

from core.fields import s3path_serializer, S3Path
from core.models import FlagModel, PersonModel
from core.models.flags import PersonFlag


class FlagRead(FlagModel):
    # TODO: make it work as alias to respect schema
    # id: uuid.UUID = Field(alias='id')
    pass


class FlagCreate(PersonFlag):
    person:  Link[PersonModel]
    pass


class FlagUpdate(PersonFlag):
    pass


class PersonInfo(BaseModel):
    id: uuid.UUID
    profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    flag_images: Optional[List[Union[S3Path, AnyHttpUrl]]] = None

    @field_serializer(
        'profile_picture',
        'flag_images',
        when_used="json-unless-none"
    )
    def serialize_visuals_images_or_photos_s3path(
            self,
            v: S3Path | str | list | None,
            info):
        if isinstance(v, list):
            v_urls = []
            for value in v:
                v_url = s3path_serializer(value, info)
                if v_url:
                    v_urls.append(v_url)
            return v_urls
        return s3path_serializer(v, info)


class FlagPersonInfo(BaseModel):
    count: int = 0
    persons: List[PersonInfo] = Field(default_factory=list)


class PersonFlagStats(BaseModel):
    illegal_immigration: FlagPersonInfo
    islamic_extremism: FlagPersonInfo
    substance: FlagPersonInfo
    sexual_misconduct: FlagPersonInfo
    bragging_exceptional_lifestyle: FlagPersonInfo
    activism: FlagPersonInfo
    terror_conviction: FlagPersonInfo
    online_radicalization: FlagPersonInfo
    pro_palestinian_statements: FlagPersonInfo
    suicidal_ideation: FlagPersonInfo
    watchlist_countries: FlagPersonInfo
    anti_israel_statements: FlagPersonInfo
    anti_usa_statements: FlagPersonInfo
    weapons: FlagPersonInfo


RedFlagStats = PersonFlagStats
