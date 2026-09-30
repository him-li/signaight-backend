# flake8: noqa
import re
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse
import uuid
from beanie import free_fall_migration

FACEBOOK_HOSTS = {
    "facebook.com", "www.facebook.com", "m.facebook.com",
    "fb.com", "www.fb.com", "web.facebook.com"
}
INSTAGRAM_HOSTS = {"instagram.com", "www.instagram.com"}
LINKEDIN_HOSTS = {"linkedin.com", "www.linkedin.com"}
X_HOSTS = {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}

PLATFORM_TOKENS = {
    "fb": "facebook", "facebook": "facebook",
    "ig": "instagram", "instagram": "instagram",
    "li": "linkedin", "linkedin": "linkedin",
    "tw": "twitter", "twitter": "twitter", "x": "twitter",
}

# ---- Legacy token -> new field mapping ------------------------------------------
POST_TOKENS      = {"post", "posts", "status", "tweet", "caption", "media", "story", "stories"}
PAGE_TOKENS      = {"page", "pages", "profile", "profiles", "group", "groups", "channel", "channels", "account", "accounts", "user", "users", "people"}
FRIENDS_TOKENS      = {"friend", "friends", "following", "follower", "followers"}
LOCATION_TOKENS  = {"location", "locations", "place", "places", "geo", "city", "country", "address"}


def _infer_platform_from_urls(*urls):
    for u in urls:
        if not u:
            continue
        try:
            host = urlparse(u).netloc.lower()
        except Exception:
            continue
        if host in FACEBOOK_HOSTS or host.endswith(".facebook.com") or host.endswith(".fb.com"):
            return "facebook"
        if host in INSTAGRAM_HOSTS:
            return "instagram"
        if host in LINKEDIN_HOSTS:
            return "linkedin"
        if host in X_HOSTS:
            return "twitter"
    return None

def _first_non_empty(*vals):
    for v in vals:
        if v not in (None, "", [], {}):
            return v
    return None

def _tokenize_legacy_field(field: Optional[str]) -> List[str]:
    if not field:
        return []
    # split by anything non-alphanumeric; keep lowercase tokens, drop empties
    return [t for t in re.split(r"[^a-z0-9]+", field.lower()) if t]

def _parse_legacy_field(legacy_field: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Returns (platform, new_field) inferred from a free-form legacy field.
    Examples:
      - "fb_post_text"                  -> ("facebook", "post")
      - "instagram_post_text"          -> ("instagram", "post")
      - "linkedin_post_text"           -> ("linkedin", "post")
      - "interests.pages.fb_page_id"   -> ("facebook", "page")
      - "following friends"            -> (None, "page")
      - "interests.locations"          -> (None, "locations")
    """
    toks = _tokenize_legacy_field(legacy_field)
    if not toks:
        return None, None

    # platform: prefer first token if recognized, else any recognized token
    platform = None
    if toks and toks[0] in PLATFORM_TOKENS:
        platform = PLATFORM_TOKENS[toks[0]]
    if platform is None:
        for t in toks:
            if t in PLATFORM_TOKENS:
                platform = PLATFORM_TOKENS[t]
                break

    # new field detection by tokens
    new_field = None
    if any(t in POST_TOKENS for t in toks):
        new_field = "post"
    elif any(t in PAGE_TOKENS for t in toks):
        new_field = "page"
    elif any(t in FRIENDS_TOKENS for t in toks):
        new_field = "friend"
    elif any(t in LOCATION_TOKENS for t in toks):
        new_field = "locations"

    return platform, new_field

_INSIGHT_LOCATIONS_PATTERNS = (
    re.compile(r"\bperson\s+has\s+check-?ins?\b", re.IGNORECASE),
    re.compile(r"\bperson\s+has\s+locations?\b", re.IGNORECASE),
)

def _insight_implies_locations(text: Optional[str]) -> bool:
    if not text:
        return False
    return any(p.search(text) for p in _INSIGHT_LOCATIONS_PATTERNS)

def _decide_field_and_platform(old: dict) -> tuple[str, str | None]:
    src = old.get("source") or {}
    legacy_platform, legacy_field = _parse_legacy_field(old.get("field"))

    # If legacy gives us both, we're done.
    if legacy_field and legacy_platform:
        return legacy_field, legacy_platform

    # If legacy gives us only field or only platform, keep it and fill the other via URLs.
    url_platform = _infer_platform_from_urls(
        src.get("eb_post_url"),
        src.get("eb_fb_page_url"),
        src.get("eb_fb_profile_url"),
    )
    platform = legacy_platform or url_platform
    
    if _insight_implies_locations(src.get("eb_auto_insight")):
        return "locations", platform

    # Determine field from legacy or content
    if legacy_field:
        new_field = legacy_field
    else:
        # Content-based fallback
        if any(_first_non_empty(src.get(k)) for k in ("eb_post_text", "eb_post_url", "eb_post_photo")):
            new_field = "post"
        elif any(_first_non_empty(src.get(k)) for k in ("eb_fb_page_url", "eb_fb_page_profile_photo")):
            new_field = "page"
        elif any(_first_non_empty(src.get(k)) for k in ("eb_location", "eb_locations")):
            new_field = "locations"
        elif any(_first_non_empty(src.get(k)) for k in ("eb_fb_profile_url", "eb_profile_picture")):
            new_field = "friend"
        else:
            new_field = "post"  # safe default

    return new_field, platform

def migrate_factor(old: dict, is_watch_list:bool) -> dict:
    src = old.get("source") or {}

    new_field, platform = _decide_field_and_platform(old)

    new_source = {
        "insight": _first_non_empty(src.get("eb_auto_insight")),
        "url": _first_non_empty(
            src.get("eb_post_url"),
            src.get("eb_fb_page_url"),
            src.get("eb_fb_profile_url"),
        ),
        "photo": _first_non_empty(
            src.get("eb_post_photo"),
            src.get("eb_fb_page_profile_photo"),
            src.get("eb_profile_picture"),
        ),
        "text": None if is_watch_list else _first_non_empty(src.get("eb_post_text")),
        "date": _first_non_empty(src.get("eb_post_date")),  # keep raw; coerce upstream or reuse your ISO helper
        "location": _first_non_empty(src.get("eb_location")),
    }

    return {
        "verified": bool(old.get("verified", False)),
        "field": new_field,          # 'post' | 'page' | 'locations'
        "platform": platform,        # 'facebook' | 'instagram' | 'linkedin' | 'twitter' | None
        "source": new_source,
        "check": old.get("check"),
        "success": bool(old.get("success", False)),
        "ratio": old.get("ratio"),
    }
    

def migrate_many(items: Iterable[Dict[str, Any]], is_watch_list:bool) -> List[Dict[str, Any]]:
    return [migrate_factor(it, is_watch_list) for it in items]

class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_flags_model(self, session):
        db = session.client.get_default_database()
        flag_delete_ids = []
        flags_to_instert = []

        async for person in db.persons.find({}, session=session):
            person_id = person.get("_id")
            flags = await db.person_flags.find({"person.$id": person_id}).to_list()
            if flags:

                for flag in flags:
                    _set = {
                        "illegal_immigration": None,
                        "islamic_extremism": None,
                        "substance": None,
                        "sexual_misconduct": None,
                        "bragging_exceptional_lifestyle": None,
                        "activism": None,
                        "terror_conviction": None,
                        "online_radicalization": None,
                        "pro_palestinian_statements": None,
                        "suicidal_ideation": None,
                        "watchlist_countries": None,
                        "weapons": None,
                        "_id": uuid.uuid4(),
                    }
                    _set["person"] = flag.get("person")
                    flag_delete_ids.append(flag.get("_id"))
                    for key, value in flag.items():
                        updated_flag = None
                        if(value is not None and key not in ('person', '_id')):
                            oldFlag = value
                            updated_flag = oldFlag
                            if key == 'watchlist_countries':
                                updated_flag['description'] = ""
                            sub_categories = oldFlag.get('sub_categories')
                            for sub_category in sub_categories:
                                factors = sub_category.get("factors")
                                if key == 'watchlist_countries' and factors and factors[0]['source']:
                                    updated_flag['description'] = updated_flag['description'] + ", " + factors[0]['source']['eb_post_text'] if updated_flag['description'] else factors[0]['source']['eb_post_text']
                                    updated_flag['description'] = ", ".join(dict.fromkeys(updated_flag['description'].split(", "))) if updated_flag['description'] else ""
                                    sub_category['description'] = factors[0]['source']['eb_post_text']
                                sub_category['factors'] = migrate_many(factors, key == 'watchlist_countries')
                            _set[key] = updated_flag
                    flags_to_instert.append(_set)
                await  db.person_flags.delete_many({"_id": {"$in": flag_delete_ids}}, session=session)

        for data in flags_to_instert:
            await db.person_flags.insert_one(data, session=session)

        async for flag in db.person_flags.find({}, session=session):
            flag_person_id = flag.get("person").id
            flag_person = await db.persons.find(
                {"_id": flag_person_id}, session=session
            ).to_list()
            if not flag_person:
                await db.person_flags.delete_one(
                    {"_id": flag.get("_id")}, session=session
                )
                               

class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_revert_flags_migration(self, session):
        db = session.client.get_default_database()
        async for flag in db.person_flags.find({}, session=session):
            flag_person = flag.get("person")
            for key, value in flag.items():
                if(value is not None and key not in ('person', '_id')):
                    new_flag = {**value, "person": flag_person, "_id": uuid.uuid4()}
                    await db.person_flags.insert_one(
                        new_flag
                    )
            await db.person_flags.delete_one({"_id": flag.get("_id")})
