from typing import Optional, List

from core.fields import EmailStrMasked
from .base import WithVerifiedFieldSchema, Variant


class Email(WithVerifiedFieldSchema):
    email_address: Optional[List[EmailStrMasked]] = None
    associated_email: Optional[List[EmailStrMasked]] = None
    fb_email_address: Optional[EmailStrMasked] = None
    linkedin_email_address: Optional[EmailStrMasked] = None
    fb_email_part: Optional[List[str]] = None
    xing_business_email: Optional[EmailStrMasked] = None
    xing_private_email: Optional[EmailStrMasked] = None
    apple_email_part: Optional[List[str]] = None
    apple_email: Optional[EmailStrMasked] = None
    microsoft_email_part: Optional[List[str]] = None
    paypal_email_part: Optional[List[str]] = None
    email_variants: Optional[List[Variant]] = None
