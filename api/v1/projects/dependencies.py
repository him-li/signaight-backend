from fastapi import Depends

from api.acl import Principal, get_principal
from .crud import ProjectsCRUD

async def get_projects_crud(
    principal: Principal = Depends(get_principal)
) -> ProjectsCRUD:
    return ProjectsCRUD(principal)
