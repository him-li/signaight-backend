from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list


foursquare_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict) and i.get("source") == "foursquare"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "foursquare_f_name": Coalesce(
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
                            "foursquare_l_name": Coalesce(
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
                            "foursquare_profile_picture": Coalesce(
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
                        "foursquare_location": Coalesce(
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
                        "foursquare_gender": Coalesce(
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
                        "foursquare_user_id": Coalesce(
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
                        "foursquare_profile_url": Coalesce(
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
                },
                "biographic_details": {
                    "description_bio_intro": {
                        "foursquare_bio": Coalesce(
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
