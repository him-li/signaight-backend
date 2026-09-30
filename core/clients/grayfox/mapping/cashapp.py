from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import (
    non_empty_str,
)


cashapp_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get(
                        "source") == "cashapp" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "cashapp_f_name": Coalesce(
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
                            "cashapp_l_name": Coalesce(
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
                            "cashapp_profile_picture": Coalesce(
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
                        "cashapp_location": Coalesce(
                            ("extras.body_location", non_empty_str),
                            default=None,
                        )
                    },
                },
                "network_signature": {
                    "user_id": {
                        "cashapp_user_id": Coalesce(
                            ("profile_id", lambda x: [x] if x else None),
                            default=None
                        )
                    },
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
