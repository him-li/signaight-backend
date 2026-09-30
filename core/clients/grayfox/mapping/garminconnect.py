from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list, non_empty_str

garminconnect_block = Coalesce(
    (
        T["data"]["profiles"],
        [
            lambda i: (
                i
                if isinstance(i, dict) and i.get("source") == "garmin"
                else SKIP
            )
        ],
        T[0],
        {
            "personal_details": {
                "name": {
                    "first_name": {
                        "garminconnect_f_name": Coalesce(
                            (T.get("firstname"), non_empty_str),
                            default=None,
                        )
                    },
                    "last_name": {
                        "garminconnect_l_name": Coalesce(
                            (T.get("lastname"), non_empty_str),
                            default=None,
                        )
                    },
                },
                "visuals": {
                    "profile_photo": {
                        "garminconnect_profile_picture": Coalesce(
                            (
                                T.get("profile_pic"),
                                lambda x: (
                                    x
                                    if isinstance(x, str)
                                    and x.startswith("http")
                                    else None
                                ),
                            ),
                            default=None,
                        )
                    }
                },
                "location": {
                    "garminconnect_location": Coalesce(
                        (T.get('city'),
                         lambda x: x if isinstance(x, str) and
                         x.strip() else None),
                        default=None)
                },
            },
            "network_signature": {
                "user_id": {
                    "garminconnect_user_id": Coalesce(
                        (
                            T.get("profile_id"),
                            lambda x: (
                                [x]
                                if isinstance(x, str) and x.strip()
                                else None
                            ),
                        ),
                        default=None,
                    )
                },
                "url": {
                    "garminconnect_profile_url": Coalesce(
                        (T.get("profile_urls"), Check(non_empty_list)),
                        (
                            T.get("profile_url"),
                            lambda x: (
                                [x]
                                if isinstance(x, str)
                                and x.startswith("http")
                                else None
                            ),
                        ),
                        default=None,
                    )
                },
                "username": {
                    "garminconnect_username": Coalesce(
                        (T.get("username"), lambda x: [x] if x else None),
                        default=None
                    )
                },
            },
            "biographic_details": {
                "description_bio_intro": {
                    "garminconnect_bio": Coalesce(
                        (T.get("bio"), non_empty_str), default=None
                    )
                }
            },
            "source": T["source"],
        },
    ),
    default=None,
),
