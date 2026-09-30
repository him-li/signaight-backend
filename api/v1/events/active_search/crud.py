from fastapi import HTTPException

from api.pagination import paginate
from core.models import ActiveSearchEventModel
from .schemas import ActiveSearchEventRead


class ActiveSearchCRUD:

    async def _pagination_transformer(self, items):
        return [ActiveSearchEventRead(**item.model_dump()) for
                item in items]

    async def create(self, data):
        active_search = ActiveSearchEventModel(**data)
        result = await active_search.insert()
        return result

    async def read_list(self, params, filter, user_id):
        query = ActiveSearchEventModel.find_many(
            {"user_id": user_id})
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        active_search = await ActiveSearchEventModel.get(id)
        if not active_search:
            raise HTTPException(
                status_code=404,
                detail="Active Search does not exist!"
            )
        return active_search

    async def update(self, id, data):
        active_search = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(active_search, k, v)
        # TODO: error with workflow detected
        await active_search.save()
        return active_search
