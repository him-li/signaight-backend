from pydantic import Field
from typing import Optional, List

from .base import WithVerifiedFieldSchema, Variant
from .website import Website


class Websites(WithVerifiedFieldSchema):
    websites: Optional[List[Website]] = Field(
        None, help="Person's websites list")
    linkedin_websites: Optional[List[Website]] = Field(
        None, help="Person's LinkedIn websites list")
    website_variants: Optional[List[Variant]] = None
