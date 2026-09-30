from glom import Coalesce


class EpieosLiSpecs:

    email_spec = {
                "linkedin_email_address": Coalesce("linkedin.query",
                                                   default=None),
                "linkedin_f_name": Coalesce("linkedin.first_name",
                                            default=None),
                "linkedin_l_name": Coalesce("linkedin.last_name",
                                            default=None),
                "location": {"location": Coalesce("linkedin.location",
                                                  default=None)},
                "visuals": {"profile_photo": {
                    "linkedin_profile_picture": Coalesce("linkedin.photo",
                                                         default=None)}},
                "network_signature": {
                    "url": {
                        "linkedin_profile_url": Coalesce("linkedin.url",
                                                         default=None),
                    }
                },
                "biographic_details": {
                    "education": {
                        "linkedin_schools": Coalesce((
                            "linkedin.schools",
                            [
                                {
                                    "school_name": Coalesce("name",
                                                            default=None),
                                    "education_field": Coalesce("field",
                                                                default=None),
                                    "period": Coalesce(
                                        "period",
                                        default=None,
                                    ),
                                }
                            ],
                        ), default=None),
                    },
                    "work": {
                        "linkedin_work": {
                            "positions": Coalesce((
                                "linkedin.companies",
                                [
                                    {
                                        "company_name": Coalesce("name",
                                                                 default=None),
                                        "title": Coalesce("title",
                                                          default=None),
                                        "period": Coalesce(
                                            "period",
                                            default=None,
                                        ),
                                    }
                                ],
                            ), default=None),
                        }
                    }
                }
            }
