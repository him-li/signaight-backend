from typing import List, Optional

from core.models import CandidateModel
from api.filter import Filter


class LimitsFilter(Filter):
    action: Optional[str] = None
    kind: Optional[str] = None
  