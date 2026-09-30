from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union
from datetime import datetime

from core.fields import S3Path, s3path_serializer
from .base import SignAIghtSchema


class ProfilePicture(SignAIghtSchema):
    created: datetime = Field(..., examples=[str(datetime.utcnow().isoformat())])
    deleted: Optional[datetime] = Field(
        None, examples=[str(datetime.utcnow().isoformat())])
    display_name: Optional[str] = Field(None, examples=["display_name"])
    last_modified: datetime = Field(...,
                                    examples=[str(datetime.utcnow().isoformat())])
    original_image: Union[AnyHttpUrl, S3Path]
    photo_filter_edit_info: Optional[str] = Field(
        None, examples=["photo_filter_edit_info"]
    )

    @field_serializer("original_image", when_used="json-unless-none")
    def serialize_profile_original_image_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)
