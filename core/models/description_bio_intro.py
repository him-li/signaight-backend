from typing import Optional, List, Union
from pydantic import Field

from .base import WithVerifiedFieldSchema, Variant
from .twitter_description import TwitterDescription


class BiographyWithEntities(WithVerifiedFieldSchema):
    instagram_userid: Optional[str] = None
    instagram_username: Optional[str] = None


class FbProfileIntro(WithVerifiedFieldSchema):
    fb_profile_intro_id: Optional[str] = None
    fb_profile_intro_text: Optional[str] = None


class DescriptionBioIntro(WithVerifiedFieldSchema):
    introduction: Optional[str] = Field(None, examples=["Real estate agent"])
    linkedin_headline: Optional[str] = Field(
        None, examples=["Real estate agent"])
    instagram_bio: Optional[str] = Field(None, examples=["Real estate agent"])
    biography_with_entities: Optional[List[BiographyWithEntities]] = Field(
        None, help="details of profiles tagged in one's biography (instagram)")
    instagram_bio_links: Optional[Union[List, str]] = None
    instagram_fb_link_on_profile: Optional[bool] = None
    twitter_description: Optional[TwitterDescription] = None
    fb_profile_intro: Optional[FbProfileIntro] = None
    xing_profile_about_me: Optional[str] = None
    tgm_profile_bio: Optional[str] = None
    goodreads_bio: Optional[str] = None
    garminconnect_bio: Optional[str] = None
    flickr_bio: Optional[str] = None
    foursquare_bio: Optional[str] = None
    linkedin_profile_description: Optional[str] = None
    google_bio: Optional[str] = None
    dropbox_bio: Optional[str] = None
    youtube_profile_bio: Optional[str] = None
    khanacademy_bio: Optional[str] = None
    medium_bio: Optional[str] = None
    notion_bio: Optional[str] = None
    bio_variants: Optional[List[Variant]] = None
