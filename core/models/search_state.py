from enum import Enum
from typing import Optional

from .base import SignAIghtSchema


class SearchStatus(str, Enum):
    in_progress = 'In progress'
    success = 'Success'
    error = 'Error'
    timeout = 'Timeout'


class SearchState(SignAIghtSchema):
    is_done: bool = False
    status: SearchStatus = SearchStatus.in_progress
    description: Optional[str] = None
