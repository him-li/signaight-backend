from glom import T, Coalesce, SKIP, Check
import pendulum

from core.clients.grayfox.mapping.utils import (
    non_empty_list,
)


deezer_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get(
                        "source") == "deezer" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "visuals": {
                        "profile_photo": {
                            "deezer_profile_picture": Coalesce(
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
                    "birth_year_birthday": {
                        "birthday": {
                            "deezer_birth_date": Coalesce(
                                (
                                    T.get("date_of_birth"),
                                    (
                                        lambda x: (
                                            pendulum.from_timestamp(x)
                                            .in_timezone("UTC")
                                            .to_datetime_string()
                                            if isinstance(x, int)
                                            and pendulum.from_timestamp(x)
                                            .in_timezone("UTC")
                                            .to_datetime_string()
                                            else None
                                        )
                                    ),
                                ),
                                default=None,
                            )
                        }
                    },
                    "gender": {
                        "deezer_gender": Coalesce(
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
                },
                "network_signature": {
                    "user_id": {
                        "deezer_user_id": Coalesce(
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
                        "deezer_profile_url": Coalesce(
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
                        "deezer_username": Coalesce(
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
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
