from typing import Optional, Type, Union, List
from pydantic import AnyHttpUrl, AnyUrl, Field, create_model, field_validator

from core.utils.socials_list import SOCIALS
from core.utils.url_normalize import url_normalize

from .base import WithVerifiedFieldSchema, Variant


def make_url_model(
    socials: list[str],
    base_cls: type = WithVerifiedFieldSchema,
) -> Type[WithVerifiedFieldSchema]:
    """
    Dynamically create a URL model with fields like:
      facebook_profile_url, instagram_profile_url, etc.
    Supports list of URLs.
    """

    # default field definition for URL types
    def url_field() -> tuple:
        return (
            Optional[List[AnyHttpUrl]],
            Field(default=None),
        )

    def variants_url_field() -> tuple:
        return (
            Optional[List[Variant]],
            None,
        )

    # Define fields dynamically
    fields = {}
    for s in socials:
        fields[f"{s}_profile_url"] = url_field()

    # Add special cases that are not in SOCIALS
    special_fields = {
        "criminal_db_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "legal_db_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "instagram_fb_link_on_profile": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "fb_instagram_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "fb_linkedin_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "fb_twitter_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "tiktok_profile_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "xing_profile_url": (
            Optional[Union[List[AnyHttpUrl],AnyHttpUrl]],
            Field(default=None)),
        "skype_profile_url": (
            Optional[Union[List[Union[AnyUrl, str]], AnyUrl]],
            Field(default=None)),
        "duolingo_profile_url": (Optional[Union[List[AnyUrl], AnyUrl]],
                                 Field(default=None)),
        "icq_profile_url": (Optional[Union[List[AnyUrl], AnyUrl]],
                            Field(default=None)),
        "profile_url_variants": variants_url_field()
    }
    fields.update(special_fields)

    DynamicURLBase = create_model(
        "URLBase",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )

    # Extend it to register validators
    class URL(DynamicURLBase):
        @field_validator("linkedin_profile_url", mode="before")
        @classmethod
        def sanitize_linkedin_profile_url(cls, v):
            if not v:
                return v
            if not isinstance(v, list):
                v = [v]
            try:
                v = [url_normalize(url, path_chunks_limit=2) for url in v]
            except Exception:
                pass
            return v

    return URL


# Example usage:
URL = make_url_model(SOCIALS)
