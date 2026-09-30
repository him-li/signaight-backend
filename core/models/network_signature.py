from typing import Optional, List

from .base import WithVerifiedFieldSchema
from .username import Username
from .url import URL
from .user_id import UserId
from .online_signature import OnlineSignature
from .network_misc import NetworkMisc
from .matched_profiles import MatchedProfiles
from .passwords import Password


class NetworkSignature(WithVerifiedFieldSchema):
    username: Optional[Username] = None
    url: Optional[URL] = None
    user_id: Optional[UserId] = None # type: ignore
    matched_profiles: Optional[MatchedProfiles] = None # type: ignore
    online_signature: Optional[OnlineSignature] = None
    misc: Optional[NetworkMisc] = None
    passwords: Optional[List[Password]] = None
