import datetime

from typing import Optional, Union, List
from pydantic import AnyHttpUrl

from .base import WithVerifiedFieldSchema, SignAIghtSchema, Variant


class Leak(SignAIghtSchema):
    title: Optional[str] = None
    url: Optional[Union[str, AnyHttpUrl]] = None


class NetworkMisc(WithVerifiedFieldSchema):
    instagram_is_verified: Optional[bool] = None
    instagram_is_business: Optional[bool] = None
    instagram_is_private: Optional[bool] = None
    twitter_is_protected: Optional[bool] = None
    twitter_is_business_account: Optional[bool] = None
    twitter_is_blue_verified: Optional[bool] = None
    twitter_is_verified: Optional[bool] = None
    xing_profile_type: Optional[str] = None
    leaks: Optional[List[Leak]] = None
    microsoft_last_seen: Optional[Union[str,
                                        datetime.datetime,
                                        datetime.date]] = None
    microsoft_creation_date: Optional[Union[str,
                                            datetime.datetime,
                                            datetime.date]] = None
    myfitnesspal_last_seen: Optional[Union[str,
                                           datetime.datetime,
                                           datetime.date]] = None
    myfitnesspal_creation_date: Optional[Union[str,
                                               datetime.datetime,
                                               datetime.date]] = None
    facebook_last_active: Optional[Union[str,
                                         datetime.datetime,
                                         datetime.date]] = None
    facebook_creation_date: Optional[Union[str,
                                           datetime.datetime,
                                           datetime.date]] = None
    chess_creation_date: Optional[Union[str,
                                        datetime.datetime,
                                        datetime.date]] = None
    chess_last_seen: Optional[Union[str,
                                    datetime.datetime,
                                    datetime.date]] = None
    network_misc_variants: Optional[List[Variant]] = None
