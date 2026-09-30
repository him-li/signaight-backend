from core.flows.complex_search.utils import build_emails_groups
from glom import T, Coalesce, SKIP

from core.clients.grayfox.mapping.utils import (
    build_images,
    build_locations,
    build_phones_groups,
    build_telegram_groups,
    ensure_list,
    ensure_str,
)


details_part_block = {
    "facebook_email_part": (
        Coalesce(
            (
                T["data"]["partial_recovery"],
                [
                    lambda i: (
                        i
                        if isinstance(i, dict)
                        and i.get("source") == "facebook"
                        and i.get("type") == "email"
                        else SKIP
                    )
                ],
                T[0],
                {
                    "personal_details": {
                        "email": {
                            "fb_email_part": Coalesce(
                                (
                                    (
                                        T.get("value"),
                                        lambda x: (
                                            x
                                            if isinstance(x, str)
                                            and x.strip()
                                            or isinstance(x, list)
                                            else None
                                        ),
                                    ),
                                    ensure_list,
                                ),
                                default=None,
                            )
                        }
                    },
                    "source": T["source"],
                },
            ),
            default=None,
        ),
    ),
    "apple_email_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "apple"
                    and i.get("type") == "email"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "email": {
                        "apple_email_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "paypal_email_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "paypal"
                    and i.get("type") == "email"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "email": {
                        "paypal_email_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "microsoft_email_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "microsoft"
                    and i.get("type") == "email"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "email": {
                        "microsoft_email_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "samsung_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "samsung"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "samsung_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "paypal_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "paypal"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "paypal_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "ebay_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "ebay"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "ebay_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "microsoft_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "microsoft"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "microsoft_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "fb_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "facebook"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "fb_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "apple_phone_part": Coalesce(
        (
            T["data"]["partial_recovery"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and i.get("source") == "apple"
                    and i.get("type") == "phone"
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "phone": {
                        "apple_phone_part": Coalesce(
                            (
                                (
                                    T.get("value"),
                                    lambda x: (
                                        x
                                        if isinstance(x, str)
                                        and x.strip()
                                        or isinstance(x, list)
                                        else None
                                    ),
                                ),
                                ensure_list,
                            ),
                            default=None,
                        )
                    }
                },
                "source": T["source"],
            },
        ),
        default=None,
    ),
    "passwords": Coalesce(
        (
            T["data"]["passwords"],
            {"network_signature": {"passwords": T}, "source": T[0]["domain"]},
        ),
        default=None,
    ),
    "leaks": Coalesce(
        (
            T["data"]["leaks"],
            {
                "network_signature": {"misc": {"leaks": T}},
                "source": Coalesce(T["leaks"], default="leaks"),
            },
        ),
        default=None,
    ),
    "locations": Coalesce(
        (
            T["data"]["locations"],
            [
                lambda i: (
                    i if isinstance(i, dict) and i.get("source") == "maps" else SKIP
                )
            ],
            {
                "personal_details": {
                    "location": {
                        "check_ins": {
                            "google_reviews": [
                                {
                                    "address": Coalesce("review.address", default=None),
                                    "comment": Coalesce("review.comment", default=None),
                                    "date": Coalesce("review.date", default=None),
                                    "id": Coalesce("review.id", default=None),
                                    "name": Coalesce("review.name", default=None),
                                    "lat": Coalesce(
                                        "review.position.latitude", default=None
                                    ),
                                    "long": Coalesce(
                                        "review.position.longitude",
                                        default=None,
                                    ),
                                }
                            ]
                        }
                    }
                },
                "source": T[0]["source"],
            },
        ),
        default=None,
    ),
    "socials": Coalesce(
        (
            T["data"]["socials"],
            [
                lambda i: (
                    i
                    if isinstance(i, dict)
                    and (
                        i.get("source") == "facebook_entity"
                        or i.get("source") == "facebook"
                        or i.get("source") == "facebook_phone_user_id_mix"
                    )
                    else SKIP
                )
            ],
            T[0],
            {
                "personal_details": {
                    "name": {
                        "full_name": {
                            "facebook_full_name": Coalesce("name", default=None)
                        }
                    },
                    "email": {"fb_email_address": Coalesce("email", default=None)},
                    "visuals": {
                        "profile_photo": {
                            "facebook_profile_picture": Coalesce("photo", default=None)
                        }
                    },
                },
                "network_signature": {
                    "url": {"facebook_profile_url": Coalesce(
                            ("url", lambda x: [str(x)] if x else None),
                            default=None
                        )},
                    "username": {"facebook_username": Coalesce(
                            ("alias", lambda x: [str(x)] if x else None),
                            default=None
                        )},
                    "user_id": {"facebook_user_id": Coalesce(
                            ("id", lambda x: [str(x)] if x else None),
                            default=None
                        )},
                    "misc": {
                        "facebook_last_active": Coalesce("last_active", default=None),
                        "facebook_creation_date": Coalesce("reg_date", default=None),
                    },
                },
                "source": Coalesce("source", default="facebook"),
            },
        ),
        default=None,
    ),
    "metadata": Coalesce(
        (
            T["data"],
            {
                "personal_details": {
                    "name": {
                        "full_name": {
                            "full_name": Coalesce(
                                (T["metadata"]["fullname"], ensure_str)
                            )
                        }
                    },
                    "email": {
                        "associated_email": Coalesce((T, build_emails_groups), default=None),
                    },
                    "phone": {
                        "grfx_phones": Coalesce((T, build_phones_groups), default=None),
                    },
                    "location": {
                        "grfx_location": Coalesce((T['locations'], build_locations), default=None)
                    },
                    "grfx_images": Coalesce((T, build_images), default=None),
                },
                "source": Coalesce(T['metadata'][0]["domain"], default="metadata"),
            },
        ),
        default=None,
    ),
    "telegram_groups": Coalesce(
        {
            "interests": {
                "groups": {
                    "telegram_groups": Coalesce(
                        (T["data"]["telegram"], build_telegram_groups),
                        default=None,
                    )
                }
            },
            "source": Coalesce(
                T["data"]["telegram"]["source"], default="telegram_groups"
            ),
        }
    ),
    "darknet": Coalesce(
        (
            T["data"]["darknet"],
            [
                {
                    "personal_details": {
                        "name": {
                            "full_name": {"full_name": Coalesce("name", default=None)},
                        },
                    },
                    "network_signature": {
                        "user_id": {
                            "facebook_user_id": Coalesce(
                                (
                                    "profile_facebook",
                                    lambda x: (
                                        x if isinstance(x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                        "url": {
                            "linkedin_profile_url": Coalesce(
                                (
                                    "profile_linkedin",
                                    lambda x: (
                                        x if isinstance(x, str) and x.strip() else None
                                    ),
                                ),
                                default=None,
                            )
                        },
                    },
                    "darknet": {
                        "breach_name": Coalesce("source.breach_name", default=None),
                        "confidence": Coalesce("source.confidence", default=None),
                        "exposed_fields": Coalesce(
                            "source.exposed_fields", default=None
                        ),
                    },
                    "source": Coalesce("source.source", default="darknet"),
                }
            ],
        ),
        default=None,
    ),
    "email": Coalesce(
        (
            T["data"]["emails"],
            T[0],
            {
                "personal_details": {
                    "email": {
                        "email_address": Coalesce(
                            (T.get("email"), ensure_list), default=None
                        )
                    },
                },
                "source": Coalesce(
                    (
                        T["source"],
                        lambda x: (f"{x}_email" if isinstance(x, str) and x.strip() else "email"),
                    ),
                    default="email",
                ),
            },
        ),
        default=None,
    ),
}
