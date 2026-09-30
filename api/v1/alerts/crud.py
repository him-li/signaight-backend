import uuid
from fastapi import HTTPException

from core.models import AlertsModel

from api.pagination import paginate
from .schemas import AlertsRead


class AlertsCRUD:

    async def _pagination_transformer(self, items):
        return [AlertsRead(**item.model_dump()) for item in items]

    async def create(self, data):
        alert = AlertsModel(**data)
        result = await alert.insert()
        return result

    async def read_list(self, params, filter):
        query = AlertsModel.find_all(fetch_links=True)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def read(self, id):
        alert = await AlertsModel.get(id)
        if not alert:
            raise HTTPException(status_code=404,
                                detail="Alert does not exist!")
        return alert

    async def read_all(self, params, filter, person_id):
        query = AlertsModel.find_many(
            AlertsModel.person.id == uuid.UUID(person_id)
        )
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, transformer=self._pagination_transformer)

    async def update(self, id, data):
        alert = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(alert, k, v)
        await alert.save()
        return alert
