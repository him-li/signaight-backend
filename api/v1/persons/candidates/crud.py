from fastapi import HTTPException
from core.models import PersonModel, CandidateModel
from beanie import operators
from uuid import UUID

from api.pagination import paginate
from api.acl import Principal
from api.local_authorization import require_project_access
from .schemas import CandidateListRead, CandidateListView


class CandidatesCRUD:

    def __init__(self, principal: Principal):
        self.principal = principal

    async def _person(self, person_id):
        person = await PersonModel.get(person_id, fetch_links=True)
        if not person or not person.project:
            raise HTTPException(status_code=404, detail="Person does not exist!")
        require_project_access(self.principal, person.project.user_id)
        return person

    async def _pagination_transformer(self, items):
        return [CandidateListRead(**item.model_dump()) for item in items]

    async def create(self, person_id, data):
        person = await self._person(person_id)
        candidate = CandidateModel(person=person, **data)
        result = await candidate.insert()
        return result

    async def read_list(self, person_id, params, filter):
        await self._person(person_id)
        query = CandidateModel.find(
            CandidateModel.person.id == person_id
        ).project(CandidateListView)
        query = filter.filter(query)
        query = filter.sort(query)
        return await paginate(query, fetch_links=False,
                              transformer=self._pagination_transformer)

    async def read(self, person_id, id):
        candidate = await CandidateModel.get(id, fetch_links=True)
        if not candidate:
            raise HTTPException(status_code=404,
                                detail="Candidate does not exist!")
        person = await self._person(person_id)
        candidate_person_id = (
            candidate.person.id if isinstance(candidate.person, PersonModel)
            else candidate.person.ref.id
        )
        if candidate_person_id != person.id:
            raise HTTPException(status_code=404,
                                detail="Candidate does not exist!")
        return candidate

    async def read_primary(self, person_id, source, resource, search_id):
        return CandidateModel.find_many(
            CandidateModel.person.id == UUID(person_id),
            CandidateModel.source == source,
            CandidateModel.resource == resource,
            CandidateModel.search_id == search_id,
            operators.In(CandidateModel.primary, [True]),
        )

    async def read_all(self, person_id):
        return CandidateModel.find_many(
            CandidateModel.person.id == UUID(person_id))

    async def read_all_by_source_resource(self, person_id, source, resource):
        return CandidateModel.find_many(
            CandidateModel.person.id == UUID(person_id),
            CandidateModel.source == source,
            CandidateModel.resource == resource
        )

    async def update(self, person_id, id, data):
        candidate = await self.read(person_id, id)
        data = {k: v for k, v in data.items() if v is not None}
        for k, v in data.items():
            if k != "id":
                setattr(candidate, k, v)
        await candidate.save()
        return candidate

    async def delete(self, person_id, id):
        candidate = await self.read(person_id, id)
        await candidate.delete()
