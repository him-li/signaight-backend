import json
import os
import tarfile
import uuid
import asyncio
import aiohttp
import aiofiles
import hashlib
import shutil
import typer
from beanie.operators import In
from datetime import datetime
from flatten_json import flatten, unflatten_list
from pathlib import Path
from rich import print
from typing_extensions import Annotated
from urllib.parse import urlparse

from cli.typer_async import AsyncTyper, Argument, Option

from core.config import settings
from core.database import init_db, client as db_client
from core.models import (
    ProjectModel,
    PersonModel,
    CandidateModel,
    AlertsModel,
    FlagModel,
    EvaluationModel
)
from core.fields import S3Path
from core.storage import init_storage

app = AsyncTyper(no_args_is_help=True)

base_dir = Path('/tmp/signaight')
base_dir.mkdir(parents=True, exist_ok=True)


@app.async_command(name="export")
async def project_export(
    project_id: uuid.UUID = Argument(
        ...,
        help="Project UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
    ),
    verbose: Annotated[bool, Option(help="Verbose process")] = False
):
    init_storage()
    await init_db()
    project = await ProjectModel.get(project_id)
    if not project:
        print("[bold red]Project has been not found[/bold red]")
        raise typer.Abort()
    projects_dir = Path(f'{base_dir}/{project.id}')
    projects_dir.mkdir(parents=True, exist_ok=True)

    _project = await download_images(
        json.loads(project.model_dump_json()),
        projects_dir
    )
    # dump project
    with open(f'{projects_dir}/projects.json', 'w') as f:
        projects = [_project]
        json.dump(projects, f)
    print(f'[bold green]{project.id}/projects.json: Done[/bold green]')

    # dump persons
    persons_query = PersonModel.find(
        PersonModel.project.id == project.id
    )
    person_ids = []
    persons = []
    async for person in persons_query:
        person_ids.append(person.id)
        _person = await download_images(
            json.loads(person.model_dump_json()),
            projects_dir
        )
        persons.append(_person)
        if verbose:
            print(f'[green]{project.id}/persons.json <- {person.id}[/green]')
    if persons:
        with open(f'{projects_dir}/persons.json', 'w') as f:
            json.dump(persons, f)
        print(f'[bold green]{project.id}/persons.json: Done[/bold green]')
    else:
        persons_file = Path(f'{projects_dir}/persons.json')
        persons_file.unlink(missing_ok=True)
        print(f'[bold red]{project.id}/persons.json: '
                'No persons found. Skipped[/bold red]')

    candidates = []
    for person_id in person_ids:
        candidates_query = CandidateModel.find(
            CandidateModel.person.id == person_id
        )
        async for candidate in candidates_query:
            _candidate = await download_images(
                json.loads(candidate.model_dump_json()),
                projects_dir
            )
            candidates.append(_candidate)
            if verbose:
                print(f'[green]{project.id}/candidates.json '
                        f'<- {person_id}/{candidate.id}[/green]')
    if candidates:
        with open(f'{projects_dir}/candidates.json', 'w') as f:
            json.dump(candidates, f)
        print(f'[bold green]{project.id}/candidates.json: Done[/bold green]')
    else:
        candidates_file = Path(f'{projects_dir}/candidates.json')
        candidates_file.unlink(missing_ok=True)
        print(f'[bold red]{project.id}/candidates.json: '
                'No candidates found. Skipped[/bold red]')

    flags = []
    for person_id in person_ids:
        flags_query = FlagModel.find(
            FlagModel.person.id == person_id
        )
        async for flag in flags_query:
            _flag = await download_images(
                json.loads(flag.model_dump_json()),
                projects_dir
            )
            flags.append(_flag)
            if verbose:
                print(f'[green]{project.id}/flags.json '
                        f'<- {person_id}/{flag.id}[/green]')
    if flags:
        with open(f'{projects_dir}/flags.json', 'w') as f:
            json.dump(flags, f)
        print(f'[bold green]{project.id}/flags.json: Done[/bold green]')
    else:
        flags_file = Path(f'{projects_dir}/flags.json')
        flags_file.unlink(missing_ok=True)
        print(f'[bold red]{project.id}/flags.json: '
                'No flags found. Skipped[/bold red]')

    alerts = []
    for person_id in person_ids:
        alerts_query = AlertsModel.find(
            AlertsModel.person.id == person_id
        )
        async for alert in alerts_query:
            _alert = await download_images(
                json.loads(alert.model_dump_json()),
                projects_dir
            )
            alerts.append(_alert)
            if verbose:
                print(f'[green]{project.id}/alerts.json '
                    f'<- {person_id}/{alert.id}[/green]')
    if alerts:
        with open(f'{projects_dir}/alerts.json', 'w') as f:
            json.dump(alerts, f)
        print(f'[bold green]{project.id}/alerts.json: Done[/bold green]')
    else:
        alerts_file = Path(f'{projects_dir}/alerts.json')
        alerts_file.unlink(missing_ok=True)
        print(f'[bold red]{project.id}/alerts.json: '
                'No alerts found. Skipped[/bold red]')

    evaluations = []
    for person_id in person_ids:
        evaluations_query = EvaluationModel.find(
            EvaluationModel.person.id == person_id
        )
        async for evaluation in evaluations_query:
            _evaluations = await download_images(
                json.loads(evaluation.model_dump_json()),
                projects_dir
            )
            evaluations.append(_evaluations)
            if verbose:
                print(f'[green]{project.id}/evaluations.json '
                        f'<- {person_id}/{evaluation.id}[/green]')
    if evaluations:
        with open(f'{projects_dir}/evaluations.json', 'w') as f:
            json.dump(evaluations, f)
        print(f'[bold green]{project.id}/evaluations.json: Done[/bold green]')
    else:
        evaluations_file = Path(f'{projects_dir}/evaluations.json')
        evaluations_file.unlink(missing_ok=True)
        print(f'[bold red]{project.id}/evaluations.json: '
                'No evaluations found. Skipped[/bold red]')

    #TODO: maybe additional models here

    # make archive
    now = datetime.now()
    arcfilename = f'{project.id}_{now.strftime("%Y%m%d%H%M%S")}.tar.gz'
    with tarfile.open(f'{base_dir}/{arcfilename}', "w:gz") as tar:
        for file in [x for x in projects_dir.rglob('*') if x.is_file()]:
            tar.add(
                str(file),
                arcname=str(file).replace(f"{str(base_dir)}/", '')
            )
    print(f'[bold green]{arcfilename}: Done[/bold green]')
    shutil.rmtree(projects_dir)


@app.async_command(name="import")
async def project_import(
    project_id: Annotated[
        uuid.UUID,
        Argument(
            ...,
            help="Project UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
        )
    ] = None,
    owner_id: Annotated[
        uuid.UUID,
        Argument(
            ...,
            help="User UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
        )
    ] = None,
    force: Annotated[
        bool,
        Option(help="Force update data for project. All data will overwritten!")
    ] = False,
    verbose: Annotated[bool, Option(help="Verbose process")] = False
):
    if project_id:
        pattern = "*.tar.gz"
        for f in base_dir.glob("*.tar.gz"):
            if str(project_id) in f.name:
                pattern = f.name
        print(pattern)
        arcfileinfo = await choose_archive_file(pattern)
    else:
        arcfileinfo = await choose_archive_file()

    await init_db()
    init_storage()
    project_id = arcfileinfo.get("project_id")

    with tarfile.open(arcfileinfo.get('file'), mode="r:gz") as tar:
        print(f"[green]Extracting data for project "
                f"{arcfileinfo.get('title')}[/green]")
        tar.extractall(base_dir)

    projects_dir = Path(f'{base_dir}/{project_id}')
    data = {
        "projects": [],
        "persons": [],
        "candidates": [],
        "flags": [],
        "alerts": [],
        "evaluations": [],
    }
    for collection in data.keys():
        datafile = Path(f'{projects_dir}/{collection}.json')
        if not datafile.exists():
            continue
        with open(datafile, 'r') as f:
            for item in json.load(f):
                item = await upload_images(item, projects_dir)
                match collection:
                    case "projects":
                        if owner_id:
                            item["user_id"] = str(owner_id)
                        data['projects'].append(ProjectModel(**item))
                    case "persons":
                        data['persons'].append(PersonModel(**item))
                    case "candidates":
                        data['candidates'].append(CandidateModel(**item))
                    case "flags":
                        data['flags'].append(FlagModel(**item))
                    case "alerts":
                        data['alerts'].append(AlertsModel(**item))
                    case "evaluations":
                        data['evaluations'].append(EvaluationModel(**item))

    async with db_client.start_session() as session:
        async with await session.start_transaction():
            if force:
                await purge_all_project_data(project_id, session)

            for collection, entities in data.items():
                if len(entities) == 0:
                    print(f"[red]Importing {collection}: "
                            " Skipped. Empty data[/red]")
                    continue
                try:
                    match collection:
                        case "projects":
                                await ProjectModel.insert_many(entities,
                                        session=session)
                        case "persons":
                                await PersonModel.insert_many(entities,
                                        session=session)
                        case "candidates":
                            await CandidateModel.insert_many(entities,
                                    session=session)
                        case "flags":
                            await FlagModel.insert_many(entities,
                                    session=session)
                        case "alerts":
                            await AlertsModel.insert_many(entities,
                                    session=session)
                        case "evaluations":
                            await EvaluationModel.insert_many(entities,
                                    session=session)
                    print(f"[bold green]Importing {collection}: "
                            "Done[/bold green]")
                except Exception as e:
                    print(f"[red]Import failed: {e}[/red]")
                    raise typer.Abort()

    shutil.rmtree(projects_dir)


@app.async_command(name="cleanup")
async def project_cleanup(
    project_id: uuid.UUID = Argument(
        ...,
        help="Project UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
    ),
    person_id: Annotated[
        uuid.UUID,
        Argument(
            ...,
            help="Person UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
        )
    ] = None,
    dryrun: Annotated[
        bool,
        Option(help="Show stats only without real data cleanup")
    ] = False,
    verbose: Annotated[bool, Option(help="Verbose process")] = False
):
    await init_db()
    init_storage()
    project = await ProjectModel.get(project_id)
    if not project:
        print("[bold red]Project has been not found[/bold red]")
        raise typer.Abort()
    print(f"[bold green]Processing project {project.title}[/bold green]")

    persons_query = PersonModel.find(
        PersonModel.project.id == project.id,
    )
    if person_id:
        persons_query.find(
            PersonModel.id == person_id
        )
    if await persons_query.count() == 0:
        print("[bold red]There no persons found in project[/bold red]")
        raise typer.Abort()
    to_remove = {
        'flags': [],
        'alerts': [],
        'evaluations': [],
    }
    async for person in persons_query:
        result = await person_find_duplicates(person)
        for datatype, stats in result.items():
            if dryrun or verbose:
                print(f"[green]Person {person.id} have {stats.get('total', 0) }"
                        f" alerts where {len(stats.get('to_remove', []))} "
                        f" are duplicates of {len(stats.get('origins', []))}"
                        f" original[/green]")
            if remove_ids := stats.get('to_remove', []):
                to_remove[datatype].extend(remove_ids)

    async with db_client.start_session() as session:
        async with await session.start_transaction():
            for datatype, _ids in to_remove.items():
                if _ids:
                    if not dryrun:
                        match datatype:
                            case "flags":
                                await FlagModel.find(
                                    In(FlagModel.id, _ids)
                                ).delete(session=session)
                            case "alerts":
                                await AlertsModel.find(
                                    In(AlertsModel.id, _ids)
                                ).delete(session=session)
                                print("Delete alerts")
                            case "evaluations":
                                await EvaluationModel.find(
                                    In(EvaluationModel.id, _ids)
                                ).delete(session=session)
                                print("Delete evaluations")
                            case _:
                                continue
                    print(f"[bold green]Project \"{project.title}\" persons"
                            f" {datatype} cleaned up[/bold green]")
                else:
                    print(f"[bold red]Project \"{project.title}\" persons"
                            f" {datatype} no data for cleanup[/bold red]")

@app.async_command(name="purge")
async def project_purge(
    project_id: Annotated[
        uuid.UUID,
        Argument(
            ...,
            help="Project UUID. Ex: 6086bd2e-f458-42c2-85f6-389ef88cc0c4"
        )
    ] = None
):
    await init_db()
    async with db_client.start_session() as session:
        async with await session.start_transaction():
            await purge_all_project_data(project_id, session)

async def person_find_duplicates(person):
        stats = {
            'flags': {},
            'alerts': {},
            'evaluations': {},
        }

        for datatype in stats.keys():
            to_remove = []
            exists = []
            match datatype:
                case "flags":
                    query = FlagModel.find(
                        FlagModel.person.id == person.id
                    )
                case "alerts":
                    query = AlertsModel.find(
                        AlertsModel.person.id == person.id
                    )
                case "evaluations":
                    query = EvaluationModel.find(
                        EvaluationModel.person.id == person.id
                    )
                case _:
                    continue
            count = await query.count()
            async for item in query:
                item_id = item.id
                data = item.model_dump(mode="json")
                data.pop("id", None)
                item_hash = hashlib.sha256(
                    json.dumps(data).encode()
                ).hexdigest()
                if item_hash not in exists:
                    exists.append(item_hash)
                else:
                    to_remove.append(item_id)
            stats[datatype] = {
                'total': count,
                'origins': exists,
                'to_remove': to_remove,
            }
        return stats


# session required to be included in transaction process
async def purge_all_project_data(project_id: uuid.UUID, session) -> None:
    persons_query = PersonModel.find(
        PersonModel.project.id == project_id
    )
    async for person in persons_query:
        await CandidateModel.find(
            CandidateModel.person.id == person.id
        ).delete(session=session)
        await EvaluationModel.find(
            EvaluationModel.person.id == person.id
        ).delete(session=session)
        await FlagModel.find(
            FlagModel.person.id == person.id
        ).delete(session=session)
        await AlertsModel.find(
            AlertsModel.person.id == person.id
        ).delete(session=session)
        await person.delete(session=session)
    await ProjectModel.find(
        ProjectModel.id == project_id
    ).delete(session=session)

async def choose_archive_file(
    pattern: str = "*.tar.gz",
    iteration: int = 0,
    files: list = []
) -> Path:
    if iteration > 5:
        print("[red]You have made too many wrong choices. "
                "Try to run import again[/red]")
        raise typer.Abort()
    if not files:
        for file in [f for f in base_dir.glob(pattern)]:
            try:
                project_id, _ = file.name.split("_")
                project_id = uuid.UUID(project_id)
            except Exception:
                continue
            with tarfile.open(file, "r:gz") as tar:
                f = tar.extractfile(tar.getmember(f"{project_id}/projects.json"))
                if f is not None:
                    _title = [project.get('title') for project in json.load(f)
                                if project.get('title')]
                    files.append({
                        "file": file,
                        "project_id": project_id,
                        "title": ", ".join(_title)
                    })
    if len(files) == 0:
        print("[red]There no archive files found. "
                "Task aborted[/red]")
        raise typer.Abort()
    if len(files) == 1:
        return files[0]
    else:
        for i, file in enumerate(files):
            print(f"{i+1}: [green]{file.get('title')}[/green]")
        try:
            fileindex = int(typer.prompt(
                "Please choose project archive to restore it by providing "
                "number from list"))
            _file = files[fileindex-1]
            return _file
        except:
            print("[red]Wrong choice has been made. Try again to provide "
                    "file number from list[/red]")
            return await choose_archive_file(iteration+1, files)


async def download_images(data, base_path):
    data = flatten(data, '.')
    images = []
    for key, value in data.items():
        if isinstance(value, str) and settings.AWS_S3_BUCKET in value:
            images.append((key, value))
    if images:
        async with aiohttp.ClientSession() as session:
            images = await asyncio.gather(
                *[download_image(key, url, str(base_path), session) for key, url in images]
            )
    for key, value in images:
        data[key] = value
    return unflatten_list(data, '.')


async def download_image(key, url, base_path, session):
    try:
        _url = urlparse(url)
        _path = _url.path.split("/")
        filename = _path.pop(-1)
        filepath = Path("{}/{}".format(base_path, "/".join(_path)))
        filepath.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)
        return key, None
    async with session.get(url) as response:
        async with aiofiles.open(f"{filepath}/{filename}", "wb") as f:
            await f.write(await response.read())
    # WARNING!!! path should always relative dump dir with media prefix!
    return key, f"media://{_url.path}"


async def upload_images(data, base_path):
    data = flatten(data, '.')
    images = []
    for key, value in data.items():
        if isinstance(value, str) and "media://" in value:
            images.append((key, value.replace("media://", "")))
    if images:
        for i, media in enumerate(images):
            key, path = media
            media = S3Path(f"s3://{settings.AWS_S3_BUCKET}{path}")
            media.upload_from(
                source=f"{base_path}{path}",
                force_overwrite_to_cloud=True
            )
            images[i] = key, str(media)
    for key, value in images:
        data[key] = value
    return unflatten_list(data, '.')
