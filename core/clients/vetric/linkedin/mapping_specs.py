from glom import Coalesce, Call, T, Literal


def parse_linkedin_headline(headline):
    if not isinstance(headline, str):
        return None

    # Drop anything after a pipe
    if "|" in headline:
        headline = headline.split("|")[0].strip()

    sep = None
    if " at " in headline:
        sep = " at "
    elif "@" in headline:
        # tolerate both " @ " and "@"
        sep = "@"

    if not sep or sep not in headline:
        return None

    before, after = headline.split(sep, 1)
    title = before.strip()
    company_name = after.strip()

    if not title or not company_name:
        return None

    return {"title": title, "company_name": company_name}


class VtLISpecs:

    url_resolver_spec = Coalesce("entity_urn", default=None)

    search_spec = Coalesce((
        "people",
        [{
            "personal_details": {
                "name": {
                    "full_name": {
                        "linkedin_full_name": Coalesce("name", default=None)
                    }
                },
                "visuals": {
                    "profile_photo": {
                        "linkedin_profile_picture": Coalesce("image",
                                                             default=None)
                    }
                },
                "location": {
                    "current_city_region_country": {
                        "linkedin_search_location": Coalesce("location",
                                                             default=None)
                    }
                }
            },
            "biographic_details": {
                "description_bio_intro": {
                    "linkedin_headline": Coalesce("position", default=None)
                }
            },
            "network_signature": {
                "url": {
                    "linkedin_profile_url": Coalesce(
                        ("url", lambda x: [x] if x else None), default=None)
                },
                "user_id": {
                    "linkedin_user_id": Coalesce(
                        ("urn", lambda x: [x] if x else None), default=None)
                }
            }
        }]
    ))

    new_search_spec = Coalesce((
        "people",
        [{
            "source": Literal("linkedin"),
            "resource": Literal("vetric"),
            "personal_details": {
                "name": {
                    "full_name": {
                        "linkedin_full_name": Coalesce("name", default=None)
                    }
                },
                "visuals": {
                    "profile_photo": {
                        "linkedin_profile_picture": Coalesce("image",
                                                             default=None)
                    }
                },
                "location": {
                    "current_city_region_country": {
                        "linkedin_search_location": Coalesce("location",
                                                             default=None)
                    }
                }
            },
            "biographic_details": {
                "description_bio_intro": {
                    "linkedin_headline": Coalesce("position", default=None)
                },
                "work": {
                    "linkedin_work": {
                        "positions": Coalesce(
                            Call(lambda h: [parse_linkedin_headline(h)]
                                 if parse_linkedin_headline(h)
                                 else [],
                                 (T["position"],)),
                            default=[],
                        )

                    }
                },
            },
            "network_signature": {
                "url": {
                    "linkedin_profile_url": Coalesce(
                        ("url", lambda x: [x] if x else None), default=None)
                },
                "user_id": {
                    "linkedin_user_id": Coalesce(
                        ("urn", lambda x: [x] if x else None), default=None)
                }
            }
        }]
    ))

    overview_spec = Coalesce(
        {
            "personal_details": {
                "name": {
                    "first_name": {
                        "linkedin_f_name": Coalesce("first_name",
                                                    default=None),
                        "f_name": Coalesce("first_name", default=None)
                    },
                    'last_name': {
                        "linkedin_l_name": Coalesce("last_name", default=None),
                        "l_name": Coalesce("last_name", default=None)
                    }
                },
                "location": {
                    "current_city_region_country": {
                        "linkedin_location": Coalesce(
                            "location.country.name", default=None)
                    },
                    "current_country": {
                        "linkedin_location_country":  Coalesce(
                            "location.country.name", default=None)
                    }
                },
                "visuals": {
                    "profile_photo": {
                        "linkedin_profile_picture": Coalesce("profile_picture",
                                                             default=None)
                    }
                }
            },
            "biographic_details": {
                "description_bio_intro": {
                    "linkedin_headline": Coalesce("headline", default=None)
                },
                "education": {
                    "linkedin_schools": Coalesce({
                        "school_name": "education.name",
                        "school_url": Coalesce("education.url",
                                               default=None)
                    }, default=None)
                },
                "work": {
                    "linkedin_work": {
                        "positions": Coalesce(
                            {
                                "company_name":
                                    "top_position.company_info.name",

                                "title":
                                    "headline",

                                "company_logo_url":
                                    "top_position.company_info.logo",

                                "linkedin_company_url":
                                    "top_position.company_info.url",

                                "period": {
                                    "date_from": {
                                        "year":
                                            "top_position.start_date.year",

                                        "month":
                                            "top_position.start_date.month",

                                    },
                                    "date_to":
                                        {
                                            "year":
                                            "top_position.end_date.year",
                                            "month":
                                            "top_position.end_date.month",

                                    },
                                }
                            }, default=None)
                    }
                }
            },
            "network_signature": {
                "username": {
                    "linkedin_username": Coalesce(
                        ("public_identifier", lambda x: [x] if x else None),
                        default=None),
                },
                "url": {
                    "linkedin_profie_url": Coalesce(
                        ("url", lambda x: [x] if x else None), default=None),
                },
                "online_signature": {
                    "linkedin_connections_count": Coalesce(
                        "connections", default=None),
                    "linkedin_followers_count": Coalesce(
                        "followers", default=None),
                    "linkedin_has_premium": Coalesce("has_premium",
                                                     default=None),
                    "linkedin_is_influencer": Coalesce("is_influencer",
                                                       default=None),
                    "linkedin_is_creator": Coalesce("is_creator",
                                                    default=None),
                    "linkedin_associated_hashtags": Coalesce(
                        "creator_info.associated_hashtag", default=None)
                }
            }
        }, default=None)

    overview_simplified_spec = Coalesce(
        {
            "name": {
                "first_name": {
                    "f_name": Coalesce("first_name", default=None)
                },
                'last_name': {
                    "l_name": Coalesce("last_name", default=None)
                }
            },
            "location": {
                "current_city_region_country": {
                    "linkedin_location": Coalesce(
                        "location.country.name", default=None)
                },
                "current_country": {
                    "linkedin_location_country":  Coalesce(
                        "location.country.name", default=None)
                }
            },
            "visuals": {
                "profile_photo": {
                    "linkedin_profile_picture": Coalesce("profile_picture",
                                                         default=None)
                }
            }
        }, default=None)

    experience_spec = Coalesce((
        "experience",
        {"biographic_details":
            {"work":
                {"linkedin_work":
                    {"positions":
                        [{
                            "company_name": Coalesce(
                                "company.name", default=None),
                            "location": Coalesce(
                                "company.location", default=None),
                            "company_logo_url": Coalesce("company.logo_url",
                                                         default=None),
                            "linkedin_company_url": Coalesce("company.url",
                                                             default=None),
                            "positions": Coalesce((
                                "positions",
                                [{
                                    "title": Coalesce(
                                        "role", default=None),
                                    "employment_type": Coalesce(
                                        "employment_type",
                                        default=None),
                                    "description": Coalesce(
                                        "description", default=None),
                                    "period": {
                                        "date_from": {
                                            "year": Coalesce(
                                                "start_date.year",
                                                default=None),
                                            "month": Coalesce(
                                                "start_date.month",
                                                default=None),
                                        },
                                        "date_to":  {
                                            "year": Coalesce(
                                                "end_date.year",
                                                default=None),
                                            "month": Coalesce(
                                                "end_date.month",
                                                default=None),
                                        },
                                        "duration": {
                                            "years": Coalesce(
                                                "duration.years",
                                                default=None),
                                            "months": Coalesce(
                                                "duration.months",
                                                default=None),
                                        }
                                    }
                                }]), default=None),
                            "skills": Coalesce(("positions",
                                                ["skills"]),
                                               default=None),
                        }]
                     }
                 }
             }
         }), default=None)

    skills_spec = Coalesce((
        "skills",
        {"biographic_details":
            {"work":
                {"linkedin_work":
                    {"skills":
                        [{
                            "name": Coalesce("name", default=None),
                            "endorsers": Coalesce(
                                ("endorsers",
                                 lambda x: x if isinstance(x, list) and
                                 len(x) > 0 and (isinstance(x[0], str) or
                                                 isinstance(x[0], dict)) else
                                 []),
                                default=[]),
                            "endorser_count": Coalesce(
                                "endorser_count",
                                default=0)
                        }]
                     }
                 }
             }
         }
    ), default=None)

    education_spec = Coalesce((
        "education",
        {"biographic_details":
            {"education":
                {"linkedin_schools":
                 [{
                     "school_name": Coalesce("institute.name", default=None),
                     "degree_name": Coalesce("degree_program", default=None),
                     "period": {
                         "date_from": {
                             "year": Coalesce(
                                 "start_date.year",
                                 default=None),
                             "month": Coalesce(
                                 "start_date.month",
                                 default=None),
                         },
                         "date_to":  {
                             "year": Coalesce(
                                 "end_date.year",
                                 default=None),
                             "month": Coalesce(
                                 "end_date.month",
                                 default=None),
                         },
                     },
                     "duration": {
                         "years": Coalesce("duration.years", default=None),
                         "months": Coalesce("duration.months", default=None),
                     },
                     "description": Coalesce("description", default=None),
                     "school_logo_url": Coalesce("institute.logo",
                                                 default=None),
                     "school_url": Coalesce("institute.url", default=None),
                 }]
                 }
             }
         }
    ), default=None)

    recommendations_received_spec = Coalesce((
        "recommendations",
        {"biographic_details":
            {"work":
                {"linkedin_work":
                    {"recommendations":
                        [{
                            "recommender": {
                                "linkedin_full_name": Coalesce(
                                    "name", default=None),
                                "linkedin_headline": Coalesce(
                                    "subtitle", default=None),
                            },
                            "date": Coalesce("date", default=None),
                            "context": Coalesce("context", default=None),
                            "description": Coalesce("description",
                                                    default=None),
                            "url": Coalesce("url", default=None),
                        }]
                     }
                 }
             }
         }
    ), default=None)

    contact_info_spec = Coalesce(
        {
            "personal_details": {
                "name": {
                    "first_name": {
                        "linkedin_f_name": Coalesce("first_name",
                                                    default=None),
                    },
                    "last_name": {
                        "linkedin_l_name": Coalesce("last_name", default=None),
                    }
                },
                "email": {
                    "linkedin_email_address": Coalesce("email", default=None),
                },
                "websites": {
                    "linkedin_websites": Coalesce((
                        "websites",
                        [{
                            "category": Coalesce("category", default=None),
                            "url": Coalesce("url", default=None),
                        }]
                    ), default=None)
                }
            },
            "network_signature": {
                "username": {
                    "linkedin_username": Coalesce(
                        ("public_identifier", lambda x: [x] if x else None),
                        default=None),
                }
            },
        }, default=None)

    courses_spec = Coalesce((
        "courses",
        {"biographic_details":
            {"work":
                {"linkedin_work":
                    {"courses":
                        [{
                            "course_name": Coalesce("name", default=None),
                            "course_code": Coalesce("code", default=None),
                        }]
                     }
                 }
             }
         }
    ), default=None)

    activity_posts_spec = Coalesce((
        "activity",
        {
            "posts":
            [{
                "linkedin_post_text": Coalesce("text", default=None),
                "linkedin_post_publishment_date": Coalesce("created_at",
                                                           default=None),
                "linkedin_post_comments_count": Coalesce("comments",
                                                         default=None),
                "linkedin_post_likes_count": Coalesce("likes", default=None),
                "linkedin_post_shares_count": Coalesce("shares", default=None),
                "linkedin_post_photo": Coalesce("attachments.image",
                                                default=None),
                "linkedin_post_url": Coalesce("url", default=None),
                "reactions": Coalesce((
                    "reactions",
                    [{
                        "linkedin_post_reaction_type": Coalesce(
                            "reaction_type", default=None),
                        "linkedin_post_reaction_type_count": Coalesce(
                            "count", default=None),
                    }]), default=[]),
                "post_author": {
                    "linkedin_f_name": Coalesce("author.first_name",
                                                default=None),
                    "linkedin_l_name": Coalesce("author.last_name",
                                                default=None),
                    "title": Coalesce("author.occupation", default=None),
                    "linkedin_profile_picture": Coalesce("author.image_url",
                                                         default=None),
                    "linkedin_profile_url": Coalesce("author.url",
                                                     default=None),
                },
                "shared_post": Coalesce({
                    "post_author": {
                        "linkedin_f_name": "shared_post.author.first_name",
                        "linkedin_l_name": "shared_post.author.last_name",
                        "title": "shared_post.author.occupation",
                        "linkedin_profile_picture": ["shared_post."
                                                     "author.image_url"],
                        "linkedin_profile_url": "shared_post.author.url",
                    },
                }, default=None),
                "tagged_profiles": Coalesce((
                    "mentions",
                    [{
                        "linkedin_f_name": "first_name",
                        "linkedin_l_name": "last_name",
                        "title": "occupation",
                        "linkedin_profile_picture": "image_url",
                        "linkedin_profile_url": "url",
                    }]
                ), default=[])
            }]
        }
    ), default=None)

    activity_reactions_spec = Coalesce((
        "activity",
        {
            "posts":
            [{
                "linkedin_post_text": Coalesce("text", default=None),
                "linkedin_post_publishment_date": Coalesce("created_at",
                                                           default=None),
                "linkedin_post_comments_count": Coalesce("comments",
                                                         default=None),
                "linkedin_post_likes_count": Coalesce("likes", default=None),
                "linkedin_post_shares_count": Coalesce("shares", default=None),
                "linkedin_post_photo": Coalesce("attachments.image",
                                                default=None),
                "linkedin_post_url": Coalesce("url", default=None),
                "reactions": Coalesce((
                    "reactions",
                    [{
                        "linkedin_post_reaction_type": Coalesce(
                            "reaction_type", default=None),
                        "linkedin_post_reaction_type_count": Coalesce(
                            "count", default=None),
                    }]), default=[]),
                "post_author": {
                    "linkedin_f_name": Coalesce("author.first_name",
                                                default=None),
                    "linkedin_l_name": Coalesce("author.last_name",
                                                default=None),
                    "title": Coalesce("author.occupation", default=None),
                    "linkedin_profile_picture": Coalesce("author.image_url",
                                                         default=None),
                    "linkedin_profile_url": Coalesce("author.url",
                                                     default=None),
                },
                "shared_post": Coalesce({
                    "post_author": {
                        "linkedin_f_name": "shared_post.author.first_name",
                        "linkedin_l_name": "shared_post.author.last_name",
                        "title": "shared_post.author.occupation",
                        "linkedin_profile_picture": ["shared_post."
                                                     "author.image_url"],
                        "linkedin_profile_url": "shared_post.author.url",
                    },
                }, default=None),
                "tagged_profiles": Coalesce((
                    "mentions",
                    [{
                        "linkedin_f_name": "first_name",
                        "linkedin_l_name": "last_name",
                        "title": "occupation",
                        "linkedin_profile_picture": "image_url",
                        "linkedin_profile_url": "url",
                    }]
                ), default=[]),
                "activity_type": Coalesce(
                    ("activity_type",
                     lambda x: x.lower() if isinstance(x, str) else
                     "reaction"),
                    default="reaction"),
                "post_reaction": {
                    "reaction_target": Coalesce("reaction_target",
                                                default='Post'),
                    "reaction_type": Coalesce(
                        ("reaction_text",
                         lambda x: (
                             'EMPATHY' if 'loves' in x.lower() else
                             'EMPATHY' if 'loved' in x.lower() else
                             'LIKE' if 'likes' in x.lower() else
                             'LIKE' if 'liked' in x.lower() else
                             'PRAISE' if 'celebrates' in x.lower() else
                             'PRAISE' if 'celebrated' in x.lower() else
                             'APPRECIATION' if 'supports' in x.lower() else
                             'APPRECIATION' if 'supported' in x.lower() else
                             'INTEREST' if 'insightful' in x.lower() else
                             'ENTERTAINMENT' if 'funny' in x.lower() else
                             'LIKE'
                         )), default='LIKE')
                }
            }]
        }
    ), default=None)

    languages_spec = Coalesce((
        "languages",
        {"personal_details": {
            "languages": {
                "li_languages": [
                    {
                        "language": "language",
                        "proficiency": "proficiency"
                    }
                ]
            }
        }
        }
    ), default=None)

    licences_certifications_spec = Coalesce((
        "licenses_and_certifications",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "licences_certifications": [
                            {
                                "name": Coalesce("title", default=None),
                                "issuer": Coalesce("issuer", default=None),
                                "issue_date": {
                                    "year": Coalesce(
                                        "issue_date.year", default=None),
                                    "month": Coalesce(
                                        "issue_date.month", default=None),
                                    "day": Coalesce(
                                        "issue_date.day", default=None),
                                },
                                "expiration_date": Coalesce(
                                    "expiration_date", default=None),
                                "issuer_photo": Coalesce(
                                    "image_url", default=None),
                                "issuer_url": Coalesce("url", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    volunteering_spec = Coalesce((
        "volunteering_experience",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "volunteering_experiences": [
                            {
                                "role": Coalesce("role", default=None),
                                "company_name": Coalesce(
                                    "organization", default=None),
                                "is_current": Coalesce(
                                    "is_current_position", default=None),
                                "start_month_year": Coalesce(
                                    "start_date", default=None),
                                "end_month_year": Coalesce(
                                    "end_date", default=None),
                                "duration": {
                                    "years": Coalesce(
                                        "duration.years", default=None),
                                    "months": Coalesce(
                                        "duration.months", default=None),

                                },
                                "description": Coalesce(
                                    "description", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    honors_awards_spec = Coalesce((
        "honors_and_awards",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "honors": [
                            {
                                "description": Coalesce(
                                    "description", default=None),
                                "issue_date": Coalesce(
                                    "issued_date", default=None),
                                "issuer": Coalesce(
                                    "issued_by", default=None),
                                "title": Coalesce("title", default=None),
                                "associated_with": Coalesce(
                                    "association", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    publications_spec = Coalesce((
        "publications",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "publications": [
                            {
                                "description": Coalesce(
                                    "summary", default=None),
                                "name": Coalesce(
                                    "title", default=None),
                                "publisher": Coalesce(
                                    "source", default=None),
                                "url": Coalesce(
                                    "url", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    projects_spec = Coalesce((
        "projects",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "projects": [
                            {
                                "title": Coalesce("title", default=None),
                                "start_month_year": Coalesce(
                                    "date", default=None),
                                "end_month_year": Coalesce(
                                    "date", default=None),
                                "description": Coalesce(
                                    "description", default=None),
                                "contributors": Coalesce(
                                    "contributors", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    interests_influencers_spec = Coalesce((
        "interests",
        {
            "interests": {
                "linkedin_interests": [{
                    "linkedin_full_name": Coalesce("name", default=None),
                    "linkedin_headline": Coalesce("subtitle", default=None),
                    "linkedin_followers_count": Coalesce("followers",
                                                         default=None),
                    "linkedin_profile_url": Coalesce("url", default=None),
                    "linkedin_profile_picture": Coalesce("image",
                                                         default=None),
                    "linkedin_is_influencer": Coalesce("type", default=None),
                }]
            }
        }
    ), default=None)

    test_scores_spec = Coalesce((
        "test_scores",
        {
            "biographic_details": {
                "work": {
                    "linkedin_work": {
                        "test_scores": [
                            {
                                "test_name": Coalesce("title", default=None),
                                "score": Coalesce("subtitle", default=None),
                                "date": Coalesce("subtitle", default=None),
                            }
                        ]
                    }
                }
            }
        }
    ), default=None)

    events_spec = Coalesce((
        "events",
        {}
    ), default=None)

    about_spec = Coalesce("", default=None)

    organizations_spec = Coalesce("", default=None)

    companies_search_spec = Coalesce((
        "companies",
        [{
            "linkedin_urn": Coalesce("urn", default=None),
            "name": Coalesce("name", default=None),
            "industry": Coalesce("specializes_in", default=None),
            "description": Coalesce("description", default=None),
            "location": {
                "city": Coalesce("headquarters", default=None),
            },
            "followers": Coalesce("followers", default=None),
            "logo_url": Coalesce("company_logo", default=None),
            "parent_company": Coalesce({
                "name": "page_by.name",
                "url": "page_byurl",
                "urn": "page_by.urn",
            }, default=None),
            "public_identifier": Coalesce("public_identifier", default=None),
            "linkedin_url": Coalesce("url", default=None),
            "website_url": Coalesce("website_url", default=None),
            "crunchbase_url": Coalesce("crunchbase_url", default=None)
        }]),
        default=None)

    company_details_spec = Coalesce(
        {
            "name": Coalesce("name", default=None),
            "public_identifier": "public_identifier",
            "linkedin_urn": "urn",
            "linkedin_url": "url",
            "industry": "industry.0.name",
            "headline": "headline",
            "description": "description",
            "employee_count": "employee_count",
            "employee_count_range": "employee_count_range",
            "followers_count": "followers_count",
            "founded_on": "founded_on",
            "phone": "phone",
            "specialities": "specialities",
            "locations": Coalesce((
                "locations",
                [{
                    "country": "address.country",
                    "geographic_area": "address.geographic_area",
                    "city": "address.city",
                    "postal_code": "address.postal_code",
                    "headquarter": "headquarter"
                }]
            ),
                default=None),
            "universal_name": Coalesce("universal_name", default=None),
            "logo_url": Coalesce("logo", default=None),
            "website_url": Coalesce("website_url", default=None),
            "organization_type": "organization_type",
            "crunchbase_url": Coalesce("crunchbase_url", default=None),
        },
        default=None)
