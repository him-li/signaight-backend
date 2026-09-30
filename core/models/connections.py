from typing import Optional, Union, List
from pydantic import AnyHttpUrl, Field, field_serializer

from .base import SignAIghtSchema
from core.fields import S3Path, s3path_serializer


class FacebookConnection(SignAIghtSchema):
    facebook_user_id: str
    facebook_full_name: Optional[str] = None
    facebook_profile_picture: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    facebook_profile_url: Optional[AnyHttpUrl] = Field(
        None,
        examples=["https://www.facebook.com/profile.php?id=100000000000000"]
    )

    @field_serializer("facebook_profile_picture", when_used="json-unless-none")
    def serialize_facebook_profile_picture_s3path(self,
                                                  v: S3Path | str | None,
                                                  info):
        return s3path_serializer(v, info)


class Friends(SignAIghtSchema):
    facebook: Optional[List[FacebookConnection]] = None


class InstagramConnection(SignAIghtSchema):
    instagram_user_id: str
    instagram_username: Optional[str] = None
    instagram_full_name:  Optional[str] = None
    instagram_is_private:   Optional[bool] = None
    instagram_profile_picture: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"]
    )
    instagram_is_verified: Optional[bool] = None

    @field_serializer("instagram_profile_picture",
                      when_used="json-unless-none")
    def serialize_instagram_profile_picture_s3path(self, v: S3Path | str
                                                   | None, info):
        return s3path_serializer(v, info)


class InstagramFollowing(InstagramConnection):
    instagram_profile_picture_id: Optional[str] = None


class Following(SignAIghtSchema):
    facebook: Optional[List[FacebookConnection]] = None
    instagram: Optional[List[InstagramFollowing]] = None


class Followers(SignAIghtSchema):
    facebook: Optional[List[FacebookConnection]] = None
    instagram: Optional[List[InstagramConnection]] = None


class Connections(SignAIghtSchema):
    friends: Optional[Friends] = None
    following: Optional[Following] = None
    followers: Optional[Followers] = None
