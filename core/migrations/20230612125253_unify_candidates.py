# from ..models import
import uuid

from beanie import Link, UnionDoc, Document, free_fall_migration
from datetime import datetime
from docarray.typing import ImageUrl
from pydantic import BaseModel, Field, AnyHttpUrl, EmailStr
from typing import Optional

from core.models import PersonModel


class OldCandidate(BaseModel):
    name: Optional[str] = Field(None, examples=["Jhon Doe"])  # data.user.name
    email: Optional[EmailStr] = Field(None, examples=["jhon.doe@example.tld"])
    profile_url: Optional[AnyHttpUrl] = Field(
        None, examples=["https://linkedin.com/ph"])
    profile_photo: Optional[ImageUrl] = Field(
        None, examples=["https://d3mrlwp8riu1ry.cloudfront.net/images/82.jpg"])
    primary: bool = False
    search_id: Optional[str] = Field(None, min_length=32, max_length=32)
    searched_at: Optional[datetime] = None
    person: Optional[Link[PersonModel]] = None


class OldCandidateModel(UnionDoc):
    class Settings:
        name = "candidates"  # Collection name
        class_id = "_class_id"


class OldFacebookCandidateModel(Document, OldCandidate):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    remote_id: str  # data.user.id
    gender: Optional[str] = None  # ...gender, Probably Enum

    class Settings:
        name = "FacebookCandidate"
        union_doc = OldCandidateModel


class OldInstagramCandidateModel(Document, OldCandidate):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    remote_id: str  # data.pk
    biography: Optional[str] = None  # data.biography

    class Settings:
        name = "InstagramCandidate"
        union_doc = OldCandidateModel


class CandidateModel(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    # Candidate
    primary: bool = False
    search_id: Optional[str] = Field(min_length=32, max_length=32)
    searched_at: Optional[datetime]
    source_id: str = Field(..., examples=["6464188a76bb36dbecacf789"])
    source: str = Field(..., examples=["Facebook"])
    person: Optional[Link[PersonModel]]
    f_name: Optional[str] = Field(examples=["John"])
    l_name: Optional[str] = Field(examples=["Doe"])
    # SerchResponseSchema
    name: Optional[str] = Field(examples=["Jhon Doe"])  # data.user.name
    email: Optional[EmailStr] = Field(examples=["jhon.doe@example.tld"])
    profile_url: Optional[AnyHttpUrl] = Field(
        examples=["https://linkedin.com/ph"])
    profile_photo: Optional[ImageUrl] = Field(
        examples=["https://d3mrlwp8riu1ry.cloudfront.net/images/82.jpg"])

    class Settings:
        name = "candidates"
        use_revision = False


class Forward:
    @free_fall_migration(
        document_models=[
            OldCandidateModel,
            OldFacebookCandidateModel,
            OldInstagramCandidateModel,
            CandidateModel
        ]
    )
    async def multimodel_to_allinone(self, session):
        async for old_candidate in OldFacebookCandidateModel.find_all():
            data = old_candidate.model_dump()
            data["source_id"] = old_candidate.remote_id
            data["source"] = "Facebook"
            new_candidate = CandidateModel(**data)
            await new_candidate.replace(session=session)
        async for old_candidate in OldInstagramCandidateModel.find_all():
            data = old_candidate.model_dump()
            data["source_id"] = old_candidate.remote_id
            data["source"] = "Instagram"
            new_candidate = CandidateModel(**data)
            await new_candidate.replace(session=session)


class Backward:
    @free_fall_migration(
        document_models=[
            OldCandidateModel,
            OldFacebookCandidateModel,
            OldInstagramCandidateModel,
            CandidateModel
        ]
    )
    async def allinone_to_multimodel(self, session):
        async for new_candidate in CandidateModel.find({"source": "Facebook"}):
            data = new_candidate.model_dump()
            data["remote_id"] = new_candidate.source_id
            old_candidate = OldFacebookCandidateModel(**data)
            await new_candidate.delete(session=session)
            await old_candidate.insert(session=session)
        async for new_candidate in CandidateModel.find(
                {"source": "Instagram"}):
            data = new_candidate.model_dump()
            data["remote_id"] = new_candidate.sorce_id
            old_candidate = OldInstagramCandidateModel(**data)
            await new_candidate.delete(session=session)
            await old_candidate.insert(session=session)
