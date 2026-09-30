from typing import Optional, List
from pydantic import Field

from .base import WithVerifiedFieldSchema, Variant


class Gender(WithVerifiedFieldSchema):
    gender: Optional[str] = Field(None, examples=["male"])
    fb_gender: Optional[str] = Field(None, examples=["MALE"])
    truecaller_gender: Optional[str] = Field(None, examples=["MALE"])
    goodreads_gender: Optional[str] = Field(None, examples=["MALE"])
    deezer_gender: Optional[str] = Field(None, examples=["MALE"])
    foursquare_gender: Optional[str] = Field(None, examples=["MALE"])
    eumw_gender: Optional[str] = Field(None, examples=["Male"])
    interpol_gender: Optional[str] = Field(None, examples=["MALE"])
    microsoft_gender: Optional[str] = Field(None, examples=["MALE"])
    myfitnesspal_gender: Optional[str] = Field(None, examples=["MALE"])
    gender_variants: Optional[List[Variant]] = None
