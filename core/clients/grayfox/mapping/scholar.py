from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list

scholar_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get(
                        "source") == "scholar" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "scholar_f_name": Coalesce(
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
                            "scholar_l_name": Coalesce(
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
                            "scholar_profile_picture": Coalesce(
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
                    "url": {
                        "scholar_profile_url": Coalesce(
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
                        "scholar_username": Coalesce(
                            (
                                T.get("username"),
                                lambda x: (
                                    [x] if isinstance(
                                        x, str) and x.strip() else None
                                ),
                            ),
                            default=None,
                        )
                    },
                    "user_id": {
                        "scholar_user_id": Coalesce(
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
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
