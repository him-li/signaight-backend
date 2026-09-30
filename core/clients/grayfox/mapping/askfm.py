from glom import T, Coalesce, SKIP, Check

from core.clients.grayfox.mapping.utils import non_empty_list


askfm_block = (
    Coalesce(
        (
            T["data"]["profiles"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get(
                        "source") == "askfm" else SKIP
                )
            ],
            T[0],
            {
                "network_signature": {
                    "url": {
                        "askfm_profile_url": Coalesce(
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
                        "askfm_username": Coalesce(
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
