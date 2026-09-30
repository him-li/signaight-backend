from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema


class PostLiker(SignAIghtSchema):
    instagram_id: str = Field(..., examples=["123456789"])
    instagram_username: Optional[str] = Field(None, examples=["johndoe"])
    instagram_full_name: Optional[str] = Field(None, examples=["John Doe"])
    instagram_is_private: Optional[bool] = Field(None, examples=[False])
    instagram_profile_picture: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"])

    # serializers
    @field_serializer("instagram_profile_picture", when_used="json-unless-none")
    def serialize_instagram_profile_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)
