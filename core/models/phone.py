from .base import WithVerifiedFieldSchema, Variant
from typing import List, Optional, Union
from pydantic import Field


class Phone(WithVerifiedFieldSchema):
    phones: Optional[List[str]] = Field(
        None, help="List of the person phones collected from APIs")
    fb_phone: Optional[Union[str, List[str]]] = None
    associated_phones: Optional[List[str]] = None
    discovery_phones: Optional[List[str]] = None
    fb_phones: Optional[List[str]] = None
    fb_phones_in_whatsapp: Optional[List[str]] = None
    linkedin_phone_numbers: Optional[List[str]] = None
    fb_phone_part: Optional[List[str]] = None
    xing_business_phone: Optional[str] = None
    apple_phone_part: Optional[List[str]] = None
    microsoft_phone_part: Optional[List[str]] = None
    samsung_phone_part: Optional[List[str]] = None
    paypal_phone_part: Optional[List[str]] = None
    ebay_phone_part: Optional[List[str]] = None
    phone_variants: Optional[List[Variant]] = None
