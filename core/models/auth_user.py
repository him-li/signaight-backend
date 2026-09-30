import uuid
from datetime import datetime

from pydantic import EmailStr, Field
from pymongo import ASCENDING, IndexModel

from .base import Document


class AuthUserModel(Document):
    email: EmailStr
    password_hash: str
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    email_verified: bool = True
    permissions: list[str] = Field(default_factory=lambda: ["signaight:user"])
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "auth_users"
        indexes = [
            IndexModel(
                [("email", ASCENDING)],
                name="auth_users_email_unique",
                unique=True,
            )
        ]

