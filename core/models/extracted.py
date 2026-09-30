from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, AnyHttpUrl


class ExtractedPersonalDetails(BaseModel):
    source_url: Optional[str] = Field(
        description="Source URL of the person's details")
    f_name: Optional[str] = Field(description="First name of the person")
    l_name: Optional[str] = Field(description="Last name of the person")
    name: Optional[str] = Field(description="full name of the person")
    email_address: Optional[EmailStr] = Field(
        description="email address of the person")
    phone_number: Optional[str] = Field(
        description="phone number of the person")
    city: Optional[str] = Field(description="city of the person")
    country: Optional[str] = Field(description="country of the person")


class ExtractedProfessionalDetails(BaseModel):
    title: Optional[str] = Field(description="Job title")
    company: Optional[str] = Field(description="Company of employment")
    city: Optional[str] = Field(description="City of employment")
    industry: Optional[str] = Field(description="Industry of employment")
    skills: Optional[List[str]] = Field(
        description="Skills utilized in profession")


class ExtractedEducationDetails(BaseModel):
    institution: Optional[str] = Field(description="Educational institution")
    degree: Optional[str] = Field(description="Degree obtained")
    field_of_study: Optional[str] = Field(description="Field of study")
    start_year: Optional[int] = Field(description="Start year of education")
    end_year: Optional[int] = Field(description="End year of education")


class ExtractedBiographicDetails(BaseModel):
    bio: Optional[str] = Field(description="Biographic summary or bio")
    marital_status: Optional[str] = Field(description="Marital status")
    relatives: Optional[List[str]] = Field(
        description="List of relatives' names")


class ExtractedNetworkDetails(BaseModel):
    profile_urls: Optional[List[str]] = Field(
        description="List of social media profile URLs")


class ExtractedPerson(BaseModel):
    extracted_personal_details: Optional[ExtractedPersonalDetails] = None
    extracted_professional_details: Optional[List[
        ExtractedProfessionalDetails]] = None
    extracted_education_details: Optional[List[
        ExtractedEducationDetails]] = None
    extracted_biographic_details: Optional[ExtractedBiographicDetails] = None
    extracted_network_details: Optional[ExtractedNetworkDetails] = None
    images: Optional[List[AnyHttpUrl]] = None
