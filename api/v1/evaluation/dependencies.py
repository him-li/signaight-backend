from .crud import EvaluationCRUD


async def get_evaluation_crud() -> EvaluationCRUD:
    return EvaluationCRUD()
