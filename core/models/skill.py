from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema


class Endorser(SignAIghtSchema):
    urn: str = Field(
        examples=["urn:li:fsd_profile:ACoAAAAAE64BvLAaObOaPWa7Tvb4KqpsM-Seb_0"])
    name: str = Field(examples=["Heather Read, Ph.D."])


class Skill(SignAIghtSchema):
    skill_id: Optional[str] = Field(None, examples=["123456789"])
    name: str = Field(..., examples=["Python"])
    endorsers: Optional[List[Endorser]] = None
    endorser_count: Optional[int] = None
