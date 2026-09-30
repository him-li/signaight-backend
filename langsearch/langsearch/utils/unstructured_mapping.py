import pendulum
from glom import Coalesce, T

unsctutured_to_candidate_spec = Coalesce({
    "personal_details": {
        "name": {
            "first_name": {
                "f_name": Coalesce("extracted_personal_details.f_name",
                                   default=None)
            },
            "last_name": {
                "l_name": Coalesce("extracted_personal_details.l_name",
                                   default=None)
            },
            "full_name": {
                "full_name": Coalesce("extracted_personal_details.name",
                                      default=None)
            }
        },
        "email": {
            "email_address": Coalesce(
                ("extracted_personal_details.email_address",
                 lambda x: [x] if x else None), default=None)
        },
        "phone": {
            "phones": Coalesce(("extracted_personal_details.phone_number",
                                lambda x: [x] if x else None),
                               default=None)
        },
        "location": {
            "general": Coalesce(
                (
                    "extracted_personal_details",
                    [
                        {"value": T.city},
                        {"value": T.country},
                    ],
                ),
                default=None,
            )
        },
        "websites": {
            "websites": Coalesce(
                (
                    {
                        "url": "extracted_personal_details.source_url",
                        "images": Coalesce("images", default=[]),
                    },
                    lambda d: [d] if d.get("url") else None,
                ),

                default=None,
            )
        }
    },
    "biographic_details": {
        "description_intro_bio": {
            "general": Coalesce(
                ("extracted_biographic_details.bio",
                 lambda x: [x] if x else None), default=None)
        },
        "work": {
            "general_work": {
                "positions": Coalesce(
                    ("extracted_professional_details",
                     [{
                         "title": "title",
                         "company_name": "company",
                         "location": "city",
                         "company_industry": "industry"
                     }]

                     ),
                    default=None
                ),
                "skills": Coalesce(
                    ("extracted_professional_details.0.skills",
                     [
                         {"name": T}
                     ]),
                    default=None
                )
            }
        },
        "education": {
            "general_schools": Coalesce(
                ("extracted_education_details",
                 [{
                     "school_name": "institution",
                     "degree_name": "degree",
                     "education_field": "field_of_study",
                     "period": {
                         "date_from": Coalesce(
                             ("start_year",
                              lambda x: pendulum.parse(
                                  str(x), strict=False).start_of('year')
                              if x else None), default=None),
                         "date_to": Coalesce(
                             ("end_year",
                              lambda x: pendulum.parse(
                                  str(x), strict=False).start_of('year')
                              if x else None), default=None),
                     }
                 }]
                 ), default=None
            )
        }
    }
}, default=None)
