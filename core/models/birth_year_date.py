import datetime
from pydantic import Field
from typing import Optional, Union, List

from .base import SignAIghtSchema, WithVerifiedFieldSchema, Variant


class Birthday(SignAIghtSchema):
    birthday: Optional[datetime.date] = Field(None, examples=["01/01/1990"])
    eumw_birthday: Optional[
        Union[str, datetime.datetime, datetime.date]] = Field(
        None, examples=["01/01/1990"])
    linkedin_birthday: Optional[datetime.date] = Field(
        None, examples=["01/01/1990"])
    twitter_birthdate: Optional[datetime.date] = Field(
        None, examples=["01/01/1990"])
    fb_birthday: Optional[datetime.date] = Field(None, examples=["01/01/1990"])
    fb_birth_date: Optional[str] = Field(None, examples=["01/01"])
    fb_birth_year: Optional[int] = Field(None, examples=[1990])
    goodreads_birth_date: Optional[str] = Field(None, examples=["01/01"])
    deezer_birth_date: Optional[str] = Field(None, examples=["01/01"])
    pulsstory_birth_date: Optional[str] = Field(None, examples=["01/01"])
    interpol_birthday: Optional[
        Union[str, datetime.datetime, datetime.date]] = Field(
        None, examples=["01/01/1990"])
    microsoft_birthday: Optional[
        Union[str, datetime.datetime, datetime.date]] = Field(
        None, examples=["01/01/1990"])
    truecaller_birthday: Optional[
        Union[str, datetime.datetime, datetime.date]] = Field(
        None, examples=["01/01/1990"])
    birthday_variants: Optional[List[Variant]] = None


class YearOfBirth(SignAIghtSchema):
    birthyear: Optional[int] = Field(None, examples=[1990])


class BirthYearBirthday(WithVerifiedFieldSchema):
    birthday: Optional[Birthday] = None
    year_of_birth: Optional[YearOfBirth] = None
