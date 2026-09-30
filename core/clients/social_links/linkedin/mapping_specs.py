from glom import Coalesce


class SlinksLiSpecs:

    email_spec = (
        {
            "linkedin_profile": {
                "linkedin_id": Coalesce("linkedin_id", default=None),
                "linkedin_profile_picture": Coalesce("photo", default=None),
                "linkedin_full_name": Coalesce("person", default=None),
                "linkedin_username": Coalesce("linkedin_alias", default=None),
                "linkedin_email_address": Coalesce("email", default=None),
            }
        },
    )

    email_v2_spec = spec = {
        "linkedin_profile": {
            "linkedin_id": Coalesce("id", default=None),
            "linkedin_full_name": Coalesce("displayName", default=None),
            "linkedin_location": Coalesce("location", default=None),
            "linkedin_profile_picture": Coalesce("photoUrl", default=None),
            "linkedin_profile_url": Coalesce("linkedInUrl", default=None),
            "linkedin_educations": Coalesce((
                "schools.educationHistory",
                [
                    {
                        "school_name": Coalesce("schoolName", default=None),
                        "fields_of_study": Coalesce("fieldOfStudy",
                                                    default=None),
                        "start_month_year": Coalesce(
                            "startEndDate.start.year", default=None
                        ),
                        "end_month_year": Coalesce("startEndDate.end.year",
                                                   default=None),
                    }
                ],
            ), default=None),
            "linkedin_positions": Coalesce((
                "positions.positionHistory",
                [
                    {
                        "title": Coalesce("title", default=None),
                        "start_month_year": Coalesce(
                            # "startEndDate. start.month" +
                            "startEndDate.start.year",
                            default=None,
                        ),
                        "end_month_year": Coalesce(
                            # "startEndDate.end.month" +
                            "startEndDate.end.year",
                            default=None,
                        ),
                        "description": Coalesce("description", default=None),
                        "company_name": Coalesce("companyName", default=None),
                    }
                ],
            ), default=None),
        }
    }

    name_spec = {
        "linkedin_profile": {
            "linkedin_f_name": Coalesce("first_name", default=None),
            "linkedin_l_name": Coalesce("last_name", default=None),
            "linkedin_location": Coalesce("location", default=None),
            "linkedin_profile_url": Coalesce("url", default=None),
            "linkedin_profile_picture": Coalesce("photo", default=None),
            "linkedin_educations": Coalesce((
                "education",
                [
                    {
                        "school_name": Coalesce("school_name", default=None),
                        "start_month_year": Coalesce("date_from",
                                                     default=None),
                        "end_month_year": Coalesce("date_to", default=None),
                    }
                ],
            ), default=None),
            "linkedin_positions": Coalesce((
                "experience",
                [
                    {
                        "company_name": Coalesce("company_name", default=None),
                        "title": Coalesce("position", default=None),
                        "start_month_year": Coalesce("date_from",
                                                     default=None),
                        "end_month_year": Coalesce("date_to", default=None),
                    }
                ],
            ), default=None),
        }
    }
