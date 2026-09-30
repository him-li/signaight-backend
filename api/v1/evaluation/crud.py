import uuid
from fastapi import HTTPException

from core.models import EvaluationModel
from api.pagination import paginate
from .schemas import EvaluationRead


class EvaluationCRUD:

    async def _pagination_transformer(self, items):
        return [EvaluationRead(**item.model_dump()) for item in items]

    async def create(self, data):
        evaluation = EvaluationModel(**data)
        result = await evaluation.insert()
        return result

    async def read_list(self, params, filter):
        query = EvaluationModel.find_all(fetch_links=True)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        evaluation = await EvaluationModel.get(id)
        if not evaluation:
            raise HTTPException(status_code=404,
                                detail="Evaluation does not exist!")
        return evaluation

    async def read_all(self, params, filter, person_id):
        query = EvaluationModel.find_many(
            EvaluationModel.person.id == uuid.UUID(person_id)
        )
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def update(self, id, data):
        evaluation = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(evaluation, k, v)
        await evaluation.save()
        return evaluation
