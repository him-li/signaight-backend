from typing import Optional
from pydantic import BaseModel


class LimitsView(BaseModel):
    limits: Optional[int] = None
    current: Optional[int] = None
    kind: Optional[str] = None
    allow: Optional[bool] = True
