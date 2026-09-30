from typing import List, Optional
from datetime import datetime
from pydantic import Field

from core.models import CandidateModel
from api.filter import Filter


class CandidateFilter(Filter):
    search: Optional[str] = None

    primary: Optional[bool] = None
    search_id: Optional[str] = None
    searched_at: Optional[datetime] = None
    source: Optional[str] = None
    resource: Optional[str] = None
    ds_filter: Optional[bool] = None

    personal_details__name__full_name__facebook_full_name: Optional[
        str] = Field(default=None, alias='facebook_full_name')
    personal_details__name__full_name__linkedin_full_name: Optional[
        str] = Field(default=None, alias='linkedin_full_name')
    personal_details__name__full_name__instagram_full_name: Optional[
        str] = Field(default=None, alias='instagram_full_name')
    personal_details__name__full_name__facebook_full_name__like: Optional[
        str] = Field(default=None, alias='facebook_full_name__like')
    personal_details__name__full_name__linkedin_full_name__like: Optional[
        str] = Field(default=None, alias='linkedin_full_name__like')
    personal_details__name__full_name__instagram_full_name__like: Optional[
        str] = Field(default=None, alias='instagram_full_name__like')
    personal_details__name__full_name__facebook_full_name__ilike: Optional[
        str] = Field(default=None, alias='facebook_full_name__ilike')
    personal_details__name__full_name__linkedin_full_name__ilike: Optional[
        str] = Field(default=None, alias='linkedin_full_name__ilike')
    personal_details__name__full_name__instagram_full_name__ilike: Optional[
        str] = Field(default=None, alias='instagram_full_name__ilike')

    personal_details__name__first_name__f_name: Optional[str] = Field(
        default=None, alias='f_name')
    personal_details__name__last_name__l_name: Optional[str] = Field(
        default=None, alias='l_name')
    personal_details__email__email_address: Optional[str] = Field(
        default=None, alias='email_address')

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = CandidateModel
        search_field_name = "search"
        search_model_fields = [
            "primary",
            "search_id",
            "searched_at",
            "source_id",
            "source",
            "resource",
            "ds_filter",
            "person",
        ]
