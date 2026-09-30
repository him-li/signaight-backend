from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list

goodreads_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict) and i.get("source") == "goodreads"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "goodreads_f_name": Coalesce(
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
                            "goodreads_l_name": Coalesce(
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
                    "visuals": {
                        "profile_photo": {
                            "goodreads_profile_picture": Coalesce(
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
                    "location": {
                        "goodreads_location": Coalesce(
                            (
                                T.get("city"),
                                lambda x: (
                                    x if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    },
                    "gender": {
                        "goodreads_gender": Coalesce(
                            (
                                T.get("gender"),
                                lambda x: (
                                    x if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    },
                    "birth_year_birthday": {
                        "birthday": {
                            "goodreads_birth_date": Coalesce(
                                (
                                    T.get("date_of_birth"),
                                    lambda x: (
                                        x if isinstance(
                                            x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        }
                    },
                },
                "network_signature": {
                    "user_id": {
                        "goodreads_user_id": Coalesce(
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
                    "url": {
                        "goodreads_profile_url": Coalesce(
                            (T.get("profile_urls"), Check(non_empty_list)),
                            (
                                T.get("profile_url"),
                                Check(lambda x: isinstance(
                                    x, str) and x.strip()),
                                lambda x: [x]
                            ),
                            default=None,
                        )
                    },
                    "username": {
                        "goodreads_username": Coalesce(
                            (
                                T.get("username"),
                                lambda x: (
                                    x if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    },
                },
                "biographic_details": {
                    "description_bio_intro": {
                        "goodreads_bio": Coalesce(
                            (
                                T.get("bio"),
                                lambda x: (
                                    x if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
