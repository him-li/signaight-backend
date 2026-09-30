from pydantic import Field
from typing import Optional, List

from .base import WithVerifiedFieldSchema, Variant
from .language import Language


class Languages(WithVerifiedFieldSchema):
    languages: Optional[List[Language]] = Field(
        None, help="List of Person's languages")
    fb_languages: Optional[List[Language]] = Field(
        None, help="List of Person's Facebook languages")
    li_languages: Optional[List[Language]] = Field(
        None, help="List of Person's Linkedin languages")
    xing_languages: Optional[List[Language]] = Field(
        None, help="List of Person's Xing languages")
    eumw_languages: Optional[List[Language]] = Field(
        None, help="List of Person's Eu Most Wanted languages")
    interpol_languages: Optional[List[Language]] = Field(
        None, help="List of Person's Interpol languages")
    microsoft_language: Optional[Language] = Field(
        None, help="Person's Microsoft language")
    myfitnesspal_language: Optional[Language] = Field(
        None, help="Person's Myfitnesspal language")
    duolingo_learning: Optional[str] = None
    language_variants: Optional[List[Variant]] = None
