import os
import json
from datetime import datetime, timezone
from pathlib import Path
from typer import Exit, Argument, Option
from typing_extensions import Annotated, Literal
from uuid import UUID
from yaml import safe_load as yaml_safe_load

# WARNING: Import is important as a workaround for non dockerised app run
from langsearch.config import settings # noqa

from core.logging import logger
from langsearch.database import init_db
from langsearch.utils.typer_async import AsyncTyper
from langsearch.models.matcher_results import (
    UnifiedPersonModel,
)
from langsearch.models.search_input import SearchInput

app = AsyncTyper(no_args_is_help=True)

def import_flows_from_config():
    flows = []
    graph_config = Path(__file__).resolve().parent / 'langsearch.yaml'
    try:
        with graph_config.open() as fp:
            config = yaml_safe_load(fp)
        flows = [key for key
            in config.get('config', {}).get('flows', {}).keys()]
    except Exception as e:
        logger.error(f"Error importing flows from config: {str(e)}")
    return flows

flows = import_flows_from_config()


@app.async_command("search")
async def search(
    person_id: Annotated[UUID | None,
        Argument(help="Person id always override options ")] = None,
    f_name: Annotated[str | None, Option(help="Frist name Ex: John")] = None,
    l_name: Annotated[str | None, Option(help="Last name Ex: Doe")] = None,
    name: Annotated[str | None, Option(help="Full name Ex: John Doe")] = None,
    email_address:  Annotated[str | None,
        Option(help="Email Ex: john.doe@domain.tld")] = None,
    phone_number:  Annotated[str | None,
        Option(help="Phone number Ex: +1234567890")] = None,
    photo:  Annotated[str | None,
        Option(help="Link to photo Ex: https://domain.tld/path/to/person"
            "/photo.jpg")] = None,
    country: Annotated[str | None, Option(help="Country name Ex: Neverland")] = None,
    city: Annotated[str | None, Option(help="City name Ex: Newercity")] = None,
    education: Annotated[str | None,
        Option(help="Education place Ex: MIT")] = None,
    work: Annotated[str | None, Option(help="Work place Ex: ACME Inc.")] = None,
    bio: Annotated[str | None,
        Option(help="Biography Ex: Building better worlds")] = None,
    username: Annotated[str | None, Option(help="Username Ex: johndoe")] = None,
    no_broker: Annotated[bool, Option(help="run graph locally")] = False,
    flow: Annotated[Literal[tuple(flows)], Option(help="run graph in specified mode")] = 'default'
):
    # Init database here
    await init_db()

    if person_id:
        person = await UnifiedPersonModel.get(person_id)
        if not person:
            logger.error("The requested person for search does not exists")
            raise Exit()
    else:
        person = UnifiedPersonModel(
            input=SearchInput(**{
                "firstname": f_name,
                "lastname": l_name,
                "homephone": phone_number,
                "cellphone": phone_number,
                "email": email_address,
                "photo": photo,
                "work": work,
                "education": education,
                "country": country,
                "city": city
            }),
            start_timestamp=datetime.now(timezone.utc)
        )
        await person.insert()
    if no_broker:
        from langsearch.tasks import search_person_task

        result = await search_person_task(person.id, flow)
        if not result:
            await person.delete()
        else:
            logger.info(f"You can run search for registered person again with id {person.id}")
    else:
        from langsearch.app import broker as taskiq_broker, search_person
        # Init MLflow here not required cause it works in context
        # of taskiq worker
        # Init broker queue here
        if not taskiq_broker.is_worker_process:
            try:
                await taskiq_broker.startup()
            except Exception as e:
                logger.error(f"Error initializing broker: {str(e)}")
        await search_person.kiq(str(person.id), flow)

@app.async_command("dummy")
def dummy():
    """
    At the moment there only one command "search"

    In the next versions mor commands will added
    """
    pass


if __name__ == "__main__":
    app()
