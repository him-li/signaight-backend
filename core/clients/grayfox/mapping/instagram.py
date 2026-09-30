from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import ensure_not_empty

instagram_block = (
    Coalesce(
        (
            T["data"]["socials"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict) and i.get("source") == "instagram"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "full_name": {
                            "instagram_full_name": Coalesce("name", default=None)
                        },
                    },
                    "visuals": {
                        "profile_photo": {
                            "instagram_profile_picture": Coalesce("photo", default=None)
                        },
                    },
                },
                "network_signature": {
                    "url": {"instagram_profile_url": Coalesce(("url", lambda x: [x] if x else None), default=None)},
                    "username": {"instagram_username": Coalesce(("alias", lambda x: [x] if x else None), default=None)},
                    "user_id": {"instagram_user_id": Coalesce(("id", lambda x: [str(x)] if x else None), default=None)},
                    "biographic_details": {
                        "description_bio_intro": {
                            "instagram_bio": Coalesce(
                                ("bio", ensure_not_empty), default=None
                            )
                        }
                    },
                    "online_signature": {
                        "instagram_followers_count": Coalesce(
                            "followers_count", default=None
                        ),
                        "instagram_following_count": Coalesce(
                            "following_count", default=None
                        ),
                    },
                },
                "source": Coalesce("source", default="instagram"),
            },
        ),
        default=None,
    ),
)
