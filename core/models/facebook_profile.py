from pydantic import Field
from typing import Optional, List, Any

from .base import SignAIghtSchema


class FacebookAbout(SignAIghtSchema):
    facebook_education: Optional[List] = Field(
        None, examples=[["Princeton University"]])
    facebook_work: Optional[List] = Field(None, examples=[["Google"]])
    facebook_current_city: Optional[str] = Field(None, examples=["New York, New York"])


class FacebookProfile(SignAIghtSchema):
    facebook_id: Optional[str] = Field(None, examples=["123456789"])
    facebook_full_name: Optional[str] = Field(None, examples=["John Doe"])
    facebook_f_name: Optional[str] = Field(None, examples=["John"])
    facebook_l_name: Optional[str] = Field(None, examples=["Doe"])
    facebook_username: Optional[str] = Field(None, examples=["johndoe"])
    facebook_profile_picture: Optional[str] = Field(None, examples=["https://..."])
    facebook_profile_url: Optional[str] = Field(None, examples=["https://..."])
    facebook_type: Optional[str] = Field(None, examples=["person"])
    facebook_gender: Optional[str] = Field(None, examples=["male"])
    facebook_about: Optional[Any] = None
    facebook_friends_count: Optional[int] = Field(None, examples=[100])
