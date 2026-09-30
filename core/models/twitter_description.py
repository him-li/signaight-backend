from typing import Optional, List
from pydantic import AnyHttpUrl

from .base import WithVerifiedFieldSchema, SignAIghtSchema
from .tagged_person import TwitterTaggedPerson


class TwitterUrl(SignAIghtSchema):
    description_url_expanded: Optional[AnyHttpUrl] = None
    description_url_on_twitter: Optional[AnyHttpUrl] = None


class TwitterDescription(WithVerifiedFieldSchema):
    description_text: Optional[str] = None
    urls: Optional[List[TwitterUrl]] = None
    tagged_profiles: Optional[List[TwitterTaggedPerson]] = None
    description_hashtags: Optional[List[str]] = None
    description_symbols: Optional[List[str]] = None
