from typing import Optional, List, Type
from pydantic import Field, create_model
from .base import WithVerifiedFieldSchema, Variant
from core.utils.socials_list import SOCIALS


def make_username_model(
    socials: list[str],
    base_cls: type = WithVerifiedFieldSchema,
) -> Type[WithVerifiedFieldSchema]:
    """
    Dynamically generate username fields for all socials.
    Adds default example and special aliases.
    """

    # Each field uses the same base definition
    def username_field() -> tuple:
        return (
            Optional[List[str]],
            Field(default=None, examples=["johndoe"]),
        )

    def username_variants_field() -> tuple:
        return (Optional[List[Variant]], None)

    # Create fields for all socials
    fields = {f"{s}_username": username_field() for s in socials}

    # Add extra aliases that don’t follow the same pattern
    fields.update({
        "linkedin_twitter_aliases": (
            Optional[List],
            Field(default=None, examples=[["johndoe"]]),
        ),
        "fb_instagram_username": username_field(),
        "fb_linkedin_username": username_field(),
        "fb_twitter_username": username_field(),
        "tgm_profile_username": username_field(),
        "username_variants": username_variants_field()
    })

    # Dynamically create the model
    model = create_model(
        "Username",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )

    return model


# ✅ Example usage
Username = make_username_model(SOCIALS)
