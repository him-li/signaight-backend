from typing import List, Optional
from core.models import PersonModel
from core.models.connections import Connections, Following, Friends


def merge_connections(persons: List[PersonModel]) -> Optional[Connections]:
    merged = Connections()

    for p in persons:
        if not p.connections:
            continue

        # ---- FRIENDS ----
        if p.connections.friends and p.connections.friends.facebook:
            if not merged.friends:
                merged.friends = Friends(facebook=[])

            merged.friends.facebook.extend(p.connections.friends.facebook)

        # ---- FOLLOWING ----
        if p.connections.following:
            if not merged.following:
                merged.following = Following(facebook=[], instagram=[])

            if p.connections.following.facebook:
                merged.following.facebook.extend(p.connections.following.facebook)

            if p.connections.following.instagram:
                merged.following.instagram.extend(p.connections.following.instagram)

    if merged.friends or merged.following:
        return merged

    return None
