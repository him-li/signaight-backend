from pydantic import Field
from typing import Optional, List, Union

from .base import SignAIghtSchema


class Properties(SignAIghtSchema):
    mapbox_id: Optional[str] = None
    wikidata: Optional[str] = None
    short_code: Optional[str] = None
    place_name: Optional[str] = None
    location_type: Optional[str] = None
    date: Optional[str] = None


class Geometry(SignAIghtSchema):
    coordinates: List[Union[float, List[float]]] = Field(
        min_length=2,
        max_length=2)
    type: str


class Features(SignAIghtSchema):
    type: str
    properties: Optional[Properties] = None
    geometry: Geometry
    id: str


class GeoTrace(SignAIghtSchema):
    features: List[Features]
    type: str = Field(
        help="type of incoming GeoJSON data",
        default="FeatureCollection")
