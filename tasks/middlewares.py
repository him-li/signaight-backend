import asyncio
import uuid
from logging import getLogger
from taskiq import TaskiqMiddleware
from taskiq.exceptions import NoResultError, TaskiqResultTimeoutError
from taskiq.kicker import AsyncKicker
from taskiq.message import TaskiqMessage
from taskiq.middlewares import (SimpleRetryMiddleware as
    OriginSimpleRetryMiddleware)
from taskiq.result import TaskiqResult
from typing import Any, Iterable, Optional, List

from core.database import client as mongo_client, init_db
from core.models import PersonModel, SearchEventModel
from core.models.search_state import SearchStatus
from core.socketio import MessageBuilder
from .redis import send_notification

class PersonStatusUpdateMixin():

    async def set_person_status(
        self,
        persons: List[uuid.UUID],
        search_id: uuid.UUID | None = None,
        status: SearchStatus = SearchStatus.error,
        is_done: bool = False,
        description: str | None = None,
    ) -> None:
        persons = []
        for person_id in persons:
            person = await PersonModel.get(person_id)
            if person:
                persons.append(person)
        try:
            search = await SearchEventModel.get(search_id)
        except Exception as e:
            search = None

        for person in persons:
            person.search_state.is_done = is_done
            person.search_state.status = status
            if description:
                person.search_state.description = description
            await person.save_changes()
        if search:
            send_notification(
                str(search.user_id),
                MessageBuilder.search_message(search.id, "error")
            )


class TimeoutStateSaveMiddleware(PersonStatusUpdateMixin, TaskiqMiddleware):

    def __init__(self) -> None:
        self.logger = getLogger("taskiq.timeoutstatesave_middleware")

    async def on_error(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
        exception: BaseException,
    ) -> None:
        if not isinstance(exception, asyncio.TimeoutError):
            return

        if "run_complex_search_flow" in message.task_name:
            await self.set_person_status(
                [uuid.UUID(person_id) for person_id in message.args[0]],
                search_id=uuid.UUID(message.args[1]),
                status=SearchStatus.timeout,
                description="Search timeout",
            )


# NOTE: Deprecated since Taskiq got startup/shutdown cycle management
class BeanieDBMiddleware(TaskiqMiddleware):

    db_initialized = False

    def __init__(self) -> None:
        self.logger = getLogger("taskiq.beanie_middleware")

    async def startup(self) -> None:
        while not self.db_initialized:
            self.logger.info("Beanie(MongoDB) connection attempt")
            try:
                await init_db()
                self.db_initialized = True
            except Exception:
                await asyncio.sleep(5)
        self.logger.info("Beanie(MongoDB) started")

    async def shutdown(self) -> None:
        await mongo_client.close()
        self.logger.info("Beanie(MongoDB) shutdown")



class SimpleRetryMiddleware(PersonStatusUpdateMixin,
    OriginSimpleRetryMiddleware):

    def __init__(
        self,
        default_retry_count: int = 3,
        default_retry_label: bool = False,
        no_result_on_retry: bool = True,
        types_of_exceptions: Optional[Iterable[type[BaseException]]] = None,
    ) -> None:
        self.logger = getLogger("taskiq.aiopika_retry_middleware")
        super().__init__(
            default_retry_count=default_retry_count,
            default_retry_label=default_retry_label,
            no_result_on_retry=no_result_on_retry,
            types_of_exceptions=types_of_exceptions
        )

    async def on_error(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
        exception: BaseException,
    ) -> None:
        """
        Retry on error.

        This middleware is used to retry
        tasks on errors.

        If error is found during the execution
        this function is invoked.

        :param message: Message that caused the error.
        :param result: execution result.
        :param exception: found exception.
        """
        if self.types_of_exceptions is not None and not isinstance(
            exception,
            tuple(self.types_of_exceptions),
        ):
            return

        # Valid exception
        if isinstance(exception, NoResultError):
            return
        retry_on_error = message.labels.get("retry_on_error")
        if isinstance(retry_on_error, str):
            retry_on_error = retry_on_error.lower() == "true"

        if retry_on_error is None:
            retry_on_error = self.default_retry_label
        # Check if retrying is enabled for the task.
        if not retry_on_error:
            return

        kicker: AsyncKicker[Any, Any] = AsyncKicker(
            task_name=message.task_name,
            broker=self.broker,
            labels=message.labels,
        ).with_task_id(message.task_id)

        # Getting number of previous retries.
        retries = int(message.labels.get("_retries", 0)) + 1
        # Make lower message priority for new retry
        priority = int(message.labels.get("priority", 5))
        priority = priority - 1 if priority - 1 > 0 else 0
        kicker.with_labels(_retries=retries, priority=priority)
        max_retries = int(message.labels.get("max_retries", self.default_retry_count))

        if retries < max_retries:
            self.logger.info(
                "Task '%s' invocation failed. Retrying.",
                message.task_name,
            )
            await kicker.kiq(*message.args, **message.kwargs)

            if "run_complex_search_flow" in message.task_name:
                if self.no_result_on_retry:
                    result.error = NoResultError()
                await self.set_person_status(
                    [uuid.UUID(person_id) for person_id in message.args[0]],
                    search_id=uuid.UUID(message.args[1]),
                    status=SearchStatus.in_progress,
                    description="Search retry",
                )
        else:
            if "run_complex_search_flow" in message.task_name:
                await self.set_person_status(
                    [uuid.UUID(person_id) for person_id in message.args[0]],
                    search_id=uuid.UUID(message.args[1]),
                    status=SearchStatus.error,
                    is_done=True,
                    description=("Maximum search retries "
                        f"count {max_retries} is reached"),
                )
            self.logger.warning(
                "Task '%s' invocation failed. Maximum retries count is reached.",
                message.task_name,
            )
