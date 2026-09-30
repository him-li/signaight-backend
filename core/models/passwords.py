from typing import Optional
from pydantic import SecretStr

from .base import SignAIghtSchema


class Password(SignAIghtSchema):
    domain: Optional[str] = None
    password: Optional[SecretStr] = None
