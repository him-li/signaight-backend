import datetime
import re
from typing import Iterable

from core.utils.socials_list import PROFILE_SOCIALS, SOCIALS
import pendulum


def ensure_not_empty(s: str) -> list[str] | None:
    return [s.strip()] if isinstance(s, str) and s.strip() else None


def non_empty_str(x):
    return x if isinstance(x, str) and x.strip() else None


def is_http_url(x):
    return x if isinstance(x, str) and x.startswith(("http://", "https://")) else None


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def ensure_datetime(value):
    if isinstance(value, datetime.datetime):
        return value
    else:
        return pendulum.parse(value, strict=False)


def validate_string(s: str) -> str | None:
    return s.strip() if isinstance(s, str) and s.strip() else None


def ensure_list(value):
    return value if isinstance(value, list) else [value]


def ensure_phone_not_empty(s: str | list[str]) -> list[str] | None:
    def normalize(phone):
        if not isinstance(phone, str):
            return None
        phone = phone.strip()
        if not phone or phone == "+0-000-0000":
            return None
        return phone if phone.startswith("+") else f"+{phone}"

    if isinstance(s, str):
        norm = normalize(s)
        return [norm] if norm else None
    elif isinstance(s, list):
        result = [normalize(item) for item in s]
        result = [item for item in result if item]
        return result if result else None
    return None


def non_empty_list(val: list) -> bool:
    return isinstance(val, list) and len(val) > 0


def ensure_str(s) -> str:
    return s if isinstance(s, str) else str(s)


def is_yelp_user_profile(url: str) -> bool:
    return isinstance(url, str) and "/user_details" in url and "userid=" in url


def flatten(items):
    out = []
    for i in items:
        if isinstance(i, list):
            out.extend(flatten(i))
        elif isinstance(i, str):
            out.append(i)
    return out


def build_locations(locations = []):
    location_list = [
        loc.get("location")
        for loc in locations
        if isinstance(loc, dict) and loc.get("location")
    ]
    return location_list[:3]

def build_telegram_groups(telegram):
    groups = telegram.get("groups")
    messages = telegram.get("messages")
    by_id = {
        g["telegram_public_group_id"]: {
            **g,
            "lastseen": (
                pendulum.from_timestamp(g["lastseen"]) if g.get("lastseen") else None
            ),
            "messages": [],
        }
        for g in (groups or [])
    }

    for m in messages or []:
        gid = str(m["group"]["id"])

        if gid not in by_id:
            by_id[gid] = {
                "telegram_public_group_id": gid,
                "telegram_public_group_screen_name": None,
                "title": m["group"]["title"],
                "lastseen": None,
                "messages": [],
            }

        trimmed = {
            "date": m.get("date"),
            "media_code": m.get("mediaCode"),
            "media_name": m.get("mediaName"),
            "message_id": m.get("messageId"),
            "reply_to_message_id": m.get("replyToMessageId"),
            "text": m.get("text"),
        }
        by_id[gid]["messages"].append(trimmed)

    return list(by_id.values())

def flatten(items):
    out = []
    for i in items:
        if isinstance(i, list):
            out.extend(flatten(i))
        elif isinstance(i, str):
            out.append(i)
    return out

def phone_to_mask(partial: str) -> str:
    """
    Converts '(*** ) 29*-**' → '***29***'
    Only digits or '*', formatting removed
    """
    return "".join(c for c in partial if c.isdigit() or c == '*')

def normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone)

def match_partial_phone(partial: str, full_phone: str) -> bool:
    mask = phone_to_mask(partial)
    digits = normalize_phone(full_phone)

    # Align from the right
    if len(mask) > len(digits):
        return False

    for m, d in zip(reversed(mask), reversed(digits)):
        if m == '*':
            continue
        if m != d:
            return False

    return True

def get_partial_phone_suffixes(data) -> set[str]:
    suffixes = set()

    for item in data.get("partial_recovery", []):
        if item.get("type") == "phone":
            suffix = phone_to_mask(item.get("value"))
            if suffix:
                suffixes.add(suffix)

    return suffixes


def build_phones_groups(data):
    phones_list = data.get("phones")
    phones = set()
    metadata_phone = data.get("metadata", {}).get("phone", None)
    phones.add(metadata_phone)
    for phone in phones_list or []:
        phone_number = phone.get("phone_number")
        if phone_number:
            phones.add(phone_number)

    flat_phones = flatten(phones)
    phones = ensure_phone_not_empty(flat_phones)
    if phones:
        partial_suffixes = get_partial_phone_suffixes(data)

        if not partial_suffixes:
            # fallback: return all phones if no partial recovery exists
            return None, phones

        # 3. Match phones by suffix
        matched = set()
        if isinstance(phones, Iterable):
            phones = list(phones)
        for phone in phones:
            for suffix in partial_suffixes:
                if match_partial_phone(suffix, phone):
                    matched.add(phone)
        not_matched = list(set(phones) - matched)
        return list(matched) if matched else None, not_matched if not_matched else None
    return None, None


def build_images(data):
    pictures_list = data.get('pictures')
    pictures = []
    for picture in pictures_list or []:
        source = picture.get("source")
        if source and source in (SOCIALS + PROFILE_SOCIALS):
            continue
        if picture_url := picture.get("picture"):
            pictures.append(picture_url)

    return pictures if pictures else None
