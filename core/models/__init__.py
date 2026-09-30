from typing import Optional
from beanie import Link

from .base import SignAIghtSchema, UUIDModel, Document, CreateUpdateMixin # noqa
from .candidate import (
    Candidate,
    CandidateModel as NonLinkedCandidateModel
)
from .mapping import Mapping, MappingModel
from .event import (SearchEvent, SearchEventModel, Event,
                    EventModel, Status, ActiveSearchEvent,
                    ActiveSearchEventModel,
                    RecalculationEvent, RecalculationEventModel)
from .person import (
    Person,
    PersonModel as NonLinkedPersonModel,
    PersonModelAuditLog as NonLinkedPersonModelAuditLog
)
from .project import Project, ProjectModel
from .biographic_details import BiographicDetails
from .physical_identifiers import PhysicalIdentifiers
from .network_signature import NetworkSignature
from .personal_details import PersonalDetails
from .flags import Flag, FlagModel as NonLinkedFlagModel
from .audit_log import UnionAuditLog

from .unstructured import WebSearch, WebSearchModel as NonLinkedWebSearchModel
from .alerts import Alerts, AlertsModel as NonLinkedAlertsModel
from .evaluation import (
    Evaluation,
    EvaluationModel as NonLinkedEvaluationModel
)
from .rule import Rule
from .resource_action_log import ResourceActionLog, ResourceActionLogModel
from .service_step_log import ServiceStepLog, ServiceStepLogModel
from .extracted import ExtractedPerson
from .auth_user import AuthUserModel


class AlertsModel(NonLinkedAlertsModel):
    person: Link["PersonModel"]


class EvaluationModel(NonLinkedEvaluationModel):
    person: Link["PersonModel"]


class FlagModel(NonLinkedFlagModel):
    person: Link["PersonModel"]


class PersonModel(NonLinkedPersonModel):
    project: Optional[Link[ProjectModel]] = None
    # TODO: backlinks do not work properly due bug:
    # https://github.com/roman-right/beanie/issues/749
    # alerts: Optional[BackLink[AlertsModel]] = Field(original_field="person")
    # evaluations: Optional[BackLink[EvaluationModel]] = Field(default=None,
    #  original_field="person")
    # flags: Optional[List[BackLink[FlagModel]]] = Field(
    # original_field="person")


class CandidateModel(NonLinkedCandidateModel):
    person: Link[PersonModel]


class PersonModelAuditLog(NonLinkedPersonModelAuditLog):
    entity: Link[PersonModel]


class WebSearchModel(NonLinkedWebSearchModel):
    person: Link[PersonModel]


AlertsModel.model_rebuild()
EvaluationModel.model_rebuild()
FlagModel.model_rebuild()


__all__ = [
    "SignAIghtSchema",
    "UUIDModel",
    "UnionAuditLog",
    "Document",
    "Project",
    "ProjectModel",
    "Person",
    "PersonModel",
    "PersonModelAuditLog",
    "Candidate",
    "CandidateModel",
    "Mapping",
    "MappingModel",
    "Event",
    "EventModel",
    "SearchEvent",
    "SearchEventModel",
    "Status",
    "BiographicDetails",
    "NetworkSignature",
    "PersonalDetails",
    "Flag",
    "FlagModel",
    "WebSearch",
    "WebSearchModel",
    "Alerts",
    "AlertsModel",
    "Evaluation",
    "EvaluationModel",
    "Rule",
    "ResourceActionLog",
    "ResourceActionLogModel",
    "PhysicalIdentifiers",
    "ActiveSearchEvent",
    "ActiveSearchEventModel",
    "RecalculationEvent",
    "RecalculationEventModel",
    "ServiceStepLog",
    "ServiceStepLogModel",
    "ExtractedPerson",
    "AuthUserModel"
]
