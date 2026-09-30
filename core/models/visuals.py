from typing import Optional, Type, Union, List
from pydantic import (
    Field,
    AnyHttpUrl,
    create_model,
    field_serializer
)
from core.fields import S3Path, s3path_serializer
from core.utils.socials_list import SOCIALS

from .base import SignAIghtSchema, Variant, WithVerifiedFieldSchema


def make_profile_photo_model(
    socials: list[str],
    base_cls: type = SignAIghtSchema,
) -> Type[SignAIghtSchema]:
    """
    Dynamically create a model for all *_profile_picture fields.
    Each field supports AnyHttpUrl or S3Path and has consistent examples.
    """

    def photo_field() -> tuple:
        return (
            Optional[Union[AnyHttpUrl, S3Path]],
            Field(
                default=None,
                examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"],
            ),
        )
    def variants_field() -> tuple:
        return (
            Optional[List[Variant]],
            Field(
                default=None,
            ),
        )

    # Generate all standard fields dynamically
    fields = {f"{s}_profile_picture": photo_field() for s in socials}

    # Add custom / special fields manually
    fields.update({
        "profile_picture": photo_field(),
        "twitter_cover_photo": photo_field(),
        "eumw_profile_picture": photo_field(),
        "tgm_profile_picture": photo_field(),
        "profile_picture_variants": variants_field()
    })

    # Create the base model dynamically
    DynamicBase = create_model(
        "ProfilePhotoBase",
        __base__=base_cls,
        __module__="core.schemas.profile_photo",
        **fields,
    )

    # Extend to add serializer (since create_model can't attach decorators directly)
    class ProfilePhoto(DynamicBase):

        @field_serializer(*fields.keys(), when_used="json-unless-none")
        def serialize_profile_pictures_s3path(self, v: Union[S3Path, str, None], info):
            return s3path_serializer(v, info)

    return ProfilePhoto


ProfilePhoto = make_profile_photo_model(SOCIALS)

# TODO: update to support automatic model creating
class Visuals(WithVerifiedFieldSchema):
    profile_photo: Optional[ProfilePhoto] = None # type: ignore
    background_image: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    fb_cover_photo: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    twitter_cover_photo: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    linkedin_cover_photo: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    unmapped_photos: Optional[List[Union[List, AnyHttpUrl, S3Path]]] = None

    eumw_photos: Optional[List[Union[List, AnyHttpUrl, S3Path]]] = None

    interpol_photos: Optional[List[Union[List, AnyHttpUrl, S3Path]]] = None

    @field_serializer(
        "background_image",
        "fb_cover_photo",
        "twitter_cover_photo",
        "linkedin_cover_photo",
        "eumw_photos",
        "interpol_photos",
        "unmapped_photos",
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
