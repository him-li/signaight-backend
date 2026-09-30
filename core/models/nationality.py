from typing import Optional, List
from pydantic import Field

from .base import WithVerifiedFieldSchema, Variant


class Nationality(WithVerifiedFieldSchema):
    nationalities: Optional[List[str]] = Field(
        None, help="List of Person's nationalities")

    eumw_nationality: Optional[str] = Field(None, examples=["Nigerian"])
    interpol_nationalities: Optional[List[str]] = Field(
        None, examples=[['Israel', 'France'],])
    nationality_variants: Optional[List[Variant]] = None
