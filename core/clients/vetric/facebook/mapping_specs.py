from glom import Coalesce, SKIP, T, Literal

from .utils import (
    extract_school_name,
    extract_studied_field,
    parse_education_period,
    extract_workplace_name,
    extract_job_position,
    parse_work_period,
    map_places_list_to_normalized,
    parse_marital_status,
    parse_languages,
    parse_gender,
    parse_birthday,
    parse_contact_info
)


class VtrcFbSpecs:

    search_edges_spec = Coalesce((
        "results",
        [
            {
                # Facebook ID
                "id": Coalesce("id", default=None),
                # Name of dsearched candidate
                "name": Coalesce("name", default=None),
                # Profile picture
                "profile_picture": Coalesce("photoUrl", default=None),
                # Info of work, education and location
                "description": Coalesce("info", default=None),
                # Number of followers
                "followers": Coalesce("followers", default=None),
            }
        ],
    ), default=None)

    new_search_spec = Coalesce((
        "results",
        [
            {
                "source": Literal("facebook"),
                "resource": Literal("vetric"),
                "personal_details": {
                    "name": {
                        "full_name": {
                            "facebook_full_name": Coalesce("name",
                                                           default=None),
                        }
                    },
                    "visuals": {
                        "profile_photo": {
                            "profile_picture": Coalesce("photoUrl",
                                                        default=None),
                            "facebook_profile_picture": Coalesce(
                                "photoUrl", default=None),
                        }
                    },
                },
                "network_signature": {
                    "user_id": {
                        "facebook_user_id": Coalesce(
                            ("id", lambda x: [x] if x else None),
                            default=None)
                    },
                    "url": {
                        "facebook_profile_url": Coalesce(
                            (
                                "id",
                                lambda x: [
                                    f"https://www.facebook.com/profile.php?id={x}"] if x else None
                            ),
                            default=None
                        )
                    },
                    "online_signature": {
                        "fb_followers_count": Coalesce((
                            "followers",
                            lambda x: int(x.replace(',', '')) if isinstance(
                                x, str) and x.replace(',', '').isdigit() else
                            None
                        ),
                            default=None)
                    }
                },
                "biographic_details": {
                    "description_bio_intro": {
                        "introduction": Coalesce("info", default=None)
                    }
                }
            }
        ],
    ), default=None)

    # very early implementation
    timeline_specs = Coalesce(
        {
            "profile_picture": Coalesce(
                "profile.profile_picture_url",  default=None),
            "profile_id": Coalesce(
                ("profile.profile_id",lambda x: [x] if x else None),  default=None),
            "fb_profile_intro": {
                "fb_profile_intro_id": Coalesce(
                    "content.profile_stories_id", default=None),
                "fb_profile_intro_text": Coalesce(
                    ("content.profile_status_text"), default=None),
            },
            "facebook_cover_photo": Coalesce(
                "profile.cover_photo_url", default=None),
            "facebook_full_name": Coalesce(
                "profile.full_name", default=None),
            "facebook_username": Coalesce(
                ("profile.username", lambda x: [x] if x else None),
                default=None),
            "facebook_profile_url": Coalesce(
                ("profile.profile_url", lambda x: [x] if x else None),
                default=None),
            "facebook_gender": Coalesce(
                "profile.gender", default=None),
            "friends": Coalesce(
                "engagement.friends", default=None),
            "followers": Coalesce(
                "engagement.followers", default=None),
            "following": Coalesce(
                "engagement.following", default=None),
        },
        default=None)

    new_timeline_spec = Coalesce(
        {
            "personal_details": {
                "name": {
                    "full_name": {
                        "facebook_full_name": Coalesce(
                            "profile.full_name", default=None
                        )
                    },
                },
                "gender": {"fb_gender": Coalesce("profile.gender", default=None)},
                "visuals": {
                    "profile_photo": {
                        "facebook_profile_picture": Coalesce(
                            "profile.profile_picture_url", default=None
                        )
                    },
                    "fb_cover_photo": Coalesce("profile.cover_photo_url", default=None),
                },
            },
            "network_signature": {
                "user_id": {
                    "facebook_user_id": Coalesce(
                        ("profile.profile_id", lambda x: [x] if x else None),
                        default=None,
                    )
                },
                "username": {
                    "facebook_username": Coalesce(
                        ("profile.username", lambda x: [x] if x else None), default=None
                    )
                },
                "url": {
                    "facebook_url": Coalesce(
                        ("profile.profile_url", lambda x: [x] if x else None),
                        default=None,
                    )
                },
                "online_signature": {
                    "fb_followers_count": Coalesce(
                        "engagement.followers", default=None
                    ),
                    "fb_following_count": Coalesce(
                        "engagement.following", default=None
                    ),
                    "fb_friends_count": Coalesce("engagement.friends", default=None),
                },
            },
            "biographic_details": {
                "description_intro_bio": {
                    "fb_profile_intro": {
                        "fb_profile_intro_id": Coalesce(
                            "content.profile_stories_id", default=None
                        ),
                        "fb_profile_intro_text": Coalesce(
                            "content.profile_status_text", default=None
                        ),
                    }
                }
            },
        },
        default=None,
    )

    about_spec = {
        "facebook_work": Coalesce(
            (
                T["data"]["user"]["profile_field_sections"]["edges"],
                [lambda i: i if i["node"][
                    "field_section_type"] == "work" else SKIP],
                (T[0]["node"]["profile_fields"]["edges"]),

                [
                    {
                        "fb_workplace_id": Coalesce(
                            "fieldInfo.entity_id",
                            default=None),
                        "descriptive_text": Coalesce(
                            "fieldInfo.title.text",
                            default=None),
                        "fb_workplace_location":
                        Coalesce(("fieldInfo.list_item_groups."
                                 "0.list_items.1.text.text"),
                                 default=None),
                        "period":
                        Coalesce(("fieldInfo.list_item_groups."
                                 "0.list_items.0.text.text"),
                                 default=None),
                    }
                ],
            ),
            default=None,
        ),
        "facebook_education": Coalesce(
            (
                T["data"]["user"]["profile_field_sections"]["edges"],
                [lambda i: i if i["node"][
                    "field_section_type"] == "education" else SKIP],
                (T[0]["node"]["profile_fields"]["edges"]),
                [
                    {
                        "fb_school_id": Coalesce("fieldInfo.entity_id",
                                                 default=None),
                        "period": Coalesce("fieldInfo.list_item_groups.0."
                                           "list_items.0.text.text",
                                           default=None),
                        "descriptive_text": Coalesce(
                            "fieldInfo.title.text",
                            default=None),
                    }
                ],
            ),
            default=None,
        ),
        "facebook_locations": {
            "facebook_location": Coalesce(
                (
                    T["data"]["user"]["profile_field_sections"]["edges"],
                    [lambda i: i if i["node"][
                        "field_section_type"] == "places_lived" else SKIP],
                    (T[0]["node"]["profile_fields"]["edges"]),
                    [
                        {
                            "city":
                            Coalesce("fieldInfo.title.text",
                                     default=None),
                            "type":
                            Coalesce(("fieldInfo.field_type"),
                                     default=None)
                        }
                    ],
                ),
                default=None,
            ),
        },
        "fb_phone": Coalesce(
            (T["data"]["user"]["profile_field_sections"]["edges"],
                [lambda i: i if i["node"]["field_section_type"]
                 == "contact_info" else SKIP],
                T[0]["node"]["profile_fields"]["edges"],
                [lambda i: i if "Phone" in i["fieldInfo"]["list_item_groups"]
                 [0]["list_items"][0]["text"]["text"] else SKIP],
             ),
            default=None),
        "facebook_basic_info": Coalesce(
            (T["data"]["user"]["profile_field_sections"]["edges"],
             [lambda i: i if i["node"][
                 "field_section_type"] == "basic_info" else SKIP],
             T[0]["node"]["profile_fields"]["edges"],
                [
                    {
                        "info_type": Coalesce(
                            "fieldInfo.field_type",
                            default=None),
                        "info_data": Coalesce(
                            "fieldInfo.title.text",
                            default=None)
                    }
            ],
            ),
            default=None
        ),
        "fb_nicknames": Coalesce(
            (T["data"]["user"]["profile_field_sections"]["edges"],
                [lambda i: i if i["node"]["field_section_type"]
                    == "contact_info" else SKIP],
                T[0]["node"]["profile_fields"]["edges"],
                [lambda i: i if "Nicknames" in i["fieldInfo"]
                 ["list_item_groups"][0]["list_items"][0]["text"]
                 ["text"] else SKIP],
             ),
            default=None),
        "facebook_relationships": {
            "marital_status": Coalesce(
                (
                    T["data"]["user"]["profile_field_sections"]["edges"],
                    [lambda i: i if i["node"][
                        "field_section_type"] == "relationship" else SKIP],
                    T[0]["node"]["profile_fields"]["edges"][0]["fieldInfo"][
                        "list_item_groups"][0]['list_items'][0]['text']['text']
                ),
                default=None,
            )},
        "facebook_family_members":  Coalesce(
            (T["data"]["user"]["profile_field_sections"]["edges"],
             [lambda i: i if i["node"][
                 "field_section_type"] == "family" else SKIP],
             (T[0]["node"]["profile_fields"]["edges"]),
                [
                    {
                        "fb_family_member_type": Coalesce(
                            "fieldInfo.list_item_groups.0.list_items."
                            "0.text.text",
                            default=None),
                        "fb_family_member_name": Coalesce(
                            ("fieldInfo.title.text"),
                            default=None),
                        "fb_user_id": Coalesce(
                            ("fieldInfo.entity_id"), default=None)
                    }
            ],
            ),
            default=[]),
        "facebook_checkins": Coalesce(
            (
                ("data.user.timeline_about_app_sections.edges.0.node."
                 "collections.edges.0.node.items.edges"),
                [
                    {
                        "id": Coalesce("appInfo.id", default=None),
                        "title": Coalesce("appInfo.title.text", default=None),
                        "subtitle": Coalesce(
                            "appInfo.subtitle_text.text",
                            default=None),
                        "url": Coalesce("appInfo.url", default=None),
                        "event_image": Coalesce("appInfo.event_image.uri",
                                                default=None)
                    }
                ],
            ),
            default=None,
        ),
        "facebook_followers": Coalesce(
            (
                ("data.user.timeline_about_app_sections.edges.1.node."
                 "collections.edges.0.node.items.edges"),
                [
                    {
                        "name": Coalesce("appInfo.title.text",
                                         default=None),
                        "subtitle": Coalesce(
                            "appInfo.subtitle_text.text",
                            default=None),
                        "url": Coalesce("appInfo.url", default=None),
                        "facebok_user_id": Coalesce("appInfo.node.id",
                                                    default=None),
                        "facebook_profile_picture": Coalesce(
                            "appInfo.image.uri",
                            default=None)
                    }
                ],
            ),
            default=None,
        ),
        "fb_contact_info": {
            "linkedin": Coalesce(
                (
                    T["data"]["user"]["profile_field_sections"]["edges"],
                    [lambda i: i if i["node"]["field_section_type"]
                        == "contact_info" else SKIP],
                    T[0]["node"]["profile_fields"]["edges"],
                    [lambda i: i if "LinkedIn" in i["fieldInfo"]
                        ["list_item_groups"][0]["list_items"][0]
                        ["text"]["text"] else SKIP],
                    {
                        "fb_linkedin_url": Coalesce(
                            T[0]["fieldInfo"]["link_url"], default=None),
                        "fb_linkedin_username": Coalesce(
                            T[0]["fieldInfo"]["title"]["text"], default=None),
                    }
                ),
                default=None
            ),
            "instagram": Coalesce(
                (
                    T["data"]["user"]["profile_field_sections"]["edges"],
                    [lambda i: i if i["node"]["field_section_type"]
                        == "contact_info" else SKIP],
                    T[0]["node"]["profile_fields"]["edges"],
                    [lambda i: i if "Instagram" in i["fieldInfo"]
                        ["list_item_groups"][0]["list_items"][0]
                        ["text"]["text"] else SKIP],
                    {
                        "fb_instagram_url": Coalesce(
                            T[0]["fieldInfo"]["link_url"], default=None),
                        "fb_instagram_username": Coalesce(
                            T[0]["fieldInfo"]["title"]["text"], default=None),
                    }
                ),
                default=None
            ),
        },
    }

    about_spec_transform = Coalesce({
        "facebook_work": Coalesce((
            ("results.work"),
            [{
                "fb_workplace_id": Coalesce("entity_id", default=None),
                "fb_workplace_name": Coalesce(
                    ("title", extract_workplace_name), default=None),
                "fb_work_title": Coalesce(
                    ("title", extract_job_position), default=None),

                # keep for backward compatibility
                "descriptive_text": Coalesce("title", default=None),
                "fb_workplace_photo_url": Coalesce("image", default=None),
                "period": Coalesce(("subtitles",
                                    (lambda subs: next(
                                        (s for s in subs if "-" in s), None), parse_work_period)
                                    ), default=None),
                "fb_workplace_location": Coalesce(
                    ("subtitles",
                     lambda subs: next(
                         (s for s in subs if "," in s and "-" not in s), None)
                     ),
                    default=None)
            }]),
            default=None),
        "facebook_education": Coalesce((
            ("results.education"),
            [
                {
                    "fb_school_id": Coalesce("entity_id", default=None),
                    "fb_school_name": Coalesce(
                        ("title", extract_school_name), default=None),
                    "fb_school_photo": Coalesce("image", default=None),
                    "fb_school_url": Coalesce("url", default=None),
                    "period": Coalesce(
                        ("subtitles.0", parse_education_period), default=None),
                    "fb_education_field": Coalesce(
                        ("title", extract_studied_field), default=None),
                    # keep for backward compatibility
                    "descriptive_text": Coalesce("title", default=None),
                }
            ]), default=None),
        "facebook_location":  Coalesce((
            ("results.places_lived", map_places_list_to_normalized),
        ), default=None),
        "facebook_relationships": Coalesce(
            ("results.relationship.0", parse_marital_status), default=None
        ),
        "facebook_family_members": Coalesce((
            ("results.family"),
            [
                {
                    "fb_family_member_type": Coalesce("subtitles.0",
                                                      default=None),
                    "fb_family_member_name": Coalesce("title", default=None),
                    "fb_user_id": Coalesce("entity_id", default=None),
                    "fb_profile_picture": Coalesce("image", default=None),
                }
            ],
        ), default=None),
        "facebook_checkins": Coalesce((
            ("results.check_ins"),
            [
                {
                    "title": Coalesce("title", default=None),
                    "subtitle": Coalesce("subtitle", default=None),
                    "url": Coalesce("url", default=None),
                    "event_image": Coalesce("eventImage", default=None),
                }
            ],
        ), default=None),
        "facebook_followers": Coalesce((
            ("results.followers"),
            [
                {
                    "name": Coalesce("title", default=None),
                    "subtitle": Coalesce("subtitle", default=None),
                    "url": Coalesce("url", default=None),
                    "facebok_user_id": Coalesce("url", default=None),
                    "facebook_profile_picture": Coalesce("image",
                                                         default=None),
                }
            ],
        ), default=None),
        "facebook_languages": Coalesce((
            ("results.basic_info"), parse_languages), default=None),
        "facebook_gender": Coalesce((
            ("results.basic_info"), parse_gender), default=None),
        "facebook_birthday": Coalesce((
            ("results.basic_info"), parse_birthday), default=None),
        "facebook_basic_info": Coalesce((
            ("results.basic_info"),
            [
                {
                    "info_type": Coalesce(
                        ("field_type",
                         lambda x: x.lower() if isinstance(x, str) else None),
                        default=None),
                    "info_data": Coalesce(
                        "title",
                        default=None)
                }
            ]),
            default=None),  # keep for backward compatibility
        "fb_nicknames": Coalesce(
            ("results.nicknames", ["title"]),
            default=None),
        "facebook_contact_info": Coalesce((
            ("results.contact_info"), parse_contact_info),
            default=None),

    }, default=None)

    feed_spec = Coalesce((
        ("data.profile.timeline_feed_units.edges"),
        [
            {
                "fb_post_text": Coalesce("node.message.text",
                                         default=None),
                "post_author": Coalesce((
                    ("node.actors"),
                    [
                        {
                            "fb_full_name": Coalesce(
                                "name", default=None),
                            "fb_user_id": Coalesce(
                                "id", default=None),
                            "fb_gender": Coalesce(
                                "gender", default=None),
                            "fb_profile_url": Coalesce(
                                "url", default=None),
                        }
                    ]
                ), default=None),
                "fb_post_language": Coalesce(
                    "node.translatability_for_viewer.source_dialect_name",
                    default=None),
                "fb_post_translated_to": Coalesce(
                    "node.translatability_for_viewer.target_dialect_name",
                    default=None),
                "post_translation": Coalesce(
                    "node.translatability_for_viewer.translation."
                    "message.text",
                    default=None),
                "fb_post_external_webpages": Coalesce((
                    ("node.message.ranges"),
                    [
                        {
                            "name": Coalesce("name", default=None),
                            "url": Coalesce("url", default=None),
                        }
                    ]
                ), default=None),
                "fb_post_photo": {
                    "fb_photo": {
                        "url": Coalesce(
                            "node.attachments.0.media.image.uri",
                            default=None),
                        "width": Coalesce(
                            "node.attachments.0.media.image.width",
                            default=None),
                        "height": Coalesce(
                            "node.attachments.0.media.image.height",
                            default=None),
                    },
                    "fb_photo_id": Coalesce(
                        "node.attachments.0.media.id", default=None),
                },

                "fb_post_comments_count": Coalesce(
                    "node.feedback.top_level_comments.total_count",
                    default=None),
                "fb_post_likers_count": Coalesce(
                    "node.feedback.likers.count", default=None),
                "fb_post_shares_count": Coalesce(
                    "node.feedback.reshares.count", default=None),
                "fb_post_reactors_count": Coalesce(
                    "node.feedback.reactors.count", default=None),
            }
        ]), default=[]),

    new_feed_spec = Coalesce((
        ("results.feed"),
        [
            {
                "fb_post_id": Coalesce("post_id", default=None),
                "fb_post_text": Coalesce("message", "attachments.0.title", "attached_story.message.text",
                                         default=None),
                "fb_post_publish_at_date": Coalesce("creation_time", default=None),
                "fb_post_url": Coalesce("url", default=None),
                "post_author": Coalesce((
                    ("actors"),
                    [
                        {
                            "fb_full_name": Coalesce(
                                "name", default=None),
                            "fb_user_id": Coalesce(
                                "id", default=None),
                            "fb_gender": Coalesce(
                                "gender", default=None),
                            "fb_profile_url": Coalesce(
                                "url", default=None),
                        }
                    ]
                ), default=None),
                "fb_post_language": Coalesce(
                    "source_language",
                    default=None),
                "fb_post_photo": {
                    "fb_photo": {
                        "url": Coalesce(
                            "attachments.0.preview_image",  "attached_story.attachments.0.preview_image",
                            default=None),
                    },
                    "fb_photo_id": Coalesce(
                        "attachments.0.id", default=None),
                },

                "fb_post_comments_count": Coalesce(
                    "feedback.comment_count",
                    default=None),
                "fb_post_likers_count": Coalesce(
                    "feedback.like_count", default=None),
                "fb_post_shares_count": Coalesce(
                    "feedback.share_count", default=None),
                "fb_post_reactors_count": Coalesce(
                    "feedback.reaction_count", default=None),
            }
        ]), default=[]),

    checkins_spec = Coalesce((
        "profile_checkins.checkins",
        [
            {
                "id": Coalesce("location_id", default=None),
                "title": Coalesce("location_name", default=None),
                "region": Coalesce(
                    "location_details",
                    default=None),
                "url": Coalesce("location_url", default=None),
                "event_image": Coalesce("image_url",
                                        default=None),
                "date": Coalesce("visit_date",
                                 default=None),
            }
        ]
    ), default=None)

    uploaded_media_spec = Coalesce((
        "uploaded_media",
        [
            {
                "fb_uploaded_photo":
                {
                    "fb_photo_id": Coalesce("photo_id", default=None),
                    "fb_photo": Coalesce(
                        {
                            "url": "image_url",
                        }, default=None
                    ),
                    "fb_photo_likes_count": Coalesce("likes_count",
                                                     default=None),
                    "fb_photo_reactions_count": Coalesce(
                        "reactions_count",
                        default=None),
                    "fb_photo_reactions_count": Coalesce(
                        "comments_count",
                        default=None),
                }
            }
        ]
    ), default=None)

    header_spec = {
        'name': Coalesce(
            'data.user.profile_header_renderer.user.name', default=''),
        'username': Coalesce(
            'data.user.profile_header_renderer.user.username_for_profile',
            default=None),
        'url': Coalesce(
            'data.user.profile_header_renderer.user.url', default=''),
        'is_verified': Coalesce(
            'data.user.profile_header_renderer.user.is_verified',
            default=False),
        'followers': Coalesce(
            'data.user.profile_header_renderer.user.'
            'profile_social_context.content.0.text.text', default=''),
        'following': Coalesce(
            'data.user.profile_header_renderer.user.'
            'profile_social_context.content.1.text.text', default=''),
        'profile_picture': Coalesce(
            'data.user.profile_header_renderer.user.profilePicMedium.uri',
            default=''),
        'cover_photo': Coalesce(
            'data.user.profile_header_renderer.user.cover_photo.photo.'
            'image.uri', default=''),
        'gender': Coalesce('data.user.profile_header_renderer.user.gender',
                           default=''),
        'is_memorialized': Coalesce(
            'data.user.profile_header_renderer.user.profile_tabs.'
            'profile_user.is_memorialized', default=False),
    }

    media_spec = {
        'photo_id': Coalesce('data.nodes.0.id', default=None),
        'image': Coalesce('data.nodes.0.image.uri', default=None),
        'created_time': Coalesce('data.nodes.0.created_time', default=None),
        'owner': {
            'id': Coalesce('data.nodes.0.owner.id', default=None),
            'name': Coalesce('data.nodes.0.owner.name', default=None),
        },
        'privacy': Coalesce('data.nodes.0.privacy_scope.label', default=None),
        'likes_count': Coalesce('data.nodes.0.feedback.likers.count',
                                default=0),
        'comments_count': Coalesce(
            'data.nodes.0.feedback.top_level_comments.count', default=0),
        'reactions_count': Coalesce('data.nodes.0.feedback.reactors.count',
                                    default=0),
        'top_reactions': Coalesce('data.nodes.0.feedback.top_reactions.edges',
                                  default=[]),
        'url': Coalesce('data.nodes.0.url', default=None),
    }

    url_resolver_spec = Coalesce(("data.urlResolver", {
        "type": Coalesce("__typename", default=None),
        "id": Coalesce("id", default=None),
    }), default=None)

    friends_spec = Coalesce((
        "results",
        [
            {
                "facebook_user_id": Coalesce("id", default=None),
                "facebook_full_name": Coalesce("name", default=None),
                "facebook_profile_picture": Coalesce("profile_picture",
                                                     default=None),
                "facebook_profile_url": Coalesce("url", default=None)
            }
        ]
    ), default=None)

    about_tabs_places_lived_spec = Coalesce(
        ("data.about_collection.style_renderer.profile_field_sections.0"
         ".profile_fields.nodes",
         [{
             "field_type": "field_type",
             "fb_moved_to": Coalesce("title.text", default=None),
             "fb_moved_at":  Coalesce(
                 ("list_item_groups.0.list_items.0.text.text",
                  lambda s: s.split()[-1]), default=None)
         }],
         [lambda i: i if i["field_type"]
          == "moved_city" else SKIP],
         ), default=None)

    liked_pages_spec = Coalesce((
        "profile_likes",
        [
            {
                "fb_page_name": Coalesce("page_name", default=None),
                "fb_page_profile_photo": Coalesce("profile_image_url",
                                                  default=None),
                "fb_page_url": Coalesce("page_url", default=None),
                "fb_page_id": Coalesce("page_id", default=None),
            }
        ]
    ), default=None)

    following_spec = Coalesce((
        "results",
        [
            {
                "facebook_user_id": Coalesce("id", default=None),
                "facebook_full_name": Coalesce("name", default=None),
                "facebook_profile_picture": Coalesce(
                    "profilePicture", default=None),
                "facebook_profile_url": Coalesce("url", default=None),
            }
        ]
    ), default=None)
