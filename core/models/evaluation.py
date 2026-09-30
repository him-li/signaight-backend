from beanie import Link, after_event, ValidateOnSave, Update, Replace, Insert
from pymongo import IndexModel, ASCENDING
from typing import Optional, List

from .base import SignAIghtSchema, Document
from .person import PersonModel


class EvaluationFactor(SignAIghtSchema):
    title: str
    score: float
    weight: float = 1


class EvaluationCategory(SignAIghtSchema):
    factors: Optional[List[EvaluationFactor]] = None
    score: float


class Evaluation(SignAIghtSchema):
    resilience: Optional[EvaluationCategory] = None
    flexibility: Optional[EvaluationCategory] = None
    work_under_pressure: Optional[EvaluationCategory] = None
    curiosity: Optional[EvaluationCategory] = None
    decision_making: Optional[EvaluationCategory] = None
    courage: Optional[EvaluationCategory] = None
    teamwork: Optional[EvaluationCategory] = None
    moral_values: Optional[EvaluationCategory] = None
    language_skills: Optional[EvaluationCategory] = None
    interpersonal_skills: Optional[EvaluationCategory] = None
    
EVAL_FIELDS = (
        "resilience",
        "flexibility",
        "work_under_pressure",
        "curiosity",
        "decision_making",
        "courage",
        "teamwork",
        "moral_values",
        "language_skills",
        "interpersonal_skills",
    )


class EvaluationModel(Document, Evaluation):
    person: Link[PersonModel]

    class Settings:
        name = "person_evaluations"
        indexes = [
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                ],
                name="evaluation_person",
                background=True,
                sparse=True,
            ),
        ]
        use_revision = False
        
    def _count_non_null(self) -> int:
        return sum(getattr(self, f) is not None for f in EVAL_FIELDS)

    async def _get_evaluation_person(self) -> Optional[PersonModel]:
        person_id = None
        try:
            if isinstance(self.person, Link):
                person_id = self.person.ref.id
            elif isinstance(self.person, PersonModel):
                person_id = self.person.id
        except Exception:
            pass
        if person_id:
            return await PersonModel.get(person_id)
        return None

    @after_event(ValidateOnSave, Update, Replace, Insert)
    async def update_evaluation(self):
        person = await self._get_evaluation_person()
        if not person:
            return
       
        new_count = self._count_non_null()
        await PersonModel.find_one(PersonModel.id == person.id).update(
            {"$set": {"evaluation_count": new_count}}
        )
