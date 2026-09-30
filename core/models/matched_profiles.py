import uuid
from typing import List, Optional, Type, Union, Dict
from pydantic import AnyHttpUrl, field_validator, create_model, field_serializer, AnyUrl
from datetime import date

from core.utils.socials_list import PROFILE_SOCIALS, SOCIALS
from core.fields import S3Path, s3path_serializer
from .base import SignAIghtSchema


class PrimaryCandidateInfo(SignAIghtSchema):
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    creation_date: Optional[str] = None
    location: Optional[str] = None
    birthdate: Optional[date] = None
    profile_id: Optional[str] = None
    profile_url: Optional[List[Union[AnyUrl, str]]] = None
    profile_username: Optional[str] = None
    profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    full_name: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    friends: Optional[int] = None
    bio: Optional[str] = None
    
    @field_validator("profile_id", mode="before")
    @classmethod
    def cast_profile_id_to_str(cls, v):
        if v is None:
            return None

        if isinstance(v, int):
            return str(v)

        return v
    
    @field_serializer("profile_id")
    def serialize_profile_id(self, v):
        if v is None:
            return None
        return str(v)
    
    @field_validator("profile_url", mode="before")
    @classmethod
    def normalize_profile_url(cls, value):
        if value is None:
            return None

        if not isinstance(value, list):
            value = [value]

        normalized = []

        for item in value:
            if item is None:
                continue

            if isinstance(item, AnyUrl):
                normalized.append(item)
                continue

            if isinstance(item, str):
                try:
                    validated = AnyUrl(item)
                    normalized.append(validated)
                except Exception:
                    normalized.append(item)

        return normalized or None

    @field_serializer(
        "profile_picture",
        when_used="json-unless-none",
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


class SourceInfo(SignAIghtSchema):
    primary_candidate: Optional[Dict[Union[uuid.UUID,
                                           str], PrimaryCandidateInfo]] = None
    candidates_count: int = 0


def make_matched_profiles_model(
    socials: list[str],
    base_cls: type = SignAIghtSchema,
) -> Type[SignAIghtSchema]:
    def field_def(): return (Optional[SourceInfo], None)
    fields = {}
    for s in socials:
        fields[s] = field_def()

    return create_model(
        "MatchedProfiles",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )


MatchedProfiles = make_matched_profiles_model(
    SOCIALS + PROFILE_SOCIALS + ['telegram'])
