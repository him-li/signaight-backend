import os
import asyncio
from glom import glom, Coalesce, T
import pendulum

from core.models.person import Person
from core.models.extracted import (
    ExtractedPerson,
    ExtractedPersonalDetails,
    ExtractedProfessionalDetails,
    ExtractedBiographicDetails,
    ExtractedEducationDetails
)


async def get_candidate_out_of_extracted_content(
    extracted_person: ExtractedPerson,
) -> Person:
    extracted_dict = extracted_person.model_dump()
    print("Extracted dict:", extracted_dict)
    mapped = glom(extracted_dict, spec, default={})

    print("Mapped person:", mapped)

    return Person(**mapped)


spec = Coalesce({
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

test_person = ExtractedPerson(
    extracted_personal_details=ExtractedPersonalDetails(
        source_url="https://iranadfair.com/ad/%D9%81%D8%B1%D9%88%D8%B2%D8%A7%D9%86-%D9%81%D8%A7%D9%85-%D9%81%D8%AC%D8%B1/",
        f_name="محمد حسن",
        l_name="پور آقا",
        name="محمد حسن پور آقا",
        email_address="fruzanfaam@gmail.com",
        phone_number="04191010111",
        city="تبریز",
        country="Iran",
    ),
    extracted_professional_details=[
        ExtractedProfessionalDetails(
            title="مدیریت",
            company="شرکت فروزان فام فجر",
            city="تبریز",
            industry="صنایع کشاورزی و مواد غدایی",
            skills=["بازرگانی", "واردات", "ماشین آلات تولید مواد غذایی"],
        )
    ],
    extracted_education_details=[
        ExtractedEducationDetails(
            institution="Harvard University",
            degree="Bachelor of Science in Computer Science",
            field_of_study="Computer Science",
            start_year=2010,
            end_year=2014
        )
    ],
    # extracted_education_details=None,
    extracted_biographic_details=ExtractedBiographicDetails(
        bio="شرکت فروزان فام فجر در سال 1390 فعالیت خود را با مدیریت آقای دکتر محمد حسن پورآقا در بخش بازرگانی با واردات انواع دستگاه آلات مواد غذایی از کشور چین، تایوان و ترکیه آغاز نمود.",
        marital_status=None,
        relatives=None,
    ),
    # extracted_network_details=None,
)


async def run_test():
    result = await get_candidate_out_of_extracted_content(test_person)
    print(result)

if __name__ == "__main__":
    asyncio.run(run_test(), debug=True)
