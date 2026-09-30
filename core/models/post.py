from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, List, Union
from enum import Enum
from datetime import datetime

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema, WithVerifiedFieldSchema
from .post_author import PostAuthor
from .tagged_person import TaggedPerson
from .post_liker import PostLiker


class InstagramPostLocation(SignAIghtSchema):
    instagram_location_id: Optional[Union[int, float]] = None
    fb_location_id: Optional[Union[int, float]] = None
    instagram_location_name: Optional[str] = None
    instagram_location_address: Optional[str] = None
    instagram_location_city: Optional[str] = None


class ExternalWebpage(SignAIghtSchema):
    name: Optional[str] = None
    url:  Optional[str] = None


class FacebookPhotoData(SignAIghtSchema):
    url: Optional[Union[S3Path, AnyHttpUrl]] = None
    width: Optional[int] = None
    height: Optional[int] = None

    @field_serializer("url", when_used="json-unless-none")
    def serialize_fb_photo_url_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class FacebookPhoto(SignAIghtSchema):
    fb_photo_id: Optional[str] = None
    fb_photo_likes_count: Optional[int] = None
    fb_photo_reactions_count: Optional[int] = None
    fb_photo_comments_count: Optional[int] = None
    fb_photo: FacebookPhotoData
    fb_photo_lq: Optional[FacebookPhotoData] = None
    fb_photo_mq: Optional[FacebookPhotoData] = None
    fb_photo_hq: Optional[FacebookPhotoData] = None


class FacebookPost(WithVerifiedFieldSchema):
    fb_post_text: Optional[str] = Field(None, help="Facebook Post text")
    fb_post_language: Optional[str] = Field(
        None, help="Language of the original post")
    fb_post_translated_to: Optional[str] = Field(
        None, help="Language of translated post")
    post_translation: Optional[str] = Field(
        None, help="Facebook Post translated text")
    fb_post_external_webpages: Optional[List[ExternalWebpage]] = None
    fb_post_comments_count: Optional[int] = None
    fb_post_likers_count: Optional[int] = None
    fb_post_shares_count: Optional[int] = None
    fb_post_reactors_count: Optional[int] = None
    fb_post_photo: Optional[FacebookPhoto] = None
    fb_uploaded_photo: Optional[FacebookPhoto] = None
    fb_post_publish_at_date: Optional[int] = None
    fb_post_url: Optional[AnyHttpUrl] = None
    fb_post_id: Optional[str] = Field(None, help="Post ID")


class InstagramPost(WithVerifiedFieldSchema):
    instagram_post_text: Optional[str] = Field(None, help="Post text")
    instagram_post_id: Optional[str] = Field(None, help="Post ID")
    instagram_user_id: Optional[str] = Field(None, help="Post Author ID")
    instagram_post_location: Optional[InstagramPostLocation] = None
    instagram_post_likes_count: Optional[int] = None
    post_likers: Optional[List[PostLiker]] = None
    instagram_post_photo: Optional[Union[AnyHttpUrl, S3Path]] = None

    @field_serializer('instagram_post_photo', when_used="json-unless-none")
    def serialize_instagram_post_photo_s3path(self,
                                              v: S3Path | str | None,
                                              info):
        return s3path_serializer(v, info)


class LinkedinReactionTypes(Enum):
    LIKE = "LIKE"
    EMPATHY = "EMPATHY"
    PRAISE = "PRAISE"
    MAYBE = "MAYBE"
    APPRECIATION = "APPRECIATION"
    INTEREST = "INTEREST"
    ENTERTAINMENT = "ENTERTAINMENT"


class LinkedinReactions(SignAIghtSchema):
    linkedin_post_reaction_type: str
    linkedin_post_reaction_type_count: int


class LinkedinPostReaction(SignAIghtSchema):
    reaction_type: str
    reaction_target: str


class LinkedinSharedPost(SignAIghtSchema):
    post_author: Optional[PostAuthor] = None


class LinkedinPost(WithVerifiedFieldSchema):
    linkedin_post_text: Optional[str] = None
    linkedin_post_publishment_date: Optional[datetime] = None
    linkedin_post_comments_count: Optional[int] = None
    linkedin_post_likes_count: Optional[int] = None
    linkedin_post_shares_count: Optional[int] = None
    linkedin_post_photo: Optional[Union[S3Path, AnyHttpUrl]] = None
    linkedin_post_url: Optional[AnyHttpUrl] = None
    reactions: Optional[List[LinkedinReactions]] = None
    post_reaction: Optional[LinkedinPostReaction] = None
    shared_post: Optional[LinkedinSharedPost] = None

    @field_serializer('linkedin_post_photo', when_used="json-unless-none")
    def serialize_linkedin_post_photo_s3path(self,
                                             v: S3Path | str | None,
                                             info):
        return s3path_serializer(v, info)


class TwitterPostCard(SignAIghtSchema):
    description_text: Optional[str] = None
    image_url_large: Optional[Union[S3Path, AnyHttpUrl]] = None
    image_url_original_size: Optional[Union[S3Path, AnyHttpUrl]] = None
    text: Optional[str] = None

    @field_serializer(
        'image_url_large',
        'image_url_original_size',
        when_used="json-unless-none"
    )
    def serialize_twitter_image_url_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class TwitterPostPhoto(SignAIghtSchema):
    post_photo: Optional[Union[S3Path, AnyHttpUrl]] = None

    @field_serializer('post_photo', when_used="json-unless-none")
    def serialize_twitter_post_photo_s3path(self,
                                            v: S3Path | str | None,
                                            info):
        return s3path_serializer(v, info)


class TwitterBasePost(SignAIghtSchema):
    twitter_post_likes_count: Optional[int] = None
    twitter_post_quoted_status: Optional[bool] = None
    twitter_post_language: Optional[str] = None
    twitter_post_quotes_count: Optional[int] = None
    twitter_post_replies_count: Optional[int] = None
    twitter_post_retweets_count: Optional[int] = None
    twitter_post_retweeted_status: Optional[bool] = None
    twitter_post_author_user_id: Optional[str] = None
    twitter_post_possibly_sensitive: Optional[bool] = None
    twitter_post_card: Optional[TwitterPostCard] = None
    twitter_post_photo: Optional[List[TwitterPostPhoto]] = None
    twitter_post_hashtags: Optional[List[str]] = None
    twitter_post_symbols: Optional[List[str]] = None
    twitter_post_urls: Optional[List[str]] = None
    twitter_post_view_count: Optional[int] = None
    twitter_post_id: Optional[str] = None
    twitter_post_text: Optional[str] = None


class TwitterPost(TwitterBasePost):
    twitter_retweeted_post: Optional[TwitterBasePost] = None
    twitter_quoted_post: Optional[TwitterBasePost] = None


class Post(FacebookPost, InstagramPost, LinkedinPost, TwitterPost):
    post_author: Optional[Union[PostAuthor, List[PostAuthor]]] = None
    tagged_profiles: Optional[List[TaggedPerson]] = None
    activity_type: str = "post"
