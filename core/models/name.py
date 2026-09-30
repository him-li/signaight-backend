from pydantic import Field, create_model, field_validator
from typing import Optional, List, Type

from core.utils.socials_list import SOCIALS

from .base import SignAIghtSchema, WithVerifiedFieldSchema, Variant


def make_first_name_model(
    socials: list[str],
    base_cls: type = SignAIghtSchema,
) -> Type[SignAIghtSchema]:
    def field_def(): return (Optional[str], Field(
        default=None, examples=["John"]))

    def variant_field(): return (Optional[List[Variant]], None)
    fields = {"f_name": field_def(), "f_name_variants": variant_field()}
    for s in socials:
        fields[f"{s}_f_name"] = field_def()

    return create_model(
        "FirstName",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )


FirstName = make_first_name_model(SOCIALS, base_cls=SignAIghtSchema)


def make_last_name_model(
    socials: list[str],
    base_cls: type = SignAIghtSchema,
) -> Type[SignAIghtSchema]:
    def field_def(): return (Optional[str], Field(
        default=None, examples=["Doe"]))

    def variant_field(): return (Optional[List[Variant]], None)
    fields = {"l_name": field_def(), "l_name_variants": variant_field()}
    for s in socials:
        fields[f"{s}_l_name"] = field_def()

    return create_model(
        "LastName",
        __base__=base_cls,
        __module__=__name__,
        **fields,
    )


LastName = make_last_name_model(SOCIALS, base_cls=SignAIghtSchema)


class FullName(SignAIghtSchema):
    full_name: Optional[str] = Field(None, examples=["John Doe"])
    linkedin_full_name: Optional[str] = Field(None, examples=["John Doe"])
    facebook_full_name: Optional[str] = Field(None, examples=["John Doe"])
    instagram_full_name: Optional[str] = Field(None, examples=["John Doe"])
    tiktok_full_name: Optional[str] = Field(None, examples=["John Doe"])
    twitter_full_name: Optional[str] = Field(None, examples=["John Doe"])
    xing_full_name: Optional[str] = Field(None, examples=["John Doe"])
    eumw_full_name: Optional[str] = Field(None, examples=["John Doe"])
    interpol_full_name: Optional[str] = Field(None, examples=["John Doe"])
    full_name_variants: Optional[List[Variant]] = None

    # TODO: we should find where is a problem in code
    # where full_name provided as list
    @field_validator('full_name', mode='before')
    @classmethod
    def full_name_as_string(cls, value: str | List) -> str:
        if isinstance(value, list):
            value = " ".join(value)
        return value


class MiddleName(SignAIghtSchema):
    mid_name: Optional[str] = Field(None, examples=["Jack"])
    mid_name_variants: Optional[List[Variant]] = None


class Nickname(SignAIghtSchema):
    other_names: Optional[List] = Field(None, examples=["johnnie"])
    fb_nicknames: Optional[List[str]] = None
    fb_other_names: Optional[str] = Field(None, examples=['johnnie'])
    other_names_variants: Optional[List[Variant]] = None


class Name(WithVerifiedFieldSchema):
    first_name: Optional[FirstName] = None  # type: ignore
    last_name: Optional[LastName] = None  # type: ignore
    full_name: Optional[FullName] = None
    middle_name: Optional[MiddleName] = None
    nickname: Optional[Nickname] = None
