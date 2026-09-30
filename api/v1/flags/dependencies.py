from .crud import FlagsCRUD


async def get_flags_crud() -> FlagsCRUD:
    return FlagsCRUD()
