from fastapi import HTTPException

from api.pagination import paginate
from core.models import SearchEventModel
from .schemas import SearchEventRead


class SearchCRUD:

    async def _pagination_transformer(self, items):
        return [SearchEventRead(**item.model_dump()) for item in items]

    async def create(self, data):
        search = SearchEventModel(**data)
        result = await search.insert()
        return result

    async def read_list(self, params, filter, user_id):
        query = SearchEventModel.find_many(
            {"user_id": user_id}).sort(-SearchEventModel.created_at)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        search = await SearchEventModel.get(id)
        if not search:
            raise HTTPException(
                status_code=404,
                detail="Search does not exist!"
                )
        return search

    async def update(self, id, data):
        search = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(search, k, v)
        # TODO: error with workflow detected
        await search.save()
        return search
