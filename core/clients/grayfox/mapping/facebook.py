from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import ensure_phone_not_empty


def skip_if_all_empty(*keys):
    def _check(d):
        if not isinstance(d, dict):
            return False
        return any(
            isinstance(d.get(k), str) and d.get(k).strip()
            for k in keys
        )
    return _check


facebook_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i
                    if (
                        isinstance(i, dict)
                        and i.get("source") == "facebook"
                        and skip_if_all_empty(
                            "firstname",
                            "lastname",
                            "profile_id",
                            "profile_pic"
                        )(i)
                    )
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "facebook_f_name": Coalesce(
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
                            "facebook_l_name": Coalesce(
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
                            "facebook_profile_picture": Coalesce(
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
                    "gender": {"fb_gender": Coalesce("profile_gender",
                                                     default=None)},
                    "phone": {
                        "fb_phone": Coalesce(
                            (T.get("extras.phone"), ensure_phone_not_empty),
                            default=None,
                        )
                    },
                },
                "network_signature": {
                    "user_id": {
                        "facebook_user_id": Coalesce(
                            ("profile_id", lambda x: [str(x)] if x else None),
                            default=None
                        )
                    },
                    "misc": {
                        "facebook_creation_date": Coalesce(
                            "extras.date_added", default=None
                        ),
                    },
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
