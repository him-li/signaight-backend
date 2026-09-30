from .crud import MappingsCRUD


async def get_mappings_crud() -> MappingsCRUD:
    return MappingsCRUD()
