from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import non_empty_str, ensure_not_empty


twitter_block = (
    Coalesce(
        (
            T["data"]["socials"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "twitter"
                    and i.get("type") == "TwitterUser"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "full_name": {
                            "twitter_full_name": Coalesce("name", default=None)
                        },
                    },
                    "visuals": {
                        "profile_photo": {
                            "twitter_profile_picture": Coalesce("image",
                                                                default=None)
                        },
                        "twitter_cover_photo": Coalesce(
                            ("banner_image", non_empty_str), default=None
                        ),
                    },
                    "location": {
                        "twitter_location": Coalesce(
                            ("location", non_empty_str), default=None
                        )
                    },
                    "birth_year_birthday": {
                        "birthday": {
                            "twitter_birthdate": Coalesce("birthdate",
                                                          default=None)
                        }
                    }
                },
                "biographic_details": {
                    "description_bio_intro": {
                        "twitter_description": {
                            "description_text": Coalesce(
                                ("description", non_empty_str), default=None
                            ),
                            "urls": Coalesce(
                                ("urls", ensure_not_empty), default=None
                            ),
                        }
                    }
                },
                "network_signature": {
                    "url": {"twitter_profile_url": Coalesce(
                        ("url", lambda x: [x] if x else None),
                        default=None)},
                    "username": {"twitter_username": Coalesce(
                        ("alias", lambda x: [x] if x else None),
                        default=None)},
                    "user_id": {"twitter_user_id": Coalesce(
                        ("id", lambda x: [x] if x else None),
                        default=None)},
                    "online_signature": {
                        "twitter_followers_count": Coalesce(
                            "follower_count", default=None
                        ),
                        "twitter_following_count": Coalesce(
                            "friend_count", default=None
                        ),
                        "twitter_favorites_count": Coalesce(
                            "favorite_count", default=None
                        ),
                        "twitter_media_count": Coalesce("media_count",
                                                        default=None),
                        "twitter_created_at": Coalesce("created",
                                                       default=None),
                        "twitter_posts_count": Coalesce("tweet_count",
                                                        default=None),
                        "twitter_creator_subscription_count": Coalesce(
                            "creator_subscription_count", default=None),
                        "twitter_list_count": Coalesce("list_count",
                                                       default=None),
                        "twitter_statuses_count": Coalesce("tweet_count",
                                                           default=None),
                    },
                    "misc": {
                        "twitter_is_protected": Coalesce("is_protected",
                                                         default=None),
                        "twitter_is_blue_verified": Coalesce(
                            "is_blue_verified", default=None),
                        "twitter_is_verified": Coalesce("is_verified",
                                                        default=None),
                    }
                },
                "source": Coalesce("source", default="twitter"),
            },
        ),
        default=None,
    ),
)
