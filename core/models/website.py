from pydantic import field_validator, Field, AnyHttpUrl, field_serializer
from typing import Optional, List, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema


class Website(SignAIghtSchema):
    category: Optional[str] = Field(None, examples=["category"])
    label: Optional[str] = Field(None, examples=["label"])
    url: Optional[Union[AnyHttpUrl, str]] = Field(..., examples=["url"])
    images: Optional[List[Union[S3Path, AnyHttpUrl]]] = Field(
        None, help="List of images associated with the website")

    @field_serializer("images", when_used="json-unless-none")
    def serialize_website_images_s3path(self, v: S3Path | str | list | None, info):
        if isinstance(v, list):
            v_urls = []
            for value in v:
                v_url = s3path_serializer(value, info)
                if v_url:
                    v_urls.append(v_url)

            return v_urls
        return s3path_serializer(v, info)

    @field_validator('url', mode="before")
    @classmethod
    def correct_url_schema(cls, v):
        if isinstance(v, str) and not v.startswith('http'):
            return f"http://{v}"
        return v
