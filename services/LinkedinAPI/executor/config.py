from typing import Optional

from core.config import Settings as CoreSettings


class Settings(CoreSettings):
    VETRIC_LINKEDIN_API_KEY: Optional[str] = None
    EPIEOS_API_KEY: Optional[str] = None
    VETRIC_LINKEDIN_CANDIDATES_LIMIT: Optional[int] = 100


settings = Settings()
