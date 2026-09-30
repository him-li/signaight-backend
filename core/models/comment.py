from datetime import datetime
from typing import Optional
from pydantic import Field

from .base import SignAIghtSchema
from .audit_log import AuditLogUser


class Comment(SignAIghtSchema):
    text: str
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, examples=[str(datetime.now().isoformat())]
    )
    created_by: Optional[AuditLogUser] = None
