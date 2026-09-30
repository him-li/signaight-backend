from docarray import BaseDoc
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List


class BaseDocSchema(BaseModel):
    urn: str
    search_id: Optional[str] = None


class SearchRequestSchema(BaseModel):
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    name: Optional[str] = None
    email_address: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    education: Optional[str] = None
    work: Optional[List[str]] = None
    bio: Optional[str] = None
    username: Optional[str] = None


class SearchRequestDocSchema(SearchRequestSchema, BaseDocSchema):
    # DEPRECATED: source, resource should be as params
    # for executors
    source: Optional[str] = None
    resource: Optional[str] = None
    doctype: str = "SearchRequestDoc"
    query: Optional[str] = None
    is_rare_name: bool = True


class SearchRequestDoc(SearchRequestDocSchema, BaseDoc):
    pass


class SearchResponseDocSchema(BaseDocSchema):
    personal_details: Optional[Dict] = None
    biographic_details: Optional[Dict] = None
    network_signature: Optional[Dict] = None
    posts: Optional[List | Dict] = None
    # DEPRECATED: source and resource should be as params for executors
    doctype: str = "SearchResponseDoc"
    resource: Optional[str] = None
    source: Optional[str] = None
    remote_id: Optional[str] = None  # data.user.id
    gender: Optional[str] = None  # ...gender, Probably Enum
    biography: Optional[str] = None  # data.biography
    interests: Optional[Dict] = None


class SearchResponseDoc(SearchResponseDocSchema, BaseDoc):
    pass


class EnrichRequestDocSchema(BaseDocSchema):
    source_id: Optional[str] = None
    doctype: str = "EnrichRequestDoc"
    username: Optional[str] = None
    # TODO: AnyHttpUrl type does not work properly
    profile_url: Optional[str] = None
    # DEPRECATED: source and resource should be as params for executors
    resource: Optional[str] = None
    source: Optional[str] = None


class EnrichRequestDoc(EnrichRequestDocSchema, BaseDoc):
    pass


class EnrichResponseDocSchema(BaseDocSchema):
    doctype: str = "EnrichResponseDoc"
    source: str
    personal_details: Optional[Dict] = None
    biographic_details: Optional[Dict] = None
    network_signature: Optional[Dict] = None
    interests: Optional[Dict] = None
    # NOTE: there was List used previously instead of union with Dict
    # With List type jina won't start
    posts: Optional[List | Dict] = None
    connections: Optional[Dict] = None


class EnrichResponseDoc(EnrichResponseDocSchema, BaseDoc):
    pass


class AggregateRequestDocSchema(BaseDocSchema):
    person_id: str
    candidate_id: Optional[str] = None
    doctype: str = "AggregateRequestDoc"


class AggregateRequestDoc(AggregateRequestDocSchema, BaseDoc):
    pass

# NOTE: Only basic schema defined here. Dummy class
class AggregateResponseDoc(BaseDocSchema, BaseDoc):
    pass


class ActiveSearchRequestDocSchema(BaseDocSchema):
    title: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    resource: Optional[str] = None
    source: Optional[str] = None
    doctype: str = "ActiveSearchRequestDoc"


class ActiveSearchRequestDoc(ActiveSearchRequestDocSchema, BaseDoc):
    pass


class ActiveSearchResponseDocSchema(BaseDocSchema):
    search_id: Optional[str] = None
    personal_details: Optional[Dict] = None
    biographic_details: Optional[Dict] = None
    network_signature: Optional[Dict] = None
    posts: Optional[List | Dict] = None
    resource: Optional[str] = None
    source: Optional[str] = None
    doctype: str = "ActiveSearchResponseDoc"


class ActiveSearchResponseDoc(ActiveSearchResponseDocSchema, BaseDoc):
    pass
