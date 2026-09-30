import copy
from beanie import Link
from pydantic import BaseModel, Field
from typing import Self, Optional, List
from pymongo import IndexModel, ASCENDING
from datetime import datetime
from dotty_dictionary import dotty

from core.models import Document, CreateUpdateMixin
from langsearch.models.search_input import SearchInput


class PersonAttributeSchema(BaseModel):
    source: Optional[str] = Field(
        description="Source of the first name",
        default=None
    )


class ValueRanking(BaseModel):
    doctype: str = "ValueRanking"
    value: Optional[str | int | float | bool] = Field(description="Value of the value", default=None)
    ranking: Optional[int] = Field(description="Ranking of the value", default=-1)
    probability: Optional[float] = Field(description="Probability of the value", default=0.0)
    count: Optional[int] = Field(description="Count of the value", default=0)
    default: Optional[bool] = Field(description="Default value of the value, if value if true it means we 100 percent sure about the value", default=False)


class FirstNameSchema(BaseModel):
    doctype: str = "FirstName"
    f_name: Optional[List[ValueRanking]] = Field(description="First name of the person", default=[])


class LastNameSchema(BaseModel):
    doctype: str = "LastName"
    l_name: Optional[List[ValueRanking]] = Field(description="Last name of the person", default=[])


class FullNameSchema(BaseModel):
    doctype: str = "FullName"
    full_name: Optional[List[ValueRanking]] = Field(description="Full name of the person", default=[])


class PhoneNumberSchema(BaseModel):
    doctype: str = "PhoneNumber"
    phone_number: Optional[List[ValueRanking]] = Field(description="Phone number of the person", default=[])


class EmailAddressSchema(BaseModel):
    doctype: str = "EmailAddress"
    email_address: Optional[List[ValueRanking]] = Field(description="Email address of the person", default=[])


class ImageSchema(BaseModel):
    doctype: str = "Image"
    image: Optional[List[ValueRanking]] = Field(description="Images of the person", default=[])


class LocationModel(BaseModel):
    city: Optional[str] = Field(description="City of the location", default=None)
    country: Optional[str] = Field(description="Country of the location", default=None)
    state: Optional[str] = Field(description="State of the location", default=None)
    zip: Optional[str] = Field(description="Zip code of the location", default=None)
    additional_info: Optional[str] = Field(description="Additional information of the location", default=None)

class LocationSchema(PersonAttributeSchema):
    doctype: str = "Location"
    match_option: str = Field(description="Match type: confirmed_match, likely_match, unclear, not_match", default=None)
    value: Optional[LocationModel] = Field(description="Locations of the person", default=None)


class WorkExperienceModel(BaseModel):
    title: Optional[str] = Field(description="Title of the work experience", default=None)
    company: Optional[str] = Field(description="Company of the work experience", default=None)
    start_date: Optional[datetime] = Field(description="Start date of the work experience", default=None)
    end_date: Optional[datetime] = Field(description="End date of the work experience", default=None)
    additional_info: Optional[str] = Field(description="Additional information of the work experience", default=None)


class WorkExperienceSchema(PersonAttributeSchema):
    doctype: str = "WorkExperience"
    match_option: str = Field(description="Match type: confirmed_match, likely_match, unclear, not_match", default=None)
    value: Optional[WorkExperienceModel] = Field(description="Work experience of the person", default=None)


class EducationModel(BaseModel):
    school: Optional[str] = Field(description="School of the education", default=None)
    degree: Optional[str] = Field(description="Degree of the education", default=None)
    field_of_study: Optional[str] = Field(description="Field of study of the education", default=None)
    start_date: Optional[datetime] = Field(description="Start date of the education", default=None)
    end_date: Optional[datetime] = Field(description="End date of the education", default=None)
    additional_info: Optional[str] = Field(description="Additional information of the education", default=None)


class EducationSchema(PersonAttributeSchema):
    doctype: str = "Education"
    match_option: str = Field(description="Match type: confirmed_match, likely_match, unclear, not_match", default=None)
    value: Optional[EducationModel] = Field(description="Education of the person", default=None)


class NetworkSignatureModel(BaseModel):
    source: str = Field(description="Source of the network signature", default=None)
    username: Optional[str] = Field(description="Username of the network signature", default=None)
    url: Optional[str] = Field(description="URL of the network signature", default=None)
    user_id: Optional[str] = Field(description="User ID of the network signature", default=None)


class NetworkSignatureSchema(PersonAttributeSchema):
    doctype: str = "NetworkSignature"
    match_option: str = Field(description="Match type: confirmed_match, likely_match, unclear, not_match", default=None)
    value: Optional[NetworkSignatureModel] = Field(description="Network signature of the person", default=None)


class UnifiedPerson(BaseModel):
    doctype: str = "UnifiedPerson"
    f_name: FirstNameSchema = Field(description="First name of the person", default=FirstNameSchema())
    l_name: LastNameSchema = Field(description="Last name of the person", default=LastNameSchema())
    full_name: FullNameSchema = Field(description="Full name of the person", default=FullNameSchema())

    # add sources like google or linkedin to saved results and may be use doctype as addidtion field {'source': ..., "source_type": ..., }
    phone_number: PhoneNumberSchema = Field(description="Phone number of the person", default=PhoneNumberSchema())
    email_address: EmailAddressSchema = Field(description="Email address of the person", default=EmailAddressSchema())
    images: ImageSchema = Field(description="Images of the person", default=ImageSchema())
    locations: List[LocationSchema] = Field(description="Locations of the person", default=[])
    work_experience: List[WorkExperienceSchema] = Field(description="Work experience of the person", default=[])
    education: List[EducationSchema] = Field(description="Education of the person", default=[])
    network_signature: List[NetworkSignatureSchema] = Field(description="Network signature of the person", default=[])
    start_timestamp: Optional[datetime] = Field(description="Start timestamp of the person", default=None)
    end_timestamp: Optional[datetime] = Field(description="End timestamp of the person", default=None)


class UnifiedPersonModel(UnifiedPerson, CreateUpdateMixin, Document):
    input: SearchInput

    class Settings:
        name = "unified_persons"

    def update_input_from_model(self) -> None:
        def get_field_value_high_probability(items: List[ValueRanking]):
            if not items:
                return None
            _items = copy.deepcopy(items)
            if len(_items) > 1:
                _items = sorted(_items,key=lambda vr: (vr.ranking, -vr.count))
            return _items[0].value
        # firstname
        if (not self.input.firstname
                and (firstname := get_field_value_high_probability(
                    self.f_name.f_name))):
            self.input.firstname = str(firstname)
        # lastname
        if (not self.input.lastname
                and(lastname := get_field_value_high_probability(
                    self.l_name.l_name))):
            self.input.lastname = str(lastname)
        # email
        if (not self.input.email and (email := get_field_value_high_probability(
                self.email_address.email_address))):
            self.input.email = str(email)
        # homephone, cellphone
        if phone := get_field_value_high_probability(
                self.phone_number.phone_number):
            self.input.homephone = str(phone)
            self.input.cellphone = str(phone)
        # photos
        if photos := [i.value for i in self.images.image]:
            if not self.input.photo:
                self.input.photo = photos
            else:
                # deduplication
                self.input.photo = list(set(self.input.photo + photos))
        # locations
        if self.locations and len(self.locations) > 0:
            location_items = [location.value for location in self.locations if location.match_option == 'confirmed match' and location.value]
            if not location_items and len(location_items) == 0:
                location_items = [location.value for location in self.locations if location.match_option == 'likely match' and location.value]
            if location_items and len(location_items) > 0:
                location = {i:j for i, j in location_items[0].model_dump().items() if j}
                self.input.locations = " ".join(dotty(location).values())
        # education
        if self.education and len(self.education) > 0:
            education_items = [education.value for education in self.education if education.match_option == 'confirmed match' and education.value]
            if not education_items and len(education_items) == 0:
                education_items = [education.value for education in self.education if education.match_option == 'likely match' and education.value]
            if education_items and len(education_items) > 0:
                education = {i:j for i, j in education_items[0].model_dump().items() if j}
                self.input.education = " ".join(dotty(education).values())
        # work_experience
        if self.work_experience and len(self.work_experience) > 0:
            work_experience_items = [work_experience.value for work_experience in self.work_experience if work_experience.match_option == 'confirmed match' and work_experience.value]
            if not work_experience_items and len(work_experience_items) == 0:
                work_experience_items = [work_experience.value for work_experience in self.work_experience if work_experience.match_option == 'likely match' and work_experience.value]
            if work_experience_items and len(work_experience_items) > 0:
                work_experience = {i:j for i, j in work_experience_items[0].model_dump().items() if j}
                self.input.work = " ".join(dotty(work_experience).values())
        if self.network_signature and len(self.network_signature) > 0:
            network_signature_items = [network_signature.value for network_signature in self.network_signature if network_signature.match_option == 'confirmed match' and network_signature.value]
            if not network_signature_items and len(network_signature_items) == 0:
                network_signature_items = [network_signature.value for network_signature in self.network_signature if network_signature.match_option == 'likely match' and network_signature.value]
            if network_signature_items and len(network_signature_items) > 0:
                network_signature = {i:j for i, j in network_signature_items[0].model_dump().items() if j}
                self.input.network_signature = " ".join(dotty(network_signature).values())


class ExtractedPersonalDetails(BaseModel):
    doctype: str = "ExtractedPersonalDetails"
    f_name: Optional[str] = Field(description="First name of the person")
    l_name: Optional[str] = Field(description="Last name of the person")
    name: Optional[str] = Field(description="full name of the person")
    email_address: Optional[str] = Field(description="email address of the person")
    phone_number: Optional[str] = Field(description="phone number of the person")
    city: Optional[str] = Field(description="city of the person")
    country: Optional[str] = Field(description="country of the person")
    # education: Optional[str] =  Field(description="education of the person")
    # work: Optional[List[str]] =  Field(description="work history of the person")
    # query: Optional[str] =  Field(description="search query related to the person")
    # bio: Optional[str] =  Field(description="Job title")
    # username: Optional[str] =  Field(description="Job title")
    # is_rare_name: bool =  Field(description="Job title")


class UrlDetails(BaseModel):
    url: Optional[str] = Field(description="Source URL of the URL's details", default=None)
    title: Optional[str] = Field(description="Job title", default=None)
    company: Optional[str] = Field(description="Company of employment", default=None)
    city: Optional[str] = Field(description="City of employment", default=None)
    industry: Optional[str] = Field(description="Industry of employment", default=None)
    skills: Optional[List[str]] = Field(description="Skills utilized in profession", default=None)
    match_option: str = Field(description="Match type: confirmed match, likely match, unclear, not match", default=None)


class ExtractedCandidate(BaseModel):
    doctype: str = "ExtractedCandidate"
    source: Optional[str] = Field(description="Source of the candidate. Must be one of the following: google, linkedin, facebook, instagram", default=None)
    # extracted_personal_details: Optional[ExtractedPersonalDetails] = None
    # url_details: Optional[List[UrlDetails]] = None
    # source: Optional[str] = Field(description="Source of the candidate")
    # images: Optional[List[str]] = Field(description="Images of the candidate")
    f_name: Optional[str] = Field(description="First name of the person", default=None)
    l_name: Optional[str] = Field(description="Last name of the person", default=None)
    full_name: Optional[str] = Field(description="Full name of the person", default=None)

    # add sources like google or linkedin to saved results and may be use doctype as addidtion field {'source': ..., "source_type": ..., }
    phone_number: Optional[str] = Field(description="Phone number of the person", default=None)
    email_address: Optional[str] = Field(description="Email address of the person", default=None)
    images: Optional[List[str]] = Field(description="Images of the person", default=None)
    locations: Optional[List[LocationSchema]] = Field(description="Locations of the person", default=None)
    work_experience: Optional[List[WorkExperienceSchema]] = Field(description="Work experience of the person", default=None)
    education: Optional[List[EducationSchema]] = Field(description="Education of the person", default=None)
    network_signature: List[NetworkSignatureSchema] = Field(description="Network signature of the person", default=None)
    timestamp: Optional[datetime] = Field(description="Timestamp of the candidate extraction", default=None)
    # match_option: str = Field(description="Match type: confirmed match, likely match, unclear, not match", default=None)

    def to_json(self) -> dict:
        return self.model_dump()


class ExtractedCandidateModel(ExtractedCandidate, CreateUpdateMixin, Document):
    unified_person: Link[UnifiedPersonModel]

    class Settings:
        name = "extracted_candidates"
        indexes = [
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
        ]
