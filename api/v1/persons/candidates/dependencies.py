from fastapi import Depends

from api.acl import Principal, get_principal
from .crud import CandidatesCRUD


async def get_candidates_crud(
    principal: Principal = Depends(get_principal),
) -> CandidatesCRUD:
    return CandidatesCRUD(principal)
