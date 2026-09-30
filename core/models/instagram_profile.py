from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema


class InstagramProfile(SignAIghtSchema):
    instagram_id: Optional[str] = Field(None, examples=["123456789"])
    instagram_full_name: Optional[str] = Field(None, examples=["John Doe"])
    instagram_f_name: Optional[str] = Field(None, examples=["John"])
    instagram_l_name: Optional[str] = Field(None, examples=["Doe"])
    instagram_picture: Optional[str] = Field(None, examples=["https://..."])
    instagram_username: Optional[str] = Field(None, examples=["johndoe"])
    instagram_followers_count: Optional[int] = Field(None, examples=[100])
    instagram_following_count: Optional[int] = Field(None, examples=[100])
    instagram_media_count: Optional[int] = Field(None, examples=[100])
    is_new_to_instagram: Optional[bool] = Field(None, examples=[False])
    instagram_is_private: Optional[bool] = Field(None, examples=[False])
    instagram_chaining_results: Optional[List] = Field(None, examples=[[]])
