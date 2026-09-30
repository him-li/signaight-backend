import uuid
import asyncio
from bson.binary import Binary as uuidBinary
from business_rules import run_all

from cli.typer_async import AsyncTyper, Argument

from core.models import FlagModel, PersonModel, AlertsModel, EvaluationModel
from core.rules.person import (
    PersonVariables,
    PersonActions,
)
from core.database import init_db

app = AsyncTyper()


@app.async_command()
async def score_change(
    project_id: uuid.UUID = Argument(
        ...,
        help="Project UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4")):

    await init_db()
    project_id_uuid_binary = uuidBinary.from_uuid(project_id)
    persons = await PersonModel.find(
        {'project.$id': {"$eq": project_id_uuid_binary}}).to_list()

    for person in persons:
        alerts = await AlertsModel.find_one(
            AlertsModel.person.id == person.id
        )
        evaluation = await EvaluationModel.find_one(
            EvaluationModel.person.id == person.id
        )
        flags = await FlagModel.find_one(
            FlagModel.person.id == person.id
        )
        if not alerts:
            alerts = AlertsModel(person=person)
        if not evaluation:
            evaluation = EvaluationModel(person=person)
        if not flags:
            flags = FlagModel(person=person)
        run_all(
            rule_list=person_ruleset,
            defined_variables=PersonVariables(
                person,
                alerts,
                evaluation,
                flags
            ),
            defined_actions=PersonActions(
                person,
                alerts,
                evaluation,
                flags
            )
        )
        await person.save()
        await alerts.save()
        await evaluation.save()
    print("Person Scores Updated")

person_ruleset = [
    {
        "label": "Calculate person signaight_score",
        "conditions": {
            "all": [
                {
                    "name": "person_with_evaluation_alerts",
                    "operator": "is_true",
                    "value": True
                }
            ]
        },
        "actions": [
            {
                "name": "set_person_score"
            }
        ]
    }
]


if __name__ == "__main__":
    asyncio.run(app())
