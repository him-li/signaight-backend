from glom import Coalesce, Literal, Check, OMIT


class VtrcIgSpecs:
    is_valid_str = Check(lambda x: isinstance(x, str)
                         and x.strip(), default=OMIT)

    search_spec = (
        "users",
        [
            {
                "instagram_full_name": Coalesce("full_name", default=None),
                "instagram_user_id": Coalesce(
                    (Coalesce("pk_id", "user_id"),
                     lambda x: [str(x)] if x else None), default=None),
                "instagram_username": Coalesce(
                    ("username", lambda x: [x] if x else None), default=None),
                "instagram_is_private": Coalesce("is_private",
                                                 default=None),
                "instagram_ld_profile_picture": Coalesce("profile_pic_url",
                                                         default=None)
            }
        ]
    )

    new_search_spec = Coalesce((
        "users",
        [
            {
                "source": Literal("instagram"),
                "resource": Literal("vetric"),
                "personal_details": {
                    "name": {
                        "full_name": {
                            "instagram_full_name": Coalesce(
                                "full_name", default=None),
                        }
                    },
                    "visuals": {
                        "profile_photo": {
                            "instagram_profile_picture": Coalesce(
                                "profile_pic_url", default=None),
                        }
                    }
                },
                "network_signature": {
                    "user_id": {
                        "instagram_user_id": Coalesce(
                            (Coalesce("pk_id", "user_id"),
                             lambda x: [str(x)] if x else None),
                            default=None),
                    },
                    "username": {
                        "instagram_username": Coalesce(
                            ("username", lambda x: [x] if x else None),
                            default=None),
                    },
                    "url": {
                        "instagram_profile_url": Coalesce(
                            (
                                "username",
                                lambda x: [
                                    f"https://www.instagram.com/{x}"] if x
                                else None
                            ),
                            default=None
                        )
                    },
                    "misc": {
                        "instagram_is_private": Coalesce(
                            "is_private", default=None),
                    }
                },
            }
        ]
    ), default=None)

    feed_spec = Coalesce((
        Coalesce("items", "media"),
        [
            {
                "instagram_post_text": Coalesce(
                    "caption.text", default=""),
                "instagram_post_id": Coalesce(
                    Coalesce("pk", "media_id"), default=None),
                "instagram_user_id": Coalesce(
                    Coalesce("user.pk_id", "coauthor_producers.0.id"),
                    default=None),
                "instagram_post_location": {
                    "instagram_location_id": Coalesce(
                        "location.pk_id", default=None),
                    "fb_location_id": Coalesce(
                        "location.facebook_places_ids", default=None),
                    "instagram_location_name": Coalesce(
                        "location.name", default=None),
                    "instagram_location_address": Coalesce(
                        "location.address", default=None),
                    "instagram_location_city": Coalesce(
                        "location.city", default=None),
                },
                "tagged_profiles": Coalesce((
                    "usertags.in",
                    [
                        {
                            "instagram_id": Coalesce(
                                "user.pk_id", default=None),
                            "instagram_username": Coalesce(
                                "user.username", default=None),
                            "instagram_full_name": Coalesce(
                                "user.full_name", default=None),
                            "instagram_is_private": Coalesce(
                                "user.is_private", default=None),
                            "instagram_is_verified": Coalesce(
                                "user.is_verified", default=None),
                            "instagram_profile_picture": Coalesce(
                                "user.profile_pic_url", default=None),
                        }
                    ]
                ), default=[]),
                "instagram_post_likes_count": Coalesce(
                    Coalesce("like_count", "engagement.like_count"),
                    default=None),
                "post_likers": Coalesce((
                    "top_likers",
                    [
                        {
                            "instagram_id": Coalesce(
                                "pk_id", default=None),
                            "instagram_username": Coalesce(
                                "username", default=None),
                            "instagram_full_name": Coalesce(
                                "full_name", default=None),
                            "instagram_is_private": Coalesce(
                                "is_private", default=None),
                            "instagram_is_verified": Coalesce(
                                "is_verified", default=None),
                            "instagram_profile_picture": Coalesce(
                                "profile_pic_url", default=None),
                        }
                    ]
                ), default=[]),
                "instagram_post_photo": Coalesce(
                    Coalesce("image_versions2.candidates.0.url",
                             "media.0.image_url"),
                    default=None)
            }
        ]
    ), default=None)

    info_spec = {
        "personal_details": {
            "name": {
                "full_name": {
                    "instagram_full_name": Coalesce(
                        "user.full_name", default=None),
                }
            },
            "visuals": {
                "profile_photo": {
                    "instagram_profile_picture": Coalesce(
                        Coalesce(
                            "user.hd_profile_pic_url_info.url",
                            "user.profile_pic_url"), default=None),
                }
            }
        },
        "biographic_details": {
            "description_bio_intro": {
                "instagram_bio": Coalesce("user.biography", default=None),
                "biography_with_entities": Coalesce((
                    ("user.biography_with_entities.entities"),
                    [
                        {
                            "instagram_userid": Coalesce(
                                "id", default=None),
                            "instagram_username": Coalesce(
                                "username", default=None),

                        }
                    ]), default=None),
                "instagram_fb_link_on_profile": Coalesce(
                    "user.show_fb_link_on_profile", default=None),
                "instagram_bio_links": Coalesce(
                    "user.external_url", default=None),
            }
        },
        "network_signature": {
            "user_id": {
                "instagram_user_id": Coalesce(
                    (Coalesce("user.pk_id", "user.user_id"),
                        lambda x: [str(x)] if x else None),
                    default=None),
            },
            "username": {
                "instagram_username": Coalesce(
                    ("user.username", lambda x: [x] if x else None),
                    default=None),
            },
            "online_signature": {
                "instagram_followers_count": Coalesce(
                    "user.follower_count", default=None),
                "instagram_following_count": Coalesce(
                    "user.following_count", default=None),
                "instagram_following_tag_count": Coalesce(
                    "user.following_tag_count", default=None),
                "instagram_posts_count": Coalesce(
                    "user.media_count", default=None),
            },
            "misc": {
                "instagram_is_private": Coalesce(
                    "user.is_private", default=None),
                "instagram_is_verified": Coalesce(
                    "user.is_verified", default=None),
                "instagram_is_buisness": Coalesce(
                    "user.is_buisness", default=None),
            }
        },
    }

    url_resolver_spec = {
        "instagram_user_id": Coalesce("author_id", default=None),
        "instagram_username": Coalesce("author_name", default=None),
        "title": Coalesce("title", default=None),
        "image": Coalesce("thumbnail_url", default=None),
        "instagram_profile_url": Coalesce("author_url", default=None),
    }

    usernameinfo_spec = {
        'username': 'user.username',
        'full_name': 'user.full_name',
        'profile_pic_url': 'user.profile_pic_url',
        'biography': 'user.biography',
        'external_url': 'user.external_url',
        'follower_count': 'user.follower_count',
        'following_count': 'user.following_count',
        'user_id': Coalesce(Coalesce('user.pk_id', 'user.user_id'),
                            default=None)
    }

    following_spec = Coalesce((
        "users",
        [
            {
                "instagram_user_id": Coalesce(("user_id", is_valid_str),
                                              ("pk_id", is_valid_str),
                                              default=None),
                "instagram_username": Coalesce("username", default=None),
                "instagram_full_name": Coalesce("full_name", default=None),
                "instagram_is_private": Coalesce("is_private", default=None),
                "instagram_profile_picture": Coalesce("profile_pic_url",
                                                      default=None),
                "instagram_profile_picture_id": Coalesce("profile_pic_id",
                                                         default=None),
                "instagram_is_verified": Coalesce("is_verified", default=None),
            }
        ]
    ), default=None)

    followers_spec = Coalesce((
        "users",
        [
            {
                "instagram_user_id": Coalesce(("user_id", is_valid_str),
                                              ("pk_id", is_valid_str),
                                              default=None),
                "instagram_username": Coalesce("username", default=None),
                "instagram_full_name": Coalesce("full_name", default=None),
                "instagram_is_private": Coalesce("is_private", default=None),
                "instagram_profile_picture": Coalesce("profile_pic_url",
                                                      default=None),
                "instagram_is_verified": Coalesce("is_verified", default=None),
            }
        ]
    ), default=None)
