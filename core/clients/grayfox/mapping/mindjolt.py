from glom import T, Coalesce, SKIP


mindjolt_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "mindjolt"
                    and isinstance(i.get("facebook_id"), list)
                    and any(
                        isinstance(v, str) and v.strip()
                        for v in i.get("facebook_id", [])
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
                                        x if isinstance(x, str) and x.strip() else None
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
                                        x if isinstance(x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                    },
                    "gender": {
                        "facebook_gender": Coalesce(
                            T.get("profile_gender"), default=None
                        )
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
                },
                "network_signature": {
                    "user_id": {
                        "facebook_user_id": Coalesce(
                            (
                                T["facebook_id"],
                                lambda ids: (
                                    ids[0]
                                    if isinstance(ids, list) and len(ids) > 0
                                    else None
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
