from dotty_dictionary import dotty
from pydantic import BaseModel, AnyHttpUrl, field_validator
from core.documents.base import SearchRequestDocSchema
from typing import Optional, List


__all__ = ["SearchInput"]


class SearchInput(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    # TODO: Maybe reasonable to turn this field into list of urls
    photo: Optional[List[AnyHttpUrl] | AnyHttpUrl] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    dob: Optional[str] = None
    homephone: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[str] = None
    # These fields are intentionally kept as generic types to avoid circular imports
    work: Optional[str] = None
    education: Optional[str] = None
    locations: Optional[str] = None
    network_signature: Optional[str] = None
    external_id: Optional[str] = None

    @field_validator('photo', mode='before')
    @classmethod
    def str_to_list_or_not_none_validator(cls,
            value: List | str | None) -> List[AnyHttpUrl] | None:
        if not value:
            return None
        if not isinstance(value, list):
            value = [value]
        for i, v in enumerate(value):
            try:
                value[i] = AnyHttpUrl(v)
            except Exception:
                pass
        value = [v for v in value if isinstance(v, AnyHttpUrl)]
        return value

    @classmethod
    def from_person(cls, person: dict):
        person_dict = dotty(person)
        return cls(**{
            'firstname': person_dict.get(
                "personal_details.name.first_name.f_name", ''),
            'lastname': person_dict.get(
                "personal_details.name.last_name.l_name", ''),
            'homephone': person_dict.get(
                "personal_details.phone.phones.0", ''),
            'cellphone': person_dict.get(
                "personal_details.phone.phones.0", ''),
            'email': person_dict.get(
                "personal_details.email.email_address.0", ''),
            # NOTE: Beanie models probably are not ready for this data
            # and review required
            # 'address': '1020 w abram st',
            # 'city': 'ARLINGTON',
            # 'state': 'TX',
            # 'zip': '76013',
            # 'dob': '1/1/1998',
        })


    # DEPRECATED: This method does not make any sense
    def __str__(self):
        return super().__str__()

    # DEPRECATED: BaseModel already have proper conversion to json as
    # model_dump_json() method for stringified json or model_dump(mode='json')
    # to get dictionary adopted for safe json.dumps
    def to_json(self) -> dict:
        """
        Convert the SearchInput instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing all the instance attributes.
        """
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "state": self.state,
            "zip": self.zip,
            "dob": self.dob,
            "homephone": self.homephone,
            "cellphone": self.cellphone,
            "email": self.email,
            "work": self.work,
            "external_id": self.external_id

        }

class DocumentSearchInput(SearchRequestDocSchema):
    external_id: str
    f_name : str
    l_name : str
    address :str
    city :   str
    country: str
    state: str
    zip : str
    dob: str
    phone_number: str
    cellphone: str
    email_address: str
    work: str

    def __init__(self,f_name: str = '', l_name: str = '', address: str = '', city: str = '',country='', state: str = '', zip: str = '', dob: str = '', phone_number: str = '', cellphone: str = '', email_address: str = '',work: str='',external_id: str= ''):
        # Use model_construct to bypass validation and set all fields at once
        urn_value = f"to_change_to_urn_{f_name}_{l_name}"
        super().__init__(
            urn=urn_value,
            f_name=f_name,
            l_name=l_name,
            email_address=email_address,
            phone_number=phone_number,
            city=city,
            state=state,
            address=address,
            country=country,
            zip=zip,
            dob=dob,
            cellphone=cellphone,
            work=work,
            external_id=external_id,
        )

    def __str__(self):
        return super().__str__()

    def to_json(self) -> dict:
        """
        Convert the SearchInput instance to a JSON-serializable dictionary.

        Returns:
            dict: A dictionary containing all the instance attributes.
        """
        return {
            "firstname": self.f_name,
            "lastname": self.l_name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "state": self.state,
            "zip": self.zip,
            "dob": self.dob,
            "homephone": self.phone_number,
            "cellphone": self.cellphone,
            "email": self.email_address,
            "work": self.work,
            "external_id": self.external_id

        }
