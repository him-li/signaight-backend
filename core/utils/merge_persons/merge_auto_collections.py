from typing import List
from core.models import PersonModel
from core.utils.merge_persons.merge_connections import merge_connections
from core.utils.merge_persons.merge_geo_trace import merge_geo_trace
from core.utils.merge_persons.merge_interests import merge_interests
from core.utils.merge_persons.merge_posts import merge_posts


def merge_auto_collections(persons: List[PersonModel]) -> dict:
    return {
        "posts": merge_posts(persons),
        "connections": merge_connections(persons),
        "interests": merge_interests(persons),
        "geo_trace": merge_geo_trace(persons),
    }
