from .crud import SearchCRUD


async def get_search_crud() -> SearchCRUD:
    return SearchCRUD()
