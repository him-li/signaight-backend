from typing import Optional, Any, List
from pydantic import Field


from .base import WithVerifiedFieldSchema, Variant

from .physical_identifiers import PhysicalIdentifiers


class EumwDetails(WithVerifiedFieldSchema):
    is_dangerous: Optional[bool] = Field(None, examples=[True])
    ehtnic_origin: Optional[str] = Field(None, examples=["African"])
    date_published: Optional[str] = Field(
        None,
        examples=["on September 27, 2022, last modified on February 2, 2023"])
    is_reward: Optional[bool] = Field(None, example=[True])
    crime: Optional[str] = Field(None, example=["Trafficking in human beings"])
    info: Optional[str] = Field(None, examples=["Unstructured info paragraph"])


class ArrestWarrant(WithVerifiedFieldSchema):
    charge: Optional[str] = Field(None, examples=["Fraud"])
    issuing_country: Optional[str] = Field(None, examples=["France"])
    charge_translation: Optional[str] = Field(
        None, help="Translation of charge")


class InterpolDetails(WithVerifiedFieldSchema):
    arrest_warrants: Optional[List[ArrestWarrant]] = None
    interpol_entity_id: Optional[str] = Field(None, examples=["2019-91101"])


class AdditionalDetails(WithVerifiedFieldSchema):
    additional_person_details: Optional[Any] = None
    fb_insterested_in: Optional[Any] = None
    fb_political_views: Optional[Any] = None
    fb_religious_views: Optional[Any] = None
    eumw_details: Optional[EumwDetails] = None
    interpol_details: Optional[InterpolDetails] = None
    physical_identifiers: Optional[PhysicalIdentifiers] = None
    variants: Optional[List[Variant]] = None
