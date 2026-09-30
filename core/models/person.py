from uuid import UUID

from networkx.readwrite import json_graph
from beanie import (
    before_event,
    Update,
    ValidateOnSave,
)
from datetime import datetime
from enum import Enum
from core.models.utils.update_connection_graph import GraphBuilder
from glom import glom
from pydantic import Field, field_validator
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import Optional, List, Any

from core.clients.vetric.linkedin import api as vtrc_api, VtLISpecs
# from core.clients.mapbox.client import api as mapbox_api
from core.dotty_dictionary import dotty
from core.fields import S3Path
from core.logging import logger

from .utils.update_geotrace import can_reuse_existing_trace, geotrace_update
from .base import SignAIghtSchema, Document, WithVerifiedFieldSchema
from .personal_details import PersonalDetails
from .biographic_details import BiographicDetails
from .network_signature import NetworkSignature
from .post import Post
from .interests import Interests
from .geo_trace import GeoTrace
from .audit_log import AuditLogMixin, AuditLog, UnionAuditLog, AuditLogUser
from .search_state import SearchState
from .comment import Comment
from .connections import Connections
from .merge_metadata import MergeMetadata
from .pnr_data import PersonPNRData


class Scores(SignAIghtSchema):
    courage: Optional[int] = Field(None, examples=[100])
    consistency: Optional[int] = Field(None, examples=[100])
    credibility: Optional[int] = Field(None, examples=[100])
    conscientiousness: Optional[int] = Field(None, examples=[100])
    clandestineness: Optional[int] = Field(None, examples=[100])


class Compatibility(Enum):
    high_compatibility = "High Compatibility"
    medium_compatibility = "Medium Compatibility"
    low_compatibility = "Low Compatibility"
    disqualified = "Disqualified"


class RecruitingSource(Enum):
    application = "application"
    internet = "internet"


class Person(WithVerifiedFieldSchema):
    personal_details: Optional[PersonalDetails] = None
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    posts: Optional[List[Post]] = None
    interests: Optional[Interests] = None
    nationality: Optional[str] = None
    comments: Optional[List[Comment]] = None
    signaight_score: Optional[int] = Field(None, examples=[80], gte=0, lte=100)
    risk_score: Optional[int] = Field(0, examples=[80], gte=0, lte=100)
    compatibility: Optional[Compatibility] = None
    scores: Optional[Scores] = None
    demo_data: bool = False
    search_state: Optional[SearchState] = None
    geo_trace: Optional[GeoTrace] = None
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, examples=[
            str(datetime.now().isoformat())]
    )
    last_update: Optional[datetime] = Field(
        None, examples=[str(datetime.utcnow().isoformat())])
    last_edited_by: Optional[AuditLogUser] = None
    recruiting_source: Optional[
        RecruitingSource] = RecruitingSource.application
    search_id: Optional[str] = None
    connections: Optional[Connections] = None
    is_favorite: bool = False
    is_attention: bool = False
    red_flags_count: Optional[int] = None
    alerts_count: Optional[int] = None
    evaluation_count: Optional[int] = None
    merge_metadata: Optional[MergeMetadata] = None
    pnr_data: Optional[PersonPNRData] = None
    connection_graph: Optional[Any] = None

    @field_validator("signaight_score", mode="before")
    @classmethod
    def validate_signaight_score(cls, v):
        if v is None:
            return None
        try:
            # Convert to float first to handle string numbers like "42.8"
            num = float(v)
            return int(round(num, 0))
        except (ValueError, TypeError):
            return None


class PersonModel(AuditLogMixin, Document, Person):

    class Settings:
        name = "persons"
        keep_nulls = False
        indexes = [
            IndexModel(
                [
                    ("project.$id", ASCENDING)
                ],
                background=True,
                sparse=True
            ),
            # IndexModel(
            #     [
            #         ("signaight_score", DESCENDING),
            #         ("personal_details.name.first_name.f_name", ASCENDING),
            #     ],
            #     background=True,
            #     sparse=True
            # ),
            IndexModel(
                [
                    ("search_state.status", DESCENDING),
                    ("personal_details.name.first_name.f_name", ASCENDING),
                ],
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("is_attention", ASCENDING),
                    ("is_favorite", ASCENDING),
                    ("search_state.status", DESCENDING),
                    ("signaight_score", DESCENDING),
                    ("personal_details.name.first_name.f_name", ASCENDING),
                    ("personal_details.name.last_name.l_name", ASCENDING),
                    ("personal_details.email.email_address", ASCENDING),
                    ("search_state", ASCENDING),
                    ("last_update", DESCENDING),
                ],
                name=("persons_for_lists_compound_index"),
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("network_signature.url.linkedin_profile_url", ASCENDING),
                    ("search_state.is_done", ASCENDING),
                    ("search_state.status", ASCENDING),
                    ("last_update", DESCENDING),
                ],
                name=(
                    "persons_project_for_search_for_existing_compound_index"),
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("demo_data", ASCENDING),
                    ("personal_details.name.first_name.f_name", ASCENDING),
                    ("personal_details.name.last_name.l_name", ASCENDING),
                ],
                name=("persons_project_for_demo_data_check_compound_index"),
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ("last_update", ASCENDING),
                    ("project", ASCENDING),
                    ("created_at", ASCENDING)
                ],
                background=True,
                sparse=True
            ),
        ]

        use_state_management = True
        state_management_save_previous = True
        use_revision = True
        keep_nulls = False

        # Required to save s3 url into database properly
        # IMPORTANT! Should defined in top level model,
        # not in nested document
        bson_encoders = {
            S3Path: str
        }

    @before_event(ValidateOnSave, Update)
    async def create_search_state(self):
        if not self.search_state:
            search_state = {
                "is_done": False,
                "status": "In progress",
            }
            self.search_state = search_state

    @before_event(ValidateOnSave, Update)
    async def create_person_geotrace(self):
        try:
            if isinstance(self.personal_details, dict):
                self.personal_details = PersonalDetails(
                    **self.personal_details)
            if not self.personal_details or not self.personal_details.location:
                return
            if self.geo_trace and can_reuse_existing_trace(
                    self.geo_trace,
                    self.personal_details.location.model_dump()):
                return
            is_new = self.get_saved_state() is None
            if is_new:
                self.geo_trace = await geotrace_update(self)
                return

            changes = self.get_changes()
            if not any(key.startswith("personal_details.location") for key in
                       changes):
                return
            self.geo_trace = await geotrace_update(self)
        except Exception as e:
            logger.error(
                f"Error generating geo_trace for person {self.id}: {e}")


    @classmethod
    async def rebuild_graph_connections(self, person_id):
        try:
            if not isinstance(person_id, UUID):
                person_id = UUID(str(person_id))
            person = await self.get(person_id)
            builder = GraphBuilder()
            graph = builder.build([person])
            json_graph_data = json_graph.node_link_data(graph)
            await self.find_one(self.id == person_id).update(
                {"$set": {"connection_graph": json_graph_data}}
            )
        except Exception as e:
            print('GRAPH DATA ERROR', e)
            logger.error(str(e))

    # NOTE: Deprecated and moved to utils/models/update_geotrace.py with improved logic
    # async def update_geotrace(self):

    #     def find_checkin_by_partial_key(check_ins, partial_key):
    #         return next(
    #             (checkin for checkin in check_ins if
    #              partial_key in checkin.get("title", "")),
    #             None
    #         )

    #     location_dict = self.personal_details.location.model_dump()
    #     locations = {key: val for key, val in location_dict.items() if val}
    #     check_ins = []
    #     if location_dict.get('check_ins'):
    #         if check_ins := location_dict.get(
    #                 'check_ins', {}).get("fb_check_ins", []):
    #             check_ins_dict = {f"check_in_{checkin.get('title')}": checkin.get(
    #                 'title') for checkin in check_ins if checkin}
    #             locations.update(**check_ins_dict)
    #         if google_reviews_list := location_dict.get(
    #                 'check_ins', {}).get("google_reviews", []):
    #             reviews_dict = {f"google_review_{review.get('address')}": review.get(
    #                 'address') for review in google_reviews_list if review}
    #             locations.update(**reviews_dict)
    #         locations.pop("check_ins")
    #     [locations] = pandas.json_normalize(
    #         locations, sep=".").to_dict(
    #         orient='records')
    #     location_len = len(locations.keys())
    #     geo_trace = self.geo_trace if self.geo_trace else None
    #     geo_trace_features = []
    #     try:
    #         if geo_trace and len(geo_trace.features) == location_len:
    #             geo_trace_features = self.geo_trace.features
    #             feature_names = [feature.properties.place_name for feature in
    #                              geo_trace_features]
    #             location_items = locations.values()
    #             matching_locations = [name for loc in location_items for name in
    #                                   feature_names if loc in name]
    #             if len(matching_locations) == location_len:
    #                 pass
    #             else:
    #                 geo_trace_features = []
    #     except Exception:
    #         pass
    #     if len(geo_trace_features) == 0 or not (len(geo_trace_features) ==
    #                                             location_len):
    #         geo_trace_features = []
    #         for location_key, location_value in locations.items():
    #             # api search call here location
    #             if (location_value is not False and location_value != "False" and
    #                     location_value is not None and location_value != "None"):
    #                 try:
    #                     response = mapbox_api.search.mapbox(location_value)
    #                     response_body = response.body
    #                     mbox_retrive_data = response_body.get('features', [])[
    #                         0]
    #                 except Exception:
    #                     logger.info(
    #                         f'{location_value} - No matches found in retrive')
    #                     continue
    #                 if not mbox_retrive_data:
    #                     logger.info(
    #                         f'{location_value} - No matches found in retrive')
    #                     continue
    #                 properties = mbox_retrive_data.get('properties', {})
    #                 geometry = mbox_retrive_data.get('geometry', {})
    #                 if 'check_in' in location_key:
    #                     location_type = 'check_ins'
    #                     check_in_title = location_key.replace("check_in_", "")
    #                     try:
    #                         check_in = find_checkin_by_partial_key(
    #                             check_ins, check_in_title)
    #                         date = check_in.get("date")
    #                     except Exception as e:
    #                         print(str(e))
    #                 elif any(key in location_key for key in
    #                          ['hometown', 'current', 'location']):
    #                     location_type = 'residence'
    #                     date = None
    #                 else:
    #                     location_type = 'entities'
    #                     date = None
    #                 feature = Features(**{
    #                     "id": mbox_retrive_data.get('id'),
    #                     "type": "Feature",
    #                     "properties": {
    #                         "mapbox_id": properties.get('mapbox_id'),
    #                         "wikidata": properties.get('wikidata'),
    #                         "short_code": None,
    #                         "place_name": mbox_retrive_data.get('place_name'),
    #                         "location_type": location_type,
    #                         "date": date
    #                     },
    #                     "geometry": {
    #                         "coordinates": geometry.get('coordinates'),
    #                         "type": geometry.get('type', "Point")
    #                     }
    #                 })
    #                 geo_trace_features.append(feature)
    #         if geo_trace_features:
    #             geo_trace_features = dedupe_geo_features(geo_trace_features)

    #             self.geo_trace = GeoTrace(
    #                 type="FeatureCollection",
    #                 features=geo_trace_features
    #             )

    async def _extend_personal_details(self):
        try:
            linkedin_url = self.network_signature.url.linkedin_profile_url[0]
        except Exception:
            linkedin_url = None
        if self.personal_details:
            if self.personal_details.name:
                return self
            elif self.personal_details.email and not linkedin_url:
                return self

        try:
            params = {"url": linkedin_url}
            response = await vtrc_api.async_profile.resolve_url(params=params)
            resolve_url_body = response.body
        except Exception as e:
            print(str(e))
            return self
        source_id = glom(resolve_url_body, VtLISpecs.url_resolver_spec)

        try:
            response = await vtrc_api.async_profile.overview(source_id)
            overview_body = response.body
        except Exception as e:
            print(str(e))
            search_state = {
                "is_done": True,
                "status": "Error",
                "description": "Linkedin Overview Error",
            }
            self.search_state = search_state
            return self
        mapped = dotty(glom(overview_body,
                            VtLISpecs.overview_spec,
                            default={}))

        if ((f_name := mapped.get("personal_details.name.first_name.f_name"))
                and (l_name := mapped.get("personal_details.name.last_name."
                                          "l_name"))):
            mapped['personal_details.name.full_name.full_name'] = " ".join(
                [f_name, l_name])

        if mapped.get('biographic_details.work.linkedin_work.positions.period.'
                      'date_to.year'):
            date_to = (str(mapped.get('biographic_details.work.linkedin_work.'
                                      'positions.period.date_to.year')) +
                       "-" +
                       str(mapped.get(
                           'biographic_details.work.linkedin_work.positions.'
                           'period.date_to.month')) + "-01")
            mapped['biographic_details.work.linkedin_work.positions.period.'
                   'date_to'] = date_to
        else:
            mapped.pop(
                'biographic_details.work.linkedin_work.positions.period.'
                'date_to')

        if mapped.get('biographic_details.work.linkedin_work.positions.period.'
                      'date_from.year'):
            date_from = (str(mapped.get('biographic_details.work.'
                                        'linkedin_work.positions.period.'
                                        'date_from.year')) +
                         "-" +
                         str(mapped.get(
                             'biographic_details.work.linkedin_work.positions.'
                             'period.date_from.month')) + "-01")
            mapped['biographic_details.work.linkedin_work.positions.period.'
                   'date_from'] = date_from
        else:
            mapped.pop(
                'biographic_details.work.linkedin_work.positions.period.'
                'date_from')

        if not mapped.get('biographic_details.work.linkedin_work.positions.'
                          'company_name'):
            mapped.pop('biographic_details.work.linkedin_work.positions')

        if mapped.get('biographic_details.work.linkedin_work.positions'):
            mapped['biographic_details.work.linkedin_work.positions'] = [
                mapped.get('biographic_details.work.linkedin_work.positions')]
        if mapped.get('biographic_details.education.linkedin_schools'):
            mapped['biographic_details.education.linkedin_schools'] = [
                mapped.get('biographic_details.education.linkedin_schools')]

        if self.personal_details:
            if email := self.personal_details.email:
                mapped['personal_details.email'] = email.model_dump()

        personal_details = mapped.get("personal_details")
        biographic_details = mapped.get("biographic_details")

        self.personal_details = PersonalDetails(**personal_details)
        self.biographic_details = BiographicDetails(**biographic_details)
        return self


    async def extend(self):
        await self._extend_personal_details()
        return self


class PersonModelAuditLog(Document, AuditLog):

    class Settings:
        keep_nulls = False
        name = "PersonAuditLog"
        union_doc = UnionAuditLog
        indexes = [
            IndexModel(
                [
                    ("_class_id", ASCENDING),
                    ("entity.$id", ASCENDING),
                    ("editor.id", ASCENDING),
                    ('created_at', DESCENDING)
                ],
                name=("persons_audit_log_multidocument_compound_index"),
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    "revision_id"
                ],
                name=("persons_audit_log_revision_id_index"),
                background=True,
                sparse=True
            ),
            IndexModel(
                [
                    ('_class_id', ASCENDING),
                    ('entity', ASCENDING)
                ],
                name=("persons_audit_log__class_id_index"),
                background=True,
                sparse=True
            ),
        ]

# NOTE: Deprecated and moved to utils/models/update_geotrace.py with
# geotrace improved logic
# def dedupe_geo_features(features):
#     """
#     Return a new list of Features without duplicates.
    # Deduplication key order: feature.id, properties.mapbox_id, properties.place_name.
#     Preserves original order.
#     """
#     seen = set()
#     unique = []

#     for feat in features:
#         # choose the strongest unique key available
#         key = (
#             getattr(feat, "id", None)
#             or feat.properties.mapbox_id
#             or feat.properties.place_name
#         )

#         if key and key not in seen:
#             seen.add(key)
#             unique.append(feat)

#     return unique
