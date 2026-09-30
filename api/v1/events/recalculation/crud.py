from fastapi import HTTPException

from api.pagination import paginate
from core.models import RecalculationEventModel
from .schemas import RecalculationEventRead


class RecalculationCRUD:

    async def _pagination_transformer(self, items):
        return [RecalculationEventRead(**item.model_dump())
                for item in items]

    async def create(self, data):
        recalculation = RecalculationEventModel(**data)
        result = await recalculation.insert()
        return result

    async def read_list(self, params, filter, user_id):
        query = RecalculationEventModel.find_many(
            {"user_id": user_id}).sort(-RecalculationEventModel.created_at)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        recalculation = await RecalculationEventModel.get(id)
        if not recalculation:
            raise HTTPException(
                status_code=404,
                detail="Recalculation does not exist!"
            )
        return recalculation

    async def update(self, id, data):
        recalculation = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(recalculation, k, v)
        # TODO: error with workflow detected
        await recalculation.save()
        return recalculation
