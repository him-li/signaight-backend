import datetime
from pydantic import AnyHttpUrl, field_serializer
from typing import Optional, Any, Union, List
from datetime import date as datetime_date

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema, WithVerifiedFieldSchema, Variant


class CurrentCityRegionCountry(SignAIghtSchema):
    linkedin_search_location: Optional[str] = None
    linkedin_location: Optional[str] = None


class CurrentLocation(SignAIghtSchema):
    linkedin_location_epieos: Optional[str] = None
    fb_lives_in_url: Optional[AnyHttpUrl] = None
    xing_location: Optional[str] = None


class FbLocation(SignAIghtSchema):
    fb_location_id: Optional[str] = None
    fb_location_picture: Optional[Union[S3Path, AnyHttpUrl]] = None

    @field_serializer("fb_location_picture", when_used="json-unless-none")
    def serialize_fb_location_picture_s3path(self,
                                             v: S3Path | str | None,
                                             info):
        return s3path_serializer(v, info)


class CurrentCity(FbLocation):
    fb_current_city: Optional[str] = None


class CurrentCountry(SignAIghtSchema):
    linkedin_location_country: Optional[str] = None


class CurrentRegion(SignAIghtSchema):
    pass


class FacebookCheckIn(SignAIghtSchema):
    id: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    url: Optional[str] = None
    event_image: Optional[Union[S3Path, AnyHttpUrl]] = None
    region: Optional[str] = None
    date: Optional[Union[str, datetime_date, None]] = None

    @field_serializer('event_image', when_used="json-unless-none")
    def serialize_event_image_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class GoogleReview(SignAIghtSchema):
    address: Optional[str] = None
    comment: Optional[str] = None
    date: Optional[Union[str, datetime.date, datetime.datetime]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    lat: Optional[Union[str, float]] = None
    long: Optional[Union[str, float]] = None


class Checkins(SignAIghtSchema):
    fb_check_ins: Optional[List[FacebookCheckIn]] = None
    google_reviews: Optional[List[GoogleReview]] = None


class CurrentLatLong(SignAIghtSchema):
    fb_lives_in_lat: Optional[Union[str, float]] = None
    fb_lives_in_long: Optional[Union[str, float]] = None


class Hometown(FbLocation):
    fb_hometown: Optional[str] = None


class FbPlaceLived(FbLocation):
    fb_moved_to: Optional[str] = None
    fb_moved_at: Optional[str] = None


class PlacesLived(SignAIghtSchema):
    fb_places_lived: Optional[List[FbPlaceLived]] = None


class Location(WithVerifiedFieldSchema):
    location: Optional[Any] = None
    grfx_location: Optional[Any] = None
    instagram_location_id: Optional[str] = None
    fb_location_id: Optional[str] = None
    instagram_location_name: Optional[str] = None
    instagram_location_address: Optional[str] = None
    instagram_location_city: Optional[str] = None
    twitter_location: Optional[str] = None
    microsoft_location: Optional[str] = None
    xing_street_address: Optional[str] = None
    xing_zip_address: Optional[str] = None
    xing_country_province_address: Optional[str] = None
    truecaller_country_code: Optional[str] = None
    icq_location: Optional[str] = None
    runkeeper_location: Optional[str] = None
    goodreads_location: Optional[str] = None
    garminconnect_location: Optional[str] = None
    flickr_location: Optional[str] = None
    foursquare_location: Optional[str] = None
    linkedin_country_code: Optional[str] = None
    cashapp_location: Optional[str] = None
    yelp_location: Optional[str] = None
    quora_location: Optional[str] = None
    chess_location: Optional[str] = None
    current_city_region_country: Optional[CurrentCityRegionCountry] = None
    current_location: Optional[CurrentLocation] = None
    current_city: Optional[CurrentCity] = None
    current_country: Optional[CurrentCountry] = None
    current_region: Optional[CurrentRegion] = None
    check_ins: Optional[Checkins] = None
    current_lat_long: Optional[CurrentLatLong] = None
    hometown: Optional[Hometown] = None
    interpol_birthplace: Optional[str] = None
    places_lived: Optional[PlacesLived] = None
    location_variants: Optional[List[Variant]] = None
