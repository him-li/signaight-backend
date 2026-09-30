from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import non_empty_str


microsoft_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict) and i.get("source") == "microsoft"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "microsoft_f_name": Coalesce(
                                (
                                    T.get("firstname"),
                                    lambda x: (
                                        x if isinstance(
                                            x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                        "last_name": {
                            "microsoft_l_name": Coalesce(
                                (
                                    T.get("lastname"),
                                    lambda x: (
                                        x if isinstance(
                                            x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                    },
                    "gender": {
                        "microsoft_gender": Coalesce(T.get("gender"),
                                                     default=None)
                    },
                    "location": {
                        "microsoft_location": Coalesce(
                            ("extras.body_location", non_empty_str),
                            default=None,
                        )
                    },
                    "birth_year_birthday": {
                        "birthday": {
                            "microsoft_birthday": Coalesce(
                                (
                                    T.get("birthday"),
                                    lambda x: (
                                        x if isinstance(
                                            x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        }
                    },
                    "languages": {
                        "microsoft_language": Coalesce(
                            {
                                "language": "extras.language",
                            },
                            default=None,
                        )
                    },
                    "visuals": {
                        "profile_photo": {
                            "microsoft_profile_picture": Coalesce(
                                (
                                    T.get("profile_pic"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and (
                                            x.startswith("http")
                                            or x.startswith("data:image")
                                        )
                                        else None
                                    ),
                                ),
                                default=None,
                            )
                        }
                    },
                },
                "network_signature": {
                    "user_id": {
                        "microsoft_user_id": Coalesce(
                            (
                                T.get("profile_id"),
                                lambda x: (
                                    [x] if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    },
                    "misc": {
                        "microsoft_last_seen": Coalesce(
                            "extras.last_seen", default=None
                        ),
                        "microsoft_creation_date": Coalesce(
                            "extras.creation_date", default=None
                        ),
                    },
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
