from pydantic import Field
from typing import List, Literal, Optional
from uuid import UUID

from core.models import PersonModel, PersonModelAuditLog
from core.models.search_state import SearchStatus
from core.models.person import Compatibility
from core.models.audit_log import ActionsEnum
from api.filter import Filter


class PersonsFilter(Filter):
    search: Optional[str] = None
    id__in: Optional[List[UUID]] = Field(
        default=None, alias='ids__in')
    project__id: Optional[UUID] = None
    project__project_platform: Optional[str] = None
    signaight_score: Optional[int] = None
    risk_score: Optional[int] = None
    flags__in: Optional[
        List[
            Literal[
                "illegal_immigration",
                "islamic_extremism",
                "substance",
                "sexual_misconduct",
                "bragging_exceptional_lifestyle",
                "activism",
                "terror_conviction",
                "online_radicalization",
                "pro_palestinian_statements",
                "suicidal_ideation",
                "watchlist_countries",
                "anti_israel_statements",
                "anti_usa_statements",
                "weapons",
            ]
        ]
    ] = None
    personal_details__name__first_name__f_name: Optional[str] = Field(
        default=None, alias='f_name')
    personal_details__name__last_name__l_name: Optional[str] = Field(
        default=None, alias='l_name')
    personal_details__email__email_address: Optional[str] = Field(
        default=None, alias='email_address')
    personal_details__location__location: Optional[str] = Field(
        default=None, alias='location')
    personal_details__name__first_name__f_name__like: Optional[str] = Field(
        default=None, alias='f_name__like')
    personal_details__name__last_name__l_name__like: Optional[str] = Field(
        default=None, alias='l_name__like')
    personal_details__email__email_address__like: Optional[str] = Field(
        default=None, alias='email_address__like')
    personal_details__location__location__like: Optional[str] = Field(
        default=None, alias='location__like')
    personal_details__name__first_name__f_name__ilike: Optional[str] = Field(
        default=None, alias='f_name__ilike')
    personal_details__name__last_name__l_name__ilike: Optional[str] = Field(
        default=None, alias='l_name__ilike')
    personal_details__email__email_address__ilike: Optional[str] = Field(
        default=None, alias='email_address__ilike')
    personal_details__location__location__ilike: Optional[str] = Field(
        default=None, alias='location__ilike')
    personal_details__name__first_name__f_name__in: Optional[str] = Field(
        default=None, alias='f_name__in')
    personal_details__name__last_name__l_name__in: Optional[str] = Field(
        default=None, alias='l_name__in')
    personal_details__email__email_address__in: Optional[str] = Field(
        default=None, alias='email_address__in')
    personal_details__location__location__in: Optional[str] = Field(
        default=None, alias='location__in')
    demo_data: Optional[bool] = None
    search_state__is_done: Optional[bool] = None
    search_state__status: Optional[SearchStatus] = Field(
        default=None, alias='status')
    search_state__status__in: Optional[str] = Field(
        default=None, alias='status__in')
    compatibility: Optional[Compatibility] = None
    compatibility__in: Optional[str] = Field(
        default=None, alias='compatibilities__in')
    signaight_score__gte: Optional[int] = None
    signaight_score__lt: Optional[int] = None
    signaight_score__lte: Optional[int] = None
    risk_score__gte: Optional[int] = None
    risk_score__lt: Optional[int] = None
    risk_score__lte: Optional[int] = None
    is_favorite: Optional[bool] = None
    is_attention: Optional[bool] = None
    # with_red_flags: Optional[bool] = None
    # with_alerts: Optional[bool] = None

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = PersonModel
        search_field_name = "search"
        search_model_fields = [
            "personal_details__email__email_address",
            "personal_details__name__first_name__f_name",
            "personal_details__name__first_name__l_name"
        ]


class PersonsExportFilter(PersonsFilter):
    project__id: UUID


class PersonsFilterByProject(PersonsFilter):
    pass


class PersonHistoryFilter(Filter):
    action: Optional[ActionsEnum] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = PersonModelAuditLog
        search_model_fields = ["action"]
