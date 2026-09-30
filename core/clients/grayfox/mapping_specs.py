import importlib
import re
import pendulum
from glom import Coalesce, T, glom

from core.clients.grayfox.mapping.utils import is_http_url, non_empty_str
from core.utils.socials_list import PROFILE_SOCIALS
from .mapping.details_part import details_part_block


def sanitize_source(s):
    s = (s or "").strip().lower()
    s = re.sub(r"\W+", "_", s).strip("_")
    return s or "unknown"


def pick_best_url(p):
    urls = p.get("profile_urls")
    if isinstance(urls, list):
        for u in urls:
            u2 = is_http_url(u)
            if u2:
                return u2
    return is_http_url(p.get("profile_url"))


def to_str(x):
    if x is None:
        return None
    s = str(x).strip()
    return s or None


def score_profile(p):
    score = 0
    if non_empty_str(p.get("firstname")):
        score += 1
    if non_empty_str(p.get("lastname")):
        score += 1
    if pick_best_url(p):
        score += 3
    if is_http_url(p.get("profile_pic")):
        score += 2
    if non_empty_str(to_str(p.get("profile_id"))):
        score += 3
    last_seen = (p.get("extras") or {}).get("last_seen") or ""
    if isinstance(last_seen, str) and last_seen:
        score += 1
    return score


def transform_profile_block(p):
    """Build your normalized block with dynamic, source-prefixed leaf keys."""
    src = sanitize_source(p.get("source"))
    first_name_key = f"{src}_f_name"
    last_name_key = f"{src}_l_name"
    photo_key = f"{src}_profile_picture"
    user_id_key = f"{src}_user_id"
    url_key = f"{src}_profile_url"

    return {
        "personal_details": {
            "name": {
                "first_name": {first_name_key: non_empty_str(
                    p.get("firstname"))},
                "last_name": {last_name_key: non_empty_str(p.get("lastname"))},
            },
            "visuals": {
                "profile_photo": {photo_key: is_http_url(p.get("profile_pic"))}
            },
        },
        "network_signature": {
            "user_id": {user_id_key: non_empty_str(
                to_str(p.get("profile_id")))},
            "url": {url_key: pick_best_url(p)},
        },
        "source": p.get("source"),
    }


def profiles_by_source(root, include=None, exclude=None):
    profs = (root or {}).get("data", {}).get("profiles", []) or []
    include_norm = (
        {sanitize_source(s) for s in include} if include is not None else None
    )
    exclude_norm = {sanitize_source(s) for s in (exclude or set())}

    groups = {}
    for p in profs:
        src = sanitize_source(p.get("source"))
        if src in exclude_norm:
            continue
        if include_norm is not None and src not in include_norm:
            continue
        groups.setdefault(src, []).append(p)

    out = {}
    for src, items in groups.items():
        best = None
        best_score = -1
        for p in items:
            s = score_profile(p)
            if s > best_score:
                best = p
                best_score = s
        if best is not None and best_score > 0:
            out[src] = transform_profile_block(best)
    return out or None


def build_request_details(root):
    base = {}
    try:
        evaluated_details = {
            k: glom(root, v, default=None)
            for k, v in details_part_block.items()
        }
        mapping = importlib.import_module("core.clients.grayfox.mapping")
        for name in getattr(mapping, "__all__", []):
            if not name.endswith("_block"):
                continue

            platform = name.removesuffix("_block")

            block = getattr(mapping, name, None)

            base[platform] = glom(root, block, default=None) if block else None

        base.update(evaluated_details)
    except Exception as e:
        print("ERROR building base", e)

    mapping = {k: v for k, v in base.items() if v is not None}

    dyn = (
        profiles_by_source(
            root, include=PROFILE_SOCIALS, exclude=list(
                base.keys()) + ["garmin"]
        )
        or {}
    )

    # merge (static keys win if name collision somehow happens)
    out = {**dyn, **mapping}
    return out or None


class GrfxSpecs:

    get_request_details_spec = Coalesce(
        (T, build_request_details), default=None)

    get_active_search_results = Coalesce(
        (
            "data.items",
            [
                {
                    "personal_details": {
                        "name": {
                            "full_name": {
                                "linkedin_full_name": Coalesce(
                                    "full_name", default=None
                                ),
                                "full_name": Coalesce("full_name",
                                                      default=None),
                            },
                            "first_name": {
                                "f_name": Coalesce(
                                    (
                                        "full_name",
                                        lambda x: (
                                            x.split(" ")[0]
                                            if x and isinstance(x, str)
                                            else None
                                        ),
                                    ),
                                    default=None,
                                )
                            },
                            "last_name": {
                                "l_name": Coalesce(
                                    (
                                        "full_name",
                                        lambda x: (
                                            " ".join(x.split(" ")[1:])
                                            if x and isinstance(x, str)
                                            else None
                                        ),
                                    ),
                                    default=None,
                                )
                            },
                        },
                        "location": {
                            "current_country": {
                                "linkedin_location_country": Coalesce(
                                    "country_name", default=None
                                )
                            },
                            "current_city_region_country": {
                                "linkedin_location": Coalesce(
                                    "location_name", default=None
                                )
                            },
                        },
                        "visuals": {
                            "profile_photo": {
                                "linkedin_profile_picture": Coalesce(
                                    "photo_url", default=None
                                )
                            }
                        },
                        "languages": {
                            "li_languages": Coalesce(
                                (
                                    "languages",
                                    [
                                        {
                                            "language": "name",
                                            "proficiency": Coalesce(
                                                "proficiency", default=None
                                            ),
                                        }
                                    ],
                                ),
                                default=None,
                            )
                        },
                    },
                    "biographic_details": {
                        "work": {
                            "linkedin_work": {
                                "positions": Coalesce(
                                    (
                                        "positions",
                                        [
                                            {
                                                "title": Coalesce(
                                                    "title", default=None
                                                ),
                                                "location": Coalesce(
                                                    "location_name",
                                                    default=None
                                                ),
                                                "description": Coalesce(
                                                    "description", default=None
                                                ),
                                                "period": {
                                                    "date_from": Coalesce(
                                                        (
                                                            "from_date",
                                                            lambda x: (
                                                                pendulum.parse(
                                                                    x,
                                                                    strict=False
                                                                )
                                                                if isinstance(
                                                                    x, str)
                                                                else None
                                                            ),
                                                        ),
                                                        default=None,
                                                    ),
                                                    "date_to": Coalesce(
                                                        (
                                                            "to_date",
                                                            lambda x: (
                                                                pendulum.parse(
                                                                    x,
                                                                    strict=False
                                                                )
                                                                if isinstance(
                                                                    x, str)
                                                                else None
                                                            ),
                                                        ),
                                                        default=None,
                                                    ),
                                                },
                                                "country": Coalesce(
                                                    "country_name",
                                                    default=None
                                                ),
                                                "company_logo_url": Coalesce(
                                                    "company_logo_url",
                                                    default=None
                                                ),
                                                "company_name": Coalesce(
                                                    "company.name",
                                                    default=None
                                                ),
                                            }
                                        ],
                                    ),
                                    default=None,
                                )
                            }
                        },
                        "education": {
                            "linkedin_schools": Coalesce(
                                (
                                    "educations",
                                    [
                                        {
                                            "school_name": Coalesce(
                                                "school_name", default=None
                                            ),
                                            "degree_name": Coalesce(
                                                "activities", default=None
                                            ),
                                            "school_logo_url": Coalesce(
                                                "company_logo_url",
                                                default=None
                                            ),
                                            "period": {
                                                "date_from": Coalesce(
                                                    (
                                                        "from_date",
                                                        lambda x: (
                                                            pendulum.parse(
                                                                x, strict=False
                                                            )
                                                            if isinstance(
                                                                x, str)
                                                            else None
                                                        ),
                                                    ),
                                                    default=None,
                                                ),
                                                "date_to": Coalesce(
                                                    (
                                                        "to_date",
                                                        lambda x: (
                                                            pendulum.parse(
                                                                x, strict=False
                                                            )
                                                            if isinstance(
                                                                x, str)
                                                            else None
                                                        ),
                                                    ),
                                                    default=None,
                                                ),
                                            },
                                        }
                                    ],
                                ),
                                default=None,
                            )
                        },
                        "description_intro_bio": {
                            "linkedin_headline": Coalesce("headline",
                                                          default=None)
                        },
                    },
                    "network_signature": {
                        "user_id": {"linkedin_user_id": Coalesce(
                            ("id", lambda x: [x] if x else None),
                            default=None)},
                        "username": {
                            "linkedin_username": Coalesce(
                                ("username", lambda x: [x] if x else None),
                                default=None)
                        },
                        "url": {
                            "linkedin_profile_url": Coalesce(
                                (
                                    "username",
                                    lambda x: (
                                        [f"https://www.linkedin.com/in/{x}"]
                                        if isinstance(x, str)
                                        else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                        "online_signature": {
                            "linkedin_connections_count": Coalesce(
                                "connections_count", default=None
                            ),
                            "linkedin_followers_count": Coalesce(
                                "followers_count", default=None
                            ),
                            "linkedin_following_count": Coalesce(
                                "following_count", default=None
                            ),
                            "linkedin_is_creator": Coalesce("is_creator",
                                                            default=None),
                            "linkedin_is_influencer": Coalesce(
                                "is_influencer", default=None
                            ),
                            "linkedin_has_premium": Coalesce(
                                "is_premium", default=None
                            ),
                        },
                    },
                }
            ],
        ),
        default=None,
    )
