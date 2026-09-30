from glom import T, Coalesce, SKIP


apple_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get("source") == "apple" else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "first_name": {
                            "apple_f_name": Coalesce(
                                (
                                    T.get("firstname"),
                                    lambda x: (
                                        x if isinstance(x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                    },
                    "email": {"apple_email": Coalesce(T.get("email"), default=None)},
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
)
