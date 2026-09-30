from fastapi import HTTPException

from core.models import ServiceStepLogModel
from api.pagination import paginate
from .schemas import ServiceStepLogRead


class ServiceStepLogCRUD:

    async def _pagination_transformer(self, items):
        return [ServiceStepLogRead(**item.model_dump()) for item
                in items]

    async def create(self, data):
        log = ServiceStepLogModel(**data)
        result = await log.insert()
        return result

    async def read(self, id):
        log = await ServiceStepLogModel.get(id)
        if not log:
            raise HTTPException(status_code=404,
                                detail="Log does not exist!")
        return log

    async def list(self, params, filter):
        query = ServiceStepLogModel.find_all()
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query,
                              transformer=self._pagination_transformer)
