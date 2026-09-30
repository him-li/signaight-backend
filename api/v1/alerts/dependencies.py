from .crud import AlertsCRUD


async def get_alerts_crud() -> AlertsCRUD:
    return AlertsCRUD()
