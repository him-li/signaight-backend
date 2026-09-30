from typing import Optional

from .base import SignAIghtSchema


class XingContact(SignAIghtSchema):
    address: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None


class XingContactDetails(SignAIghtSchema):
    business: Optional[XingContact] = None
    private: Optional[XingContact] = None
