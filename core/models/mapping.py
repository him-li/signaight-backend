from pydantic import Field
from typing import Dict

from .base import SignAIghtSchema, Document


class Mapping(SignAIghtSchema):
    source: str = Field(..., examples=["Facebook"])
    resource: str = Field(..., examples=["social_links"])
    map: Dict


class MappingModel(Document, Mapping):
    class Settings:
        name = "mappings"
        use_revision = False
