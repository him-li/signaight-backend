from .crud import CandidatesCRUD


async def get_candidates_crud() -> CandidatesCRUD:
    return CandidatesCRUD()
