from typing import List, Optional
from core.models import PersonModel
from core.models.interests import Interests


def merge_interests(persons: List[PersonModel]) -> Optional[Interests]:
    merged = Interests()

    for p in persons:
        interests = p.interests
        if not interests:
            continue

        # ---- pages ----
        pages = getattr(interests, "pages", None)
        if pages:
            merged.pages = (merged.pages or []) + pages

        # ---- groups.telegram_groups ----
        groups = getattr(interests, "groups", None)
        telegram_groups = getattr(groups, "telegram_groups", None) if groups else None

        if telegram_groups:
            if not merged.groups:
                merged.groups = {}
            merged.groups["telegram_groups"] = (
                merged.groups.get("telegram_groups", []) + telegram_groups
            )

        # ---- xing_interests_hobbies (OPTIONAL FIELD!) ----
        xing_hobbies = getattr(interests, "xing_interests_hobbies", None)
        if xing_hobbies:
            merged.xing_interests_hobbies = (
                getattr(merged, "xing_interests_hobbies", None) or []
            ) + xing_hobbies

    if merged.model_dump(exclude_none=True):
        return merged

    return None
