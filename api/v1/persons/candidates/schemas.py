import uuid
from beanie import Link
from pydantic import Field
from typing import Optional
from datetime import datetime

from core.models import (
    UUIDModel,
    Candidate,
    BiographicDetails,
    NetworkSignature,
    PersonalDetails)


class CandidateRead(Candidate, UUIDModel):
    pass


class PersonListRead(UUIDModel):
    pass


class CandidateListRead(Candidate, UUIDModel):
    person: Optional[Link[PersonListRead]] = None


class CandidateListView(CandidateListRead):
    id: uuid.UUID = Field(..., alias="_id")


class CandidateCreate(Candidate):
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    search_id: Optional[str] = Field(None, examples=[
        "55c05aa4-2aee-4762-b966-b2dc50928cd5"])
    searched_at: Optional[datetime] = None
    source: Optional[str] = Field(None, examples=["facebook"])


class CandidateUpdate(Candidate):
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    personal_details: Optional[PersonalDetails] = None
