from typing import Optional

from core.config import Settings as CoreSettings


class Settings(CoreSettings):
    VETRIC_INSTAGRAM_API_KEY: Optional[str] = None
    SOCIAL_LINKS_API_KEY: Optional[str] = None
    VETRIC_INSTAGRAM_API_CANDIDATE_POSTS_LIMIT: int = 100
    VETRIC_INSTAGRAM_API_CANDIDATE_FOLLOWING_LIMIT: int = 100
    VETRIC_INSTAGRAM_API_CANDIDATE_FOLLOWERS_LIMIT: int = 100


settings = Settings()
