from glom import T, Coalesce, SKIP, S

from core.clients.grayfox.mapping.utils import (
    non_empty_str,
)


linkedin_block = (
    Coalesce(
        (
            S(profiles=T["data"]["profiles"]),
            T["data"]["socials"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "linkedin"
                    and i.get("profile")
                    else SKIP
                )
            ],
            T[0]["profile"],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "linkedin_f_name": Coalesce("first_name", default=None)
                        },
                        "last_name": {
                            "linkedin_l_name": Coalesce("last_name", default=None)
                        },
                    },
                    "visuals": {
                        "profile_photo": {
                            "linkedin_profile_picture": Coalesce(
                                (
                                    S["profiles"],
                                    [
                                        lambda p: (
                                            p.get("profile_pic")
                                            if isinstance(p, dict)
                                            and p.get("source") == "linkedin"
                                            and non_empty_str(p.get("profile_pic"))
                                            else SKIP
                                        )
                                    ],
                                    T[0],
                                ),
                                ("photo", lambda x: (
                                    x if isinstance(
                                        x, str) and x.strip() else None
                                ),),
                                default=None,
                            )
                        },
                        "linkedin_cover_photo": Coalesce(
                            "background_image", default=None
                        ),
                    },
                    "location": {
                        "current_city_region_country": {
                            "linkedin_location": Coalesce("location", default=None)
                        },
                        "linkedin_country_code": Coalesce("country_code", default=None),
                    },
                },
                "biographic_details": {
                    "description_bio_intro": {
                        "linkedin_profile_description": Coalesce(
                            ("description", non_empty_str), default=None
                        )
                    }
                },
                "network_signature": {
                    "url": {"linkedin_profile_url": Coalesce(("url", lambda x: [x] if x else None), default=None)},
                    "username": {"linkedin_username": Coalesce(("alias", lambda x: [x] if x else None), default=None)},
                    "user_id": {"linkedin_user_id": Coalesce(("fs_id", lambda x: [x] if x else None), default=None)},
                },
                "source": Coalesce("source", default="linkedin"),
            },
        ),
        default=None,
    ),
)
