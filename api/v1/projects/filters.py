from typing import List, Optional
from core.models import ProjectModel
from api.filter import Filter


class ProjectFilter(Filter):
    search: Optional[str] = None
    title: Optional[str] = None
    title__like: Optional[str] = None
    created_at: Optional[str] = None
    uppdated_at: Optional[str] = None
    project_platform: Optional[str] = None
    description: Optional[str] = None
    description__like: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = ProjectModel
        search_field_name = "search"
        search_model_fields = ["title", "created_at", "updated_at"]
