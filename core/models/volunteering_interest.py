from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema
from .causes import Cause


class VolunteeringInterest(SignAIghtSchema):
    supported_non_profits: Optional[str] = Field(
        None, examples=["supported_non_profits"])
    company_id: Optional[str] = Field(None, examples=["123456789"])
    company_name: str = Field(..., examples=["company_name"])
    supported_predefined_causes: Optional[List[Cause]] = Field(None, examples=[[
        "cause"]])
    supported_user_defined_causes: Optional[List[str]] = Field(None, examples=[[
        "cause"]])
