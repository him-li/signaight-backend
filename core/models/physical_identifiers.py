from typing import Optional, List
from pydantic import Field

from .base import WithVerifiedFieldSchema


class Height(WithVerifiedFieldSchema):
    eumw_height: Optional[str] = Field(None, example=['184 cm'])
    interpol_height: Optional[str] = Field(None, examples=['1.84'])


class EyeColor(WithVerifiedFieldSchema):
    eumw_eye_color: Optional[str] = Field(None, examples=["Brown"])
    interpol_eye_color: Optional[list[str]] = Field(None, examples=["BRO"])


class Identifiers(WithVerifiedFieldSchema):
    eumw_identifiers: Optional[List[str]] = Field(
        None, examples=[["Body - Tattoo(s) Abstract Design"],])
    interpol_identifiers: Optional[str] = Field(
        None,
        exmaples=[
            'PALMER has a deformed left thumb.'
            ' PALMER may be 175 to 178 centimeters tall and'
            ' may be balding or may be bald.',])


class Weight(WithVerifiedFieldSchema):
    interpol_weight: Optional[str] = Field(None, examples=['80'])


class HairColor(WithVerifiedFieldSchema):
    interpol_hair_color: Optional[list[str]] = Field(None, examples=["BLA"])


class PhysicalIdentifiers(WithVerifiedFieldSchema):
    height: Optional[Height] = None
    weight: Optional[Weight] = None
    eye_color: Optional[EyeColor] = None
    hair_color: Optional[HairColor] = None
    identifiers: Optional[Identifiers] = None
