from fastapi import HTTPException

from api.pagination import paginate
from core.models import MappingModel
from .schemas import MappingRead

class MappingsCRUD:

    async def  _pagination_transformer(self, items):
        return [MappingRead(**item.model_dump()) for item in items]

    async def create(self, data):
        mapping = MappingModel(**data)
        result = await mapping.insert()
        return result

    async def read_list(self, params, filter):
        query = MappingModel.find_all()
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        mapping = await MappingModel.get(id)
        if not mapping:
            raise HTTPException(status_code=404,
                                detail="Mapping does not exist!"
                                )
        return mapping

    async def update(self, id, data):
        mapping = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            setattr(mapping, k, v)
        await mapping.save()
        return mapping

    async def delete(self, id):
        mapping = await self.read(id)
        await mapping.delete()
