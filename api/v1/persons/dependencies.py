from fastapi import Depends, BackgroundTasks

from api.acl import Principal, get_principal
from .crud import PersonsCRUD

async def get_persons_crud(
    background_tasks: BackgroundTasks,
    principal: Principal = Depends(get_principal),
) -> PersonsCRUD:
    return PersonsCRUD(background_tasks, principal)
