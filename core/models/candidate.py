import uuid
from beanie import Link, after_event, Insert, Update, Replace, Delete
from datetime import datetime
from core.models.utils.followers_mapping import ONLINE_SIGNATURE_MAPPING
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import Optional, List, Union

from core.fields import S3Path

from .base import SignAIghtSchema, Document
from .person import PersonModel, Person


class CandidateDarknet(SignAIghtSchema):
    breach_name: Optional[str]
    confidence: Optional[str]
    exposed_fields: Optional[str]


class Candidate(Person, SignAIghtSchema):
    primary: bool = False
    search_id: str = Field(..., examples=[
                           "55c05aa4-2aee-4762-b966-b2dc50928cd5"])
    searched_at: datetime
    source: str = Field(examples=["facebook"])
    resource: Optional[str] = Field(None, examples=["social_links"])
    darknet: Optional[CandidateDarknet] = None
    similarity: float = 0
    ds_filter: bool = False
    projects_list: Optional[List[Union[str, uuid.UUID]]] = None


class CandidateModel(Document, Candidate):
    person: Link[PersonModel]

    class Settings:
        name = "candidates"
        keep_nulls = False
        indexes = [
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("search_id", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("primary", ASCENDING),
                    ("person.$id", ASCENDING),
                    ("search_id", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                    ("search_id", ASCENDING),
                    ("source", ASCENDING),
                    ("resource", ASCENDING),
                    ("searched_at", DESCENDING),
                ],
                name=("candidates_person_search_id_source_resource"
                      "_searched_at"),
                background=True,
                sparse=True
            ),
            # IndexModel(
            #    [
            #        ("person.$id", ASCENDING),
            #        ("search_id", ASCENDING),
            #        ("source", ASCENDING),
            #        ("resource", ASCENDING),
            #        ("network_signature.user_id", ASCENDING),
            #        ("network_signature.user_name", ASCENDING),
            #        ("searched_at", DESCENDING),
            #    ],
            #    name=("candidates_person_search_id_source_resource"
            #          "_primary_ns_user_id_ns_user_name_searched_at"),
            #    background=True,
            #    sparse=True
            # ),
            # IndexModel(
            #    [
            #        ("network_signature.misc", ASCENDING),
            #        ("network_signature.passwords", ASCENDING),
            #        ("network_signature.url", ASCENDING),
            #        ("network_signature.user_id", ASCENDING),
            #        ("network_signature.username", ASCENDING),
            #        ("search_id", ASCENDING),
            #    ],
            #    name=("candidates_search_id_network_signature_fields"),
            #    background=True,
            #    sparse=True
            # ),
            IndexModel(
                [
                    ("person.$id", ASCENDING),
                    ("primary", ASCENDING),
                ],
                name=("candidates_person_id_compound index"),
                background=True,
                sparse=True
            ),

        ]
        use_revision = False
        # Required to save s3 url into database properly
        # IMPORTANT! Should defined in top level model,
        # not in nested document
        bson_encoders = {
            S3Path: str
        }

    async def _update_person_network_signature(self, action: str):
        """
        Atomic PersonModel Update
        """
        person_id = None
        if isinstance(self.person, Link):
            person_id = self.person.ref.id
        elif isinstance(self.person, PersonModel):
            person_id = self.person.id

        if not person_id:
            return

        source = self.source
        candidate_id = self.id
        inc_val = 1 if action == "add" else (-1 if action == "delete" else 0)

        mp_base = "network_signature.matched_profiles"
        source_path = f"{mp_base}.{source}"

        pipeline = [
            {
                "$set": {
                    "network_signature": {
                        "$cond": [
                            {"$or": [{"$eq": ["$network_signature", None]}, {
                                "$not": ["$network_signature"]}]},
                            {"matched_profiles": None},
                            "$network_signature"
                        ]
                    }
                }
            },
            {
                "$set": {
                    mp_base: {
                        "$cond": [
                            {"$or": [{"$eq": [f"${mp_base}", None]},
                                     {"$not": [f"${mp_base}"]}]},
                            {},
                            f"${mp_base}"
                        ]
                    }
                }
            },
            {
                "$set": {
                    source_path: {
                        "$ifNull": [
                            f"${source_path}",
                            {"candidates_count": 0, "primary_candidate": None}
                        ]
                    }
                }
            },
            {
                "$set": {
                    f"{source_path}.candidates_count": {
                        "$max": [0,
                                 {"$add": [f"${source_path}.candidates_count",
                                           inc_val]}]
                    }
                }
            }
        ]

        candidate_info = (
            self._extract_candidate_info()
            if action in ["add", "update"] and self.primary
            else None
        )

        if action in ["add", "update"] and self.primary:
            pipeline.append({
                "$set": {
                    f"{source_path}.primary_candidate.{candidate_id}": (
                        candidate_info)
                }
            })

        elif action == "delete":
            pipeline.append({
                "$unset": [f"{source_path}.primary_candidate.{candidate_id}"]
            })

        await PersonModel.find_one(PersonModel.id == person_id).update(
            pipeline)

    def _get_bio_from_biographic_details(
       self
    ) -> Optional[str]:
        if not self.biographic_details:
            return None

        bio_intro = getattr(self.biographic_details, "description_bio_intro", None)
        if not bio_intro:
            return None
        source = self.source

        # --- Special cases first ---

        if source == "twitter":
            twitter_desc = getattr(bio_intro, "twitter_description", None)
            return getattr(twitter_desc, "description_text", None)

        if source == "facebook":
            fb_intro = getattr(bio_intro, "fb_profile_intro", None)
            return getattr(fb_intro, "fb_profile_intro_text", None)

        if source == "linkedin":
            return (
                bio_intro.linkedin_profile_description
                or bio_intro.linkedin_headline
            )

        # --- Generic mapping fallback ---
        field_name = f"{source}_bio"

        return getattr(bio_intro, field_name, None)
        
    def _extract_online_counts(self):
        if not self.network_signature or not self.network_signature.online_signature:
            return {"followers": None, "following": None, "friends": None}

        source = self.source
        online = self.network_signature.online_signature

        mapping = ONLINE_SIGNATURE_MAPPING.get(source, {})

        def get_value(field_name):
            if not field_name:
                return None
            return getattr(online, field_name, None)

        return {
            "followers": get_value(mapping.get("followers")),
            "following": get_value(mapping.get("following")),
            "friends": get_value(mapping.get("friends")),
        }
        
    def _extract_location(self):
        if not self.personal_details or not self.personal_details.location:
            return None

        location_obj = self.personal_details.location
        source = self.source

        def _first(value):
            if isinstance(value, list) and value:
                return value[0]
            return value

        source_location = getattr(location_obj, f"{source}_location", None)
        if source_location:
            return _first(source_location)

        if getattr(location_obj, "current_city", None):
            city = getattr(location_obj.current_city, "fb_current_city", None)
            if city:
                return city

        if getattr(location_obj, "current_city_region_country", None):
            linkedin_loc = getattr(
                location_obj.current_city_region_country,
                "linkedin_location",
                None
            )
            if linkedin_loc:
                return linkedin_loc

        if getattr(location_obj, "current_country", None):
            country = getattr(
                location_obj.current_country,
                "linkedin_location_country",
                None
            )
            if country:
                return country

        if getattr(location_obj, "hometown", None):
            hometown = getattr(location_obj.hometown, "fb_hometown", None)
            if hometown:
                return hometown

        grfx = getattr(location_obj, "grfx_location", None)
        if grfx:
            return _first(grfx)

        return None

    def _extract_candidate_info(self):
        source = self.source

        def _get_first(obj, attr):
            if not obj:
                return None
            value = getattr(obj, attr, None)
            if isinstance(value, list) and value:
                return value[0]
            return value
        
        counts = self._extract_online_counts()


        return {
            "f_name": getattr(
                self.personal_details.name.first_name, f"{source}_f_name",
                None) if self.personal_details else None,
            "l_name": getattr(
                self.personal_details.name.last_name, f"{source}_l_name",
                None) if self.personal_details else None,
            "full_name": getattr(
                self.personal_details.name.full_name, f"{source}_full_name",
                None) if self.personal_details else None,
            "profile_id": _get_first(
                self.network_signature.user_id, f"{source}_user_id") if
            self.network_signature else None,
            "profile_url": _get_first(
                self.network_signature.url, f"{source}_profile_url") if
            self.network_signature else None,
            "profile_username": _get_first(
                self.network_signature.username, f"{source}_username") if
            self.network_signature else None,
            "profile_picture": getattr(
                self.personal_details.visuals.profile_photo,
                f"{source}_profile_picture", None) if
            self.personal_details and self.personal_details.visuals else None,
            "creation_date": getattr(
                self.network_signature.misc, f"{source}_creation_date",
                None) if self.network_signature else None,
            "location": self._extract_location(),
            "birthdate": getattr(
                self.personal_details.birth_year_birthday.birthday,
                f"{source}_birthdate", None) if self.personal_details and
            self.personal_details.birth_year_birthday else None,
            "followers": counts["followers"] if counts and counts["followers"] is not None else None,
            "following": counts["following"] if counts and counts["following"] is not None else None,
            "friends": counts["friends"] if counts and counts["friends"] is not None else None,
            "bio": self._get_bio_from_biographic_details()
    }


    @after_event(Insert)
    async def add_candidate(self):
        await self._update_person_network_signature(action="add")

    @after_event(Replace, Update)
    async def update_candidate(self):
        await self._update_person_network_signature(action="update")

    @after_event(Delete)
    async def delete_candidate(self):
        await self._update_person_network_signature(action="delete")
