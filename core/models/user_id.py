from typing import Optional, Type, List
from pydantic import Field, create_model

from core.utils.socials_list import SOCIALS

from .base import WithVerifiedFieldSchema, Variant


def make_user_id_model(
    socials: list[str],
    base_cls: type = WithVerifiedFieldSchema,
) -> Type[WithVerifiedFieldSchema]:
    def field_def(): return (Optional[List[str]], Field(
        default=None, examples=["123456789"]))
    fields = {"tgm_profile_user_id": field_def()}
    for s in socials:
        fields[f"{s}_user_id"] = field_def()

    def user_id__variants_field() -> tuple:
        return (
            Optional[List[Variant]],
            None,
        )

    # Define fields dynamically

    # Add special cases that are not in SOCIALS
    special_fields = {
        "user_id_variants": user_id__variants_field()
    }
    fields.update(special_fields)

    return create_model(
        "UserId",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )


UserId = make_user_id_model(SOCIALS)
