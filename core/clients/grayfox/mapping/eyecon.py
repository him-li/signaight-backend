from glom import T, Coalesce, SKIP


eyecon_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get("source") == "eyecon" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "eyecon_f_name": Coalesce(
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
                            "eyecon_l_name": Coalesce(
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
                    "visuals": {
                        "profile_photo": {
                            "eyecon_profile_picture": Coalesce(
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
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
