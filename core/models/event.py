import uuid
from beanie import (
    UnionDoc,
    after_event,
    ValidateOnSave,
    Update,
    Replace
)
from datetime import datetime, timedelta
from enum import Enum
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import Optional, List, Dict, Union

from .base import SignAIghtSchema, Document
from .person import PersonModel
from .candidate import Candidate


class Status(Enum):
    queued = "Queued"
    started = "Started"
    active = "Active"
    paused = "Paused"
    success = "Success"
    in_progress = "In progress"
    done = "Done"
    seen = "Seen"
    error = "Error"


class Event(SignAIghtSchema):
    # TODO: probably should be group or list of users in future
    user_id: Optional[str] = Field(None, examples=[str(uuid.uuid4())])
    status: Optional[Status] = Field(
        default=Status.queued, examples=["Active"])
    created_at: datetime = Field(
        default_factory=datetime.now, examples=[
            str(datetime.now().isoformat())]
    )
    updated_at: Optional[datetime] = Field(None, examples=[str(datetime.now().
                                                               isoformat())])


class EventModel(UnionDoc):
    class Settings:
        name = "events"
        class_id = "_class_id"
        use_revision = False


class BaseSearchEvent(Event, SignAIghtSchema):
    duration: Optional[timedelta] = Field(None, examples=[1000])
    retries: int = Field(0, examples=[10])
    percent_completed: Optional[int] = Field(None, gt=-1, le=100, examples=[10])


class SearchEvent(BaseSearchEvent):
    # context describe for which flow search has been ran
    context: Optional[str] = Field(None, examples=["DeepSearch"])
    flows_list: List[Dict] = Field(
        help="List of flows names used in the search")
    persons_list: List[uuid.UUID] = Field(help="List of persons IDs searched")


class SearchEventModel(SearchEvent, Document):

    @after_event(ValidateOnSave, Update, Replace)
    async def change_search_ready(self):
        if self.status == Status.done or self.status == "Done":
            for person_id in self.persons_list:
                person = await PersonModel.find_one(
                    PersonModel.id == person_id)
                person.search_state.is_done = True
                person.search_state.status = Status.success
                await person.save_changes()
        if self.status == Status.started or self.status == Status.in_progress:
            for person_id in self.persons_list:
                person = await PersonModel.find_one(
                    PersonModel.id == person_id)
                person.search_state.is_done = False
                person.search_state.status = Status.in_progress
                await person.save_changes()

    class Settings:
        name = "Search"
        union_doc = EventModel
        # NOTE: index creation should be run only once and not possible inside union_doc
        # indexes = [
        #     IndexModel(
        #         [
        #             ("_class_id", ASCENDING),
        #             ("user_id", ASCENDING),
        #             ("created_at", DESCENDING),
        #         ],
        #         name="events_class_id_user_id_created_at",
        #         background=True,
        #         sparse=True
        #     ),
        #     # IndexModel(
        #     #     [
        #     #         ("_class_id", ASCENDING),
        #     #         ("user_id", ASCENDING),
        #     #         ("status", ASCENDING),
        #     #         ("created_at", DESCENDING),
        #     #     ],
        #     #     name="events_class_id_user_id_status_created_at",
        #     #     background=True,
        #     #     sparse=True
        #     # ),
        # ]


class ActiveSearchEvent(BaseSearchEvent):
    search_results: Optional[List[Candidate]] = []
    title: Optional[str] = None
    education: Optional[str] = None
    location: Optional[Union[str, int]] = None


class ActiveSearchEventModel(ActiveSearchEvent, Document):

    class Settings:
        name = "ActiveSearch"
        union_doc = EventModel


class RecalculationEvent(Event):
    project_id: Optional[uuid.UUID] = None


class RecalculationEventModel(RecalculationEvent, Document):

    class Settings:
        name = "RecalculationEvent"
        union_doc = EventModel
