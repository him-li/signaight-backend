from typing import Optional, Any, List, Union
from datetime import date, datetime

from .base import WithVerifiedFieldSchema, Variant
from .contact_details import XingContactDetails


class OnlineSignature(WithVerifiedFieldSchema):
    instagram_followers_count: Optional[int] = None
    instagram_following_count: Optional[int] = None
    instagram_following_tag_count: Optional[int] = None
    instagram_posts_count: Optional[int] = None
    fb_followers_count: Optional[int] = None
    fb_following_count: Optional[int] = None
    fb_friends_count: Optional[int] = None
    fb_followers: Optional[Any] = None
    linkedin_connections_count: Optional[int] = None
    linkedin_followers_count: Optional[int] = None
    linkedin_following_count: Optional[int] = None
    linkedin_joined: Optional[int] = None
    linkedin_has_premium: Optional[bool] = None
    linkedin_is_influencer: Optional[bool] = None
    linkedin_is_creator: Optional[bool] = None
    linkedin_associated_hashtags: Optional[List[str]] = None
    twitter_created_at: Optional[Union[str, date, datetime]] = None
    twitter_posts_count: Optional[int] = None
    twitter_favorites_count: Optional[int] = None
    twitter_followers_count: Optional[int] = None
    twitter_following_count: Optional[int] = None
    twitter_media_count: Optional[int] = None
    twitter_statuses_count: Optional[int] = None
    twitter_professional_type: Optional[str] = None
    twitter_professional_category: Optional[str] = None
    twitter_professional_category_id: Optional[str] = None
    twitter_creator_subscription_count: Optional[int] = None
    twitter_list_count: Optional[int] = None
    xing_contacts: Optional[XingContactDetails] = None
    flickr_posts_count: Optional[int] = None
    flickr_following_count: Optional[int] = None
    flickr_followers_count: Optional[int] = None
    vivino_followers_count: Optional[int] = None
    vivino_following_count: Optional[int] = None
    vivino_posts_count: Optional[int] = None
    online_signature_variants: Optional[List[Variant]] = None
