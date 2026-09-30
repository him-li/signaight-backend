from glom import T, Coalesce, SKIP


callapp_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get("source") == "callapp" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "visuals": {
                        "profile_photo": {
                            "callapp_profile_picture": Coalesce(
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
