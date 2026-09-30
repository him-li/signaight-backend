from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list

chess_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get(
                        "source") == "chess" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "chess_f_name": Coalesce(
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
                            "chess_l_name": Coalesce(
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
                            "chess_profile_picture": Coalesce(
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
                        "chess_location": Coalesce(
                            (
                                T.get("extras", {}).get("body_location"),
                                Check(lambda x: isinstance(
                                    x, str) and x.strip()),
                            ),
                            default=None,
                        )
                    }
                },
                "network_signature": {
                    "url": {
                        "chess_profile_url": Coalesce(
                            (T.get("profile_urls"), Check(non_empty_list)),
                            (
                                T.get("profile_url"),
                                Check(lambda x: isinstance(
                                    x, str) and x.strip()),
                            ),
                            default=None,
                        )
                    },
                    "misc": {
                        "chess_creation_date": Coalesce(
                            (
                                T.get("extras", {}).get("creation_date"),
                                Check(lambda x: isinstance(
                                    x, str) and x.strip()),
                            ),
                            default=None,
                        ),
                        "chess_last_seen": Coalesce(
                            (
                                T.get("extras", {}).get("last_seen"),
                                Check(lambda x: isinstance(
                                    x, str) and x.strip()),
                            ),
                            default=None,
                        ),
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
