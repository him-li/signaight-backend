from .crud import ActiveSearchCRUD


async def get_active_search_crud() -> ActiveSearchCRUD:
    return ActiveSearchCRUD()
