import datetime
from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema


class LicenceCertification(SignAIghtSchema):
    name: str = Field(..., help="Name of the licence or certification")
    issuer: Optional[str] = Field(
        None, help="issuer of the licence or certification")
    issue_date: Optional[datetime.date] = None
    expiration_date: Optional[datetime.date] = None
    issuer_photo: Optional[Union[S3Path, AnyHttpUrl]] = None
    issuer_url: Optional[AnyHttpUrl] = None

    @field_serializer("issuer_photo", when_used="json-unless-none")
    def serialize_issuer_photo_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)
