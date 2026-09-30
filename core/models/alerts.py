from uuid import UUID
from beanie import (Link, after_event, before_event,
                    ValidateOnSave, Update, Replace, Insert)
from pymongo import IndexModel, ASCENDING
from typing import Optional, List

from .base import SignAIghtSchema, Document
from .person import PersonModel


class Heuristic(SignAIghtSchema):
    title: str
    description: str
    score: float


class Alert(SignAIghtSchema):
    heuristics: Optional[List[Heuristic]] = None
    # NOTE: value comes from max score value from Heuristics
    score: Optional[float] = None


class Alerts(SignAIghtSchema):
    strong_affinity_with_israel: Optional[Alert] = None
    strong_affinity_with_usa: Optional[Alert] = None
    occupational_instability: Optional[Alert] = None
    ineligible_occupation: Optional[Alert] = None
    anti_israel_statements:  Optional[Alert] = None
    anti_usa_statements:  Optional[Alert] = None
    criminal_records:  Optional[Alert] = None
    
ALERTS_FIELDS = [
    "strong_affinity_with_israel",
    "strong_affinity_with_usa",
    "occupational_instability",
    "ineligible_occupation",
    "anti_israel_statements",
    "anti_usa_statements",
    "criminal_records"
]

class AlertsModel(Document, Alerts):
    person: Link[PersonModel]

    class Settings:
        name = "person_alerts"
        indexes = [
            # NOTE: pers is upcoming link declared in package __init__
            # python inheritance does not work for Settings class in Beanie
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                ],
                name="alerts_person",
                background=True,
                sparse=True
            ),
        ]
        use_revision = False
        
    def _get_person_id(self) -> Optional[UUID]:
        try:
            if hasattr(self.person, "ref") and getattr(self.person.ref, "id", None):
                return self.person.ref.id
            if isinstance(self.person, PersonModel):
                return self.person.id
            if getattr(self.person, "id", None):
                return self.person.id
        except Exception:
            pass
        return None

    @after_event(ValidateOnSave, Update, Replace, Insert)
    async def update_alerts(self):
        person_id = self._get_person_id()
        if not person_id:
            return

        alert_count = sum(
            getattr(self, field) is not None
            for field in ALERTS_FIELDS
        )

        if alert_count:
            await PersonModel.find(PersonModel.id == person_id).update(
                {"$set": {"alerts_count": alert_count}}
            )

    @before_event(ValidateOnSave)
    async def validate_not_all_none(self):
        """Prevent saving if all alerts are None"""
        alert_fields = [
            self.strong_affinity_with_israel,
            self.strong_affinity_with_usa,
            self.occupational_instability,
            self.ineligible_occupation,
            self.anti_israel_statements,
            self.anti_usa_statements,
            self.criminal_records,
        ]

        # If all alerts are None, raise a validation error
        if all(field is None for field in alert_fields):
            raise ValueError("At least one alert must be set before saving.")
