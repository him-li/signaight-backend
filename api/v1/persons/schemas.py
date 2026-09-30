from enum import Enum
import uuid
from datetime import datetime
from typing import Any, Dict, Literal, Optional, List, Union
from beanie import Link
from core.models.merge_metadata import MergeMode
from pydantic import AnyHttpUrl, Field, BaseModel, AnyUrl
from core.models import (
    SignAIghtSchema,
    UUIDModel,
    Project,
    Person,
    PersonModel,
    BiographicDetails,
    NetworkSignature,
    PersonalDetails
)
from core.models.name import Name, FullName, FirstName, LastName
from core.models.email import Email
from core.models.audit_log import AuditLogUser
from core.models.search_state import SearchState
from core.models.person import Scores, Compatibility, RecruitingSource, Comment

from ..projects.schemas import ProjectListRead, ProjectListView


class PersonListRead(UUIDModel):
    project: Optional[Link[ProjectListRead]] = None
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    personal_details: Optional[PersonalDetails] = None
    signaight_score: Optional[int] = Field(
        default=None, examples=[80], gte=0, lte=100)
    risk_score: Optional[int] = Field(
        default=0, examples=[80], gte=0, lte=100)
    compatibility: Optional[Compatibility] = None
    scores: Optional[Scores] = None
    demo_data: bool = False
    search_state: Optional[SearchState] = None
    last_update: Optional[datetime] = Field(
        default=None,
        examples=[str(datetime.utcnow().isoformat())])
    last_edited_by: Optional[AuditLogUser] = None
    recruiting_source: Optional[RecruitingSource] = RecruitingSource.application
    is_favorite: bool = False
    is_attention: bool = False
    comments: Optional[List[Comment]] = None
    red_flags_count: Optional[int] = None
    alerts_count: Optional[int] = None
    evaluation_count: Optional[int] = None


class PersonListView(PersonListRead):
    # Workaround only for query projection schema.
    # WARNING: Do not use alias for fastapi output validation schema
    id: uuid.UUID = Field(..., alias="_id")
    project: Optional[Link[ProjectListView]] = None


class PersonIdsSchema(SignAIghtSchema):
    persons: Optional[List[uuid.UUID]] = None


class PersonExportRead(UUIDModel):
    personal_details: Optional[PersonalDetails] = None
    signaight_score: Optional[int] = Field(
        default=None, examples=[80], gte=0, lte=100)
    compatibility: Optional[Compatibility] = None


class PersonExportView(PersonExportRead):
    id: uuid.UUID = Field(..., alias="_id")


class PersonRead(Person, UUIDModel):
    project: Optional[Link[Project]] = None


class NameOptional(Name):
    first_name: Optional[FirstName] = None
    last_name: Optional[LastName] = None
    full_name: Optional[FullName] = None


class PersonalDetailsUpdate(PersonalDetails):
    name: Optional[NameOptional] = None
    email: Optional[Email] = None


class PersonCreate(PersonModel):
    project_id: Optional[uuid.UUID] = None
    personal_details: Optional[PersonalDetailsUpdate] = None
    search_existing: bool = True


class PersonUpdate(Person):
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    personal_details: Optional[PersonalDetailsUpdate] = None
    remark: Optional[str] = None
    demo_data: Optional[bool] = False


class ActionMethod(str, Enum):
    All = 'all'
    In = 'in'
    Not_in = 'not_in'


class PersonDeleteBatch(BaseModel):
    method: ActionMethod = None
    person_ids: Optional[List[uuid.UUID]] = None
    project_id: uuid.UUID = None


class MergeResponse(BaseModel):
    merged_person_id: str
    merge_mode: MergeMode


Side = Literal["first", "second", "third"]


class ManualMergeSelection(BaseModel):
    selection: Dict[str, Side]


class MergeRequest(BaseModel):
    person_ids: List[str] = Field(
        ..., min_items=2, description="Persons to merge"
    )
    merge_mode: MergeMode
    project_id: str
    merged_person: Person


class ConnectionData(BaseModel):
    connection_url: Optional[AnyHttpUrl] = None
    connection_username: Optional[str] = None
    connection_platform: Optional[str] = None


class ConnectionCreate(BaseModel):
    connection_data: ConnectionData
    connection_type: str


class PersonFieldPatch(BaseModel):
    """
    Partial update for any person fields.

    - operation="replace"  → overwrites the target field (default)
    - operation="add"      → appends list items or deep-merges dicts/nested
                             models; falls back to replace for scalars
    """
    data: Dict[str, Any]
    operation: Literal["add", "replace"] = "replace"


class GraphConnection(BaseModel):
    project_id: Optional[str] = None
    selected_persons: Optional[List[str]] = None
    node_types: Optional[List[str]] = None
    edge_types: Optional[List[str]] = None
    min_degree: int = Field(default=2)
    connection_type: List[Literal["all", "bidirectional",
                                  "unidirectional", "likes", "groups"]] = Field(default=["all"])


class NodeData(BaseModel):
    id: str
    type: Literal[
        "person",
        "candidate",
        "hometown",
        "has_hometown",
        "interest_page",
        "interest_group",
        "interest_linkedin",
        "interest_xing",
        "social_connections",
        "work",
        "company",
        "education",
        "school",
        "check_ins",
        "check_in_place",
    ]
    name: Optional[str] = None
    picture: Optional[str] = None
    platform: Optional[str] = None
    url: Optional[Union[str | AnyUrl]] = None
    risk_score: Optional[int] = None
    signaight_score: Optional[float] = None
    matched_profiles: Optional[Dict[str, bool]] = None


class EdgeData(BaseModel):
    id: str
    source: str
    type: Literal["edge"]
    target: str
    relation: str
    label: Optional[str] = None


class GraphItem(BaseModel):
    data: Union[NodeData, EdgeData] = Field(..., discriminator='type')


class GraphResponse(BaseModel):
    result: List[GraphItem]
