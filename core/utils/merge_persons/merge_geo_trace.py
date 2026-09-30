from typing import List, Optional

from core.models.geo_trace import GeoTrace
from core.models.person import PersonModel


def merge_geo_trace(persons: List[PersonModel]) -> Optional[GeoTrace]:
    features = []

    for p in persons:
        if p.geo_trace and p.geo_trace.features:
            features.extend(p.geo_trace.features)

    if not features:
        return None

    return GeoTrace(type="FeatureCollection", features=features)
