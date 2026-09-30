from typing import Union, Optional
from pydantic import ConfigDict, AnyHttpUrl, field_validator, field_serializer

from core.models import SignAIghtSchema, Document
from core.fields import S3Path, s3path_serializer


class PhotoDoc(SignAIghtSchema):
    photo: Union[S3Path, AnyHttpUrl]

    # serializers
    @field_serializer('photo', when_used="json-unless-none")
    def serialize_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class PictureNestedDoc(PhotoDoc):  # PhotoDoc
    alt: str


class PictureParentDoc(Document):
    name: str
    picture_nested_doc: Optional[PictureNestedDoc]


class HybridStorage(PhotoDoc, Document):
    # NOTE: we do not set bson_encoder config here cause model
    # inherits PhotoDoc parent class as top level model
    pass
