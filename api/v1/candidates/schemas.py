from core.models import Candidate, CandidateModel


class CandidateRead(CandidateModel):
    # TODO: make it work as alias to respect schema
    # id: uuid.UUID = Field(alias='id')
    pass


class CandidateCreate(Candidate):
    pass


class CandidateUpdate(Candidate):
    pass
