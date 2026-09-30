from .crud import RecalculationCRUD


async def get_recalculation_crud() -> RecalculationCRUD:
    return RecalculationCRUD()
