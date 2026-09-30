from fastapi import HTTPException

from core.models import CandidateModel

from api.pagination import paginate


class CandidatesCRUD:

    # TODO: schema returns object without id
    async def create(self, data):
        candidate = CandidateModel(**data)
        result = await candidate.insert()
        return result

    async def read_list(self, params, filter):
        # Turn document into find query
        query = CandidateModel.find_all()
        # Filtering
        query = filter.filter(query)
        # Sorting
        query = filter.sort(query)
        # Paginate
        return await paginate(query)

    async def read(self, id):
        candidate = await CandidateModel.get(id)
        if not candidate:
            raise HTTPException(
                status_code=404,
                detail="Candidate do not exists!"
            )
        return candidate

    async def update(self, id, data):
        candidate = await self.read(id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            setattr(candidate, k, v)
        await candidate.save()
        return candidate

    async def delete(self, id):
        candidate = await self.read(id)
        await candidate.delete()
