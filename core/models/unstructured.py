from beanie import (before_event, Insert, Replace,
                    Update, SaveChanges, ValidateOnSave)
from typing import Optional, List, Union
from pydantic import (
    AnyHttpUrl,
    field_serializer
)
from pymongo import IndexModel, ASCENDING

from core.fields import S3Path, s3path_serializer

from .base import WithVerifiedFieldSchema, Document


class WebSearch(WithVerifiedFieldSchema):
    search_id: Optional[str] = None
    title: str
    # TODO: investigate possibilty to strict source field as AnyHttpUrl only
    source: Union[AnyHttpUrl, str]
    preview: Optional[str] = None
    content: Optional[str] = None
    images: Optional[List[Union[AnyHttpUrl, S3Path]]] = None
    is_match: Optional[bool] = None

    @field_serializer("images", when_used="json-unless-none")
    def serialize_websearch_images_s3path(self, v: S3Path | str | list | None, info):
        if isinstance(v, list):
            v_urls = []
            for value in v:
                v_url = s3path_serializer(value, info)
                if v_url:
                    v_urls.append(v_url)

            return v_urls
        return s3path_serializer(v, info)


class WebSearchModel(WebSearch, Document):

    class Settings:
        name = "web_searches"
        indexes = [
            IndexModel(
                [
                    ("search_id", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("search_id", ASCENDING),
                    ("person.$id", ASCENDING),
                    ("title", ASCENDING),
                    ("source", ASCENDING),
                ],
                name="search_id_websearch_person_title_source_UNIQUE",
                unique=True
            ),
        ]

    @before_event(Insert, Replace, Update, SaveChanges, ValidateOnSave)
    def remove_empty_images(self):
        if self.images and isinstance(self.images, list):
            for i, image in enumerate(self.images):
                if not isinstance(image, S3Path):
                    self.images[i] = S3Path.validate(image)
            self.images = [image for image in self.images if image]
