from core.models import UUIDModel, Evaluation


class EvaluationRead(Evaluation, UUIDModel):
    # TODO: make it work as alias to respect schema
    # id: uuid.UUID = Field(alias='id')
    pass


class EvaluationCreate(Evaluation):
    pass


class EvaluationUpdate(Evaluation):
    pass
