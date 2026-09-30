from glom import Coalesce, T, SKIP


class VtTwSpecs:

    search_spec = Coalesce((
        "users",
        [{
            "personal_details": {
                "name": {
                    "full_name": {
                        "twitter_full_name": Coalesce("name", default=None)
                    }
                },
                "location": {
                    "twitter_location":  Coalesce("location", default=None)
                },
                "visuals": {
                    "profile_photo": {
                        "twitter_profile_picture": Coalesce(
                            "profile_image_url_https", default=None),
                        "twitter_cover_photo": Coalesce(
                            "profile_banner_url", default=None),
                    }
                }
            },
            "biographic_details": {
                "description_bio_intro": {
                    "twitter_description": {
                        "description_text": Coalesce("description",
                                                     default=None),
                        "urls": Coalesce((
                            "entities.url.urls",
                            [{
                                "description_url_expanded": "expanded_url",
                                "description_url_on_twitter": "url"
                            }]
                        ), default=None),
                        "tagged_profiles": Coalesce((
                            "entities.description.user_mentions",
                            [{
                                "twitter_user_id": "id_str",
                                "twitter_full_name": "name",
                                "twitter_username": "screen_name"
                            }]
                        ), default=None),
                        "description_hashtags": Coalesce(
                            "entities.description.hashtags", default=None),
                        "description_symbols": Coalesce(
                            "entities.description.symbols", default=None)
                    }
                }
            },
            "network_signature": {
                "username": {
                    "twitter_username": Coalesce(
                        ("screen_name", lambda x: [x] if x else None),
                        default=None)
                },
                "url": {
                    "twitter_url": Coalesce(
                        ("url", lambda x: [x] if x else None), default=None)
                },
                "online_signature": {
                    "twitter_created_at": Coalesce("created_at", default=None),
                    "twitter_favorites_count": Coalesce("favourites_count",
                                                        default=None),
                    "twitter_followers_count": Coalesce("followers_count",
                                                        default=None),
                    "twitter_following_count": Coalesce("friends_count",
                                                        default=None),
                    "twitter_media_count": Coalesce("media_count",
                                                    default=None),
                    "twitter_statuses_count": Coalesce("statuses_count",
                                                       default=None),
                },
                "misc": {
                    "twitter_is_protected": Coalesce("protected",
                                                     default=None)
                }
            },
        }]
    ), default=None)

    profile_spec = Coalesce(
        {
            "personal_details": {
                "name": {
                    "full_name": {
                        "twitter_full_name": Coalesce("name", default=None)
                    }
                },
                "location": {
                    "twitter_location":  Coalesce("location", default=None)
                },
                "visuals": {
                    "profile_photo": {
                        "twitter_profile_picture": Coalesce(
                            "profile_image_url_https", default=None),
                        "twitter_cover_photo": Coalesce(
                            "profile_banner_url", default=None),
                    }
                }
            },
            "biographic_details": {
                "description_bio_intro": {
                    "twitter_description": {
                        "description_text": Coalesce("description",
                                                     default=None),
                        "urls": Coalesce((
                            "entities.url.urls",
                            [{
                                "description_url_expanded": "expanded_url",
                                "description_url_on_twitter": "url"
                            }]
                        ), default=None),
                        "tagged_profiles": Coalesce((
                            "entities.description.user_mentions",
                            [{
                                "twitter_user_id": "id_str",
                                "twitter_full_name": "name",
                                "twitter_username": "screen_name"
                            }]
                        ), default=None),
                        "description_hashtags": Coalesce(
                            "entities.description.hashtags", default=None),
                        "description_symbols": Coalesce(
                            "entities.description.symbols", default=None)
                    }
                }
            },
            "network_signature": {
                "username": {
                    "twitter_username": Coalesce("screen_name", default=None)
                },
                "user_id": {
                    "twitter_user_id": Coalesce("id_str", default=None)
                },
                "online_signature": {
                    "twitter_created_at": Coalesce("created_at", default=None),
                    "twitter_favorites_count": Coalesce("favourites_count",
                                                        default=None),
                    "twitter_followers_count": Coalesce("followers_count",
                                                        default=None),
                    "twitter_following_count": Coalesce("friends_count",
                                                        default=None),
                    "twitter_media_count": Coalesce("media_count",
                                                    default=None),
                    "twitter_statuses_count": Coalesce("statuses_count",
                                                       default=None),
                    "twitter_professional_type": Coalesce(
                        "professional.professional_type",
                        default=None),
                    "twitter_professional_category_id": Coalesce(
                        "professional.category.0.id",
                        default=None),
                    "twitter_professional_category": Coalesce(
                        "professional.category.0.name",
                        default=None),
                },
                "misc": {
                    "twitter_is_protected": Coalesce("protected",
                                                     default=None)
                }
            },
        }, default=None)

    unique_tweets_spec = Coalesce(
        {
            "twitter_post_likes_count": Coalesce("favorite_count",
                                                 default=None),
            "twitter_post_quoted_status": Coalesce("is_quote_status",
                                                   default=None),
            "twitter_post_language": Coalesce("lang", default=None),
            "twitter_post_quotes_count": Coalesce("quote_count",
                                                  default=None),
            "twitter_post_replies_count": Coalesce("reply_count",
                                                   default=None),
            "twitter_post_retweets_count": Coalesce("retweet_count",
                                                    default=None),
            "twitter_post_retweeted_status": Coalesce("retweeted",
                                                      default=None),
            "twitter_post_author_user_id": Coalesce("user_id_str",
                                                    default=None),
            "twitter_post_possibly_sensitive": Coalesce(
                "possibly_sensitive", default=None),
            "twitter_post_card": Coalesce(
                (T["tweet_card"]["binding_values"],
                    {
                    "description_text": [lambda i: i['text'] if i["key"] ==
                                         "description" else SKIP],
                    "image_url_large": [lambda i: i['image_url'] if
                                        i["key"] == "thumbnail_image_large"
                                        else SKIP],
                    "image_url_original_size": [lambda i: i['image_url'] if
                                                i["key"] == "thumbnail_image"
                                                else SKIP],
                    "text": [lambda i: i['text'] if i["key"] == "title"
                             else SKIP]
                }), default=None),
            "twitter_post_photo": Coalesce(
                (T["extended_entities"]["media"],
                    [lambda i: i["media_url_https"] if i["type"] == "photo"
                     else SKIP]), default=None),
            "post_author": Coalesce(
                {
                    "twitter_user_id": Coalesce("user_id_str",
                                                default=None),
                    "twitter_created_at": Coalesce(
                        "user_details.created_at", default=None),
                    "twitter_full_name": Coalesce("user_details.name",
                                                  default=None),
                    "twitter_username": Coalesce(
                        "user_details.screen_name", default=None),
                    "twitter_location": Coalesce(
                        "user_details.location", default=None),
                    "twitter_favourites_count": Coalesce(
                        "user_details.favourites_count", default=None),
                    "twitter_followers_count": Coalesce(
                        "user_details.followers_count", default=None),
                    "twitter_following_count": Coalesce(
                        "user_details.friends_count", default=None),
                    "twitter_media_count": Coalesce(
                        "user_details.media_count", default=None),
                    "twitter_cover_photo": Coalesce(
                        "user_details.profile_banner_url", default=None),
                    "twitter_profile_picture": Coalesce(
                        "user_details.profile_image_url_https",
                        default=None),
                    "twitter_is_protected": Coalesce(
                        "user_details.protectetd", default=None),
                    "twitter_statuses_count": Coalesce(
                        "user_details.statuses_count", default=None),
                    "twitter_description": {
                        "description_text": Coalesce(
                            "user_details.description",
                            default=None),
                        "urls": Coalesce((
                            "user_details.entities.url.urls",
                            [{
                                "description_url_expanded": "expanded_url",
                                "description_url_on_twitter": "url"
                            }]
                        ), default=None),
                        "tagged_profiles": Coalesce((
                            "user_details.entities.description."
                            "user_mentions",
                            [{
                                "twitter_user_id": "id_str",
                                "twitter_full_name": "name",
                                "twitter_username": "screen_name"
                            }]
                        ), default=None),
                        "description_hashtags": Coalesce(
                            "user_details.entities.description.hashtags",
                            default=None),
                        "description_symbols": Coalesce(
                            "user_details.entities.description.symbols",
                            default=None),
                    },
                    "tagged_profiles": Coalesce((
                        "entities.user_mentions",
                        [{
                            "twitter_user_id": "id_str",
                            "twitter_full_name": "name",
                            "twitter_username": "screen_name"
                        }]
                    ), default=None)
                },
                default=None),
            "twitter_post_hashtags": Coalesce("entities.hashtags",
                                              default=None),
            "twitter_post_symbols": Coalesce("entities.symbols",
                                             default=None),
            "twitter_post_urls": Coalesce("entities.urls", default=None),
            "twitter_post_view_count": Coalesce("view_count",
                                                default=None),
            "twitter_post_id": Coalesce("rest_id", default=None),
            "twitter_post_text": Coalesce("full_text", default=None),
            "twitter_retweeted_post": Coalesce("retweeted_status_result",
                                               default=None),
            "twitter_quoted_post": Coalesce("quoted_status_result",
                                            default=None)
        },
        default=None)
