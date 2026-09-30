# from beanie import iterative_migration
# from datetime import datetime
# from pydantic import Field
# from typing import Optional, List

# from core.fields import S3Path

# from core.models.base import SignAIghtSchema, Document

# from core.models.profile_picture import ProfilePicture
# from core.models.position import Position
# from core.models.certification import Certification
# from core.models.course import Course
# from core.models.education import Education
# from core.models.honor import Honor
# from core.models.language import Language
# from core.models.organization import Organization
# from core.models.patent import Patent
# from core.models.phone_number import PhoneNumber
# from core.models.project_part_of import ProjectPartOf
# from core.models.publication import Publication
# from core.models.skill import Skill
# from core.models.test_score import TestScore
# from core.models.volunteering_experience import VolunteeringExperience
# from core.models.volunteering_interest import VolunteeringInterest
# from core.models.website import Website
# from core.models.facebook_profile import FacebookProfile
# from core.models.instagram_profile import InstagramProfile
# from core.models.linkedin_profile import LinkedInProfile
# from core.models.person import RedFlags, Scores

# from core.models.personal_details import PersonalDetails
# from core.models.biographic_details import BiographicDetails
# from core.models.network_signature import NetworkSignature
# from core.models.post import Post


# class OldPerson(SignAIghtSchema):
#     f_name: str = Field(..., example="John")
#     l_name: str = Field(..., example="Doe")
#     full_name: Optional[str] = Field(example="John Doe")
#     email_address: Optional[str] = Field(example="johndoe@mail.com")
#     signaight_score: Optional[int] = Field(example=80)
#     scores: Optional[Scores]
#     red_flags: Optional[List[RedFlags]]
#     last_update: Optional[datetime] = Field(
#         example=str(datetime.utcnow().isoformat()))
#     profile_picture: Optional[ProfilePicture]
#     location: Optional[str] = Field(example="Falls Church")
#     positions: Optional[List[Position]]
#     certifications: Optional[List[Certification]]
#     courses: Optional[List[Course]]
#     educations: Optional[List[Education]]
#     honors: Optional[List[Honor]]
#     languages: Optional[List[Language]]
#     organizations: Optional[List[Organization]]
#     patents: Optional[List[Patent]]
#     phone_numbers: Optional[List[PhoneNumber]]
#     projects_part_of: Optional[List[ProjectPartOf]]
#     publications: Optional[List[Publication]]
#     skills: Optional[List[Skill]]
#     test_scores: Optional[List[TestScore]]
#     volunteering_experiences: Optional[List[VolunteeringExperience]]
#     volunteering_interests: Optional[List[VolunteeringInterest]]
#     websites: Optional[List[Website]]
#     facebook_profile: Optional[FacebookProfile]
#     instagram_profile: Optional[InstagramProfile]
#     linkedin_profile: Optional[LinkedInProfile]

#     class Config:
#         json_encoders = {
#             S3Path: lambda pf: pf.as_presigned_url()
#         }


# class OldPersonModel(Document, OldPerson):
#     class Settings:
#         name = "persons"
#         use_revision = False

#         # Required to expose image as temporarely url in json response
#         json_encoders = {
#             S3Path: lambda pf: pf.as_presigned_url()
#         }
#         # Required to save s3 url into database properly
#         # IMPORTANT! Should defined in top level model,
#         # not in nested document
#         bson_encoders = {
#             S3Path: str
#         }


# class Person(SignAIghtSchema):
#     personal_details: PersonalDetails
#     biographic_details: BiographicDetails
#     network_signature: NetworkSignature
#     posts: Optional[List[Post]]

#     signaight_score: Optional[int] = Field(example=80)
#     scores: Optional[Scores]
#     red_flags: Optional[List[RedFlags]]
#     last_update: Optional[datetime] = Field(
#         example=str(datetime.utcnow().isoformat()))


# class PersonModel(Document, Person):
#     class Settings:
#         name = "persons"
#         use_revision = False

#         # Required to expose image as temporarely url in json response
#         json_encoders = {
#             S3Path: lambda pf: pf.as_presigned_url()
#         }
#         # Required to save s3 url into database properly
#         # IMPORTANT! Should defined in top level model,
#         # not in nested document
#         bson_encoders = {
#             S3Path: str
#         }


# class Forward:
#     @iterative_migration()
#     async def update_to_new_model(self,
#                                   input_document: OldPersonModel,
#                                   output_document: PersonModel):
#         # User input fields
#         if input_document.f_name is not None:
#             output_document.personal_details.name.first_name.f_name = (
#                 input_document.f_name)
#         if input_document.l_name is not None:
#             output_document.personal_details.name.last_name.l_name = (
#                 input_document.l_name)
#         if input_document.full_name is not None:
#             output_document.personal_details.name.full_name.full_name = (
#                 input_document.full_name)
#         else:
#             output_document.personal_details.name.full_name.full_name = input_document.f_name + " " + input_document.l_name
#         if input_document.email_address is not None:
#             output_document.personal_details.email.email_address = [(
#                 input_document.email_address)]
#         else:
#             output_document.personal_details.email.email_address = [""]
#         # Facebook Search fields
#         if input_document.facebook_profile is not None:
#             (output_document.personal_details.name.first_name.
#              facebook_f_name) = (
#                 input_document.facebook_profile.facebook_f_name)
#             output_document.personal_details.name.last_name.facebook_l_name = (
#                 input_document.facebook_profile.facebook_l_name)
#             (output_document.personal_details.name.full_name.
#              facebook_full_name) = (
#                 input_document.facebook_profile.facebook_full_name)
#             (output_document.personal_details.visuals
#                 .profile_photo.facebook_profile_picture) = (
#                 input_document.facebook_profile.facebook_profile_picture)
#             output_document.personal_details.gender.fb_gender = (
#                 input_document.facebook_profile.facebook_gender)
#             output_document.network_signature.user_id.facebook_user_id = (
#                 input_document.facebook_profile.facebook_id)
#             output_document.network_signature.username.facebook_username = (
#                 input_document.facebook_profile.facebook_username)
#             output_document.network_signature.url.facebook_profile_url = (
#                 input_document.facebook_profile.facebook_profile_url)
#         # Instagram Search fields
#         if input_document.instagram_profile is not None:
#             (output_document.personal_details.name.full_name.
#              instagram_full_name) = (
#                 input_document.instagram_profile.instagram_full_name)
#             (output_document.personal_details.visuals
#                 .profile_photo.instagram_profile_picture) = (
#                 input_document.instagram_profile.instagram_picture)
#             output_document.network_signature.user_id.instagram_user_id = (
#                 input_document.instagram_profile.instagram_id)
#             output_document.network_signature.username.instagram_username = (
#                 input_document.instagram_profile.instagram_username)
#             (output_document.network_signature.online_signature
#                 .instagram_followers_count) = (
#                 input_document.instagram_profile.instagram_followers_count)
#             (output_document.network_signature.online_signature
#                 .instagram_following_count) = (
#                 input_document.instagram_profile.instagram_following_count)
#             (output_document.network_signature.online_signature
#                 .instagram_posts_count) = (
#                 input_document.instagram_profile.instagram_media_count)
#             output_document.network_signature.misc.instagram_is_private = (
#                 input_document.instagram_profile.instagram_is_private)
#         # LinkedIn Search fields
#         if input_document.linkedin_profile is not None:
#             (output_document.personal_details.name.first_name.
#              linkedin_f_name) = (
#                 input_document.linkedin_profile.linkedin_f_name)
#             output_document.personal_details.name.last_name.linkedin_l_name = (
#                 input_document.linkedin_profile.linkedin_l_name)
#             (output_document.personal_details.name.full_name.
#              linkedin_full_name) = (
#                 input_document.linkedin_profile.linkedin_full_name)
#             output_document.personal_details.email.linkedin_email_address = (
#                 input_document.linkedin_profile.linkedin_email_address)
#             output_document.network_signature.username.linkedin_username = (
#                 input_document.linkedin_profile.linkedin_username)
#             output_document.network_signature.user_id.linkedin_user_id = (
#                 input_document.linkedin_profile.linkedin_id)
#             output_document.network_signature.url.linkedin_profile_url = (
#                 input_document.linkedin_profile.linkedin_profile_url)
#             (output_document.personal_details.visuals
#                 .profile_photo.linkedin_profile_picture) = (
#                 input_document.linkedin_profile.linkedin_profile_picture)
#             (output_document.personal_details.location
#                 .current_city_region_country.linkedin_location) = (
#                 input_document.linkedin_profile.linkedin_location)
#         # Location
#         output_document.personal_details.location.location = (
#             input_document.location)
#         # Last Update
#         output_document.last_update = input_document.last_update
#         # SignAIght Score
#         output_document.signaight_score = input_document.signaight_score
#         # Scores
#         output_document.scores = input_document.scores
#         # Red Flags
#         output_document.red_flags = input_document.red_flags
#         # Biographic Details
#         output_document.biographic_details = {}
#         # Network Signature
#         output_document.network_signature = {}


# class Backward:
#     @iterative_migration()
#     async def update_to_old_model(self,
#                                   input_document: PersonModel,
#                                   output_document: OldPersonModel):
#         # User input fields
#         output_document.f_name = (input_document.personal_details
#                                   .name.first_name.f_name)
#         output_document.l_name = (input_document.personal_details
#                                   .name.last_name.l_name)
#         output_document.full_name = (input_document.personal_details
#                                      .name.full_name.full_name)
#         output_document.email_address = (input_document.personal_details
#                                          .email.email_address)
#         # Facebook Search fields
#         output_document.facebook_profile.facebook_f_name = (
#             input_document.personal_details.name.first_name.facebook_f_name)
#         output_document.facebook_profile.facebook_l_name = (
#             input_document.personal_details.name.last_name.facebook_l_name)
#         output_document.facebook_profile.facebook_full_name = (
#             input_document.personal_details.name.full_name.facebook_full_name)
#         output_document.facebook_profile.facebook_profile_picture = (
#             input_document.personal_details.visuals
#             .profile_photo.facebook_profile_picture)
#         output_document.facebook_profile.facebook_gender = (
#             input_document.personal_details.gender.fb_gender)
#         output_document.facebook_profile.facebook_id = (
#             input_document.network_signature.user_id.facebook_user_id)
#         output_document.facebook_profile.facebook_username = (
#             input_document.network_signature.username.facebook_username)
#         output_document.facebook_profile.facebook_profile_url = (
#             input_document.network_signature.url.facebook_profile_url)
#         # Instagram Search fields
#         output_document.instagram_profile.instagram_full_name = (
#             input_document.personal_details.name.full_name.instagram_full_name)
#         output_document.instagram_profile.instagram_picture = (
#             input_document.personal_details.visuals
#             .profile_photo.instagram_profile_picture)
#         output_document.instagram_profile.instagram_id = (
#             input_document.network_signature.user_id.instagram_user_id)
#         output_document.instagram_profile.instagram_username = (
#             input_document.network_signature.username.instagram_username)
#         output_document.instagram_profile.instagram_followers_count = (
#             input_document.network_signature.online_signature
#             .instagram_followers_count)
#         output_document.instagram_profile.instagram_following_count = (
#             input_document.network_signature.online_signature
#             .instagram_following_count)
#         output_document.instagram_profile.instagram_media_count = (
#             input_document.network_signature.online_signature
#             .instagram_posts_count)
#         output_document.instagram_profile.instagram_is_private = (
#             input_document.network_signature.misc.instagram_is_private)
#         # LinkedIn Search fields

#         output_document.linkedin_profile.linkedin_f_name = (
#             input_document.personal_details.name.first_name.linkedin_f_name)
#         output_document.linkedin_profile.linkedin_l_name = (
#             input_document.personal_details.name.last_name.linkedin_l_name)
#         output_document.linkedin_profile.linkedin_full_name = (
#             input_document.personal_details.name.full_name.linkedin_full_name)
#         output_document.linkedin_profile.linkedin_email_address = (
#             input_document.personal_details.email.linkedin_email_address)
#         output_document.linkedin_profile.linkedin_username = (
#             input_document.network_signature.username.linkedin_username)
#         output_document.linkedin_profile.linkedin_id = (
#             input_document.network_signature.user_id.linkedin_user_id)
#         output_document.linkedin_profile.linkedin_profile_url = (
#             input_document.network_signature.url.linkedin_profile_url)
#         output_document.linkedin_profile.linkedin_profile_picture = (
#             input_document.personal_details.visuals
#             .profile_photo.linkedin_profile_picture)
#         output_document.linkedin_profile.linkedin_location = (
#             input_document.personal_details.location
#             .current_city_region_country.linkedin_location)
#         # Location
#         output_document.location = (
#             input_document.personal_details.location.location)
#         # Last Update
#         output_document.last_update = input_document.last_update
#         # SignAIght Score
#         output_document.signaight_score = input_document.signaight_score
#         # Scores
#         output_document.scores = input_document.scores
#         # Red Flags
#         output_document.red_flags = input_document.red_flags
