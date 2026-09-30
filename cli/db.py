import os
import importlib
import json
# from pydantic_mermaid import MermaidGenerator
from rich import print
from typing_extensions import Annotated


import core.models as models
from core.models import PersonModel
from core.database import init_db
from cli.typer_async import AsyncTyper, Argument, Option

app = AsyncTyper(no_args_is_help=True)


# pydantic_mermaid in early staged development
'''
@app.async_command()
async def schema():
    generator = MermaidGenerator(models)
    chart = generator.generate_chart()
    print(chart)
'''


@app.async_command()
async def person_score(
    min: int = Argument(default=1, help="Person score minimal value"),
    max: int = Argument(default=60, help="Person score maximum value"),
):
    print(min)
    print(max)


# NOTE: probably onetime action
@app.async_command()
async def person_sl_rf():
    await init_db()
    data_path = "{}/sample_data/json_outputs/persons_sl_rf.json".format(
        os.path.dirname(models.__file__))
    with open(data_path) as f:
        data = json.load(f)
    for row in data:
        name = row.get('personal_details', {}).get('name', {})
        f_name = name.get('first_name', {}).get('f_name')
        l_name = name.get('last_name', {}).get('l_name')
        persons = await PersonModel.find({
            'personal_details.name.first_name.f_name': f_name,
            'personal_details.name.last_name.l_name': l_name,
        }).to_list()
        # TODO: maybe add entity if there is no persons found?
        for person in persons:
            person.demo_data = True
            person.connection_graph = row.get('connection_graph', None)
            # person.red_flags = row.get('red_flags', [])
            await person.save()
            print(f'{f_name} {l_name} saved')


@app.async_command()
async def dump(
    model: Annotated[str, Argument(help="Model name")] = "Wade Wilson",
    demo: Annotated[bool, Option(help="Import only demo data.")] = False,
):

    module = importlib.import_module('my_package.my_module')
    my_class = getattr(module, 'MyClass') # noqa

    # my_instance = my_class()
