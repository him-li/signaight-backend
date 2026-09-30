from core.models import UUIDModel, SearchEvent


class SearchEventRead(SearchEvent, UUIDModel):
    pass
