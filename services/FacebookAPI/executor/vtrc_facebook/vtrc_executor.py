import re
import pendulum
from typing import Dict, List
from nested_lookup import get_occurrences_and_values
from glom import glom
from mergedeep import merge, Strategy

from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    EnrichRequestDoc,
    EnrichResponseDoc,
)
from core.dotty_dictionary import dotty
from core.clients.vetric.facebook import api, VtrcFbSpecs
from core.logging import logger
from core.models.utils import post_service_log
from core.utils.parse_string import parse_numeric_string
from core.utils.extend_check_in import extend_check_in
from services.FacebookAPI.executor.vtrc_facebook.enrich_timeline import enrich_timeline
from services.FacebookAPI.executor.vtrc_facebook.fetch_all_results import (
    fetch_all_results)

from ..config import settings


def drop_none(obj):
    if isinstance(obj, dict):
        return {
            k: drop_none(v)
            for k, v in obj.items()
            if v is not None
        }
    elif isinstance(obj, list):
        return [drop_none(v) for v in obj if v is not None]
    return obj


class VetricFacebookAPI():

    resource = "vetric"

    async def search(
        self,
        doc: SearchRequestDoc,
    ) -> List[SearchResponseDoc]:
        docs = []
        mapped_edges = await fetch_all_results(
            doc,
            limit=settings.VETRIC_FACEBOOK_API_CANDIDATES_LIMIT)
        # NOTE: Deprecated due new candidates search limits mechanism
        # if doc.work:
        #     mapped_edges = mapped_edges[:3]
        for result in mapped_edges:
            try:
                data = {}
                first_name = {"f_name": doc.f_name}
                last_name = {"l_name": doc.l_name}
                full_name = {
                    "full_name": doc.name,
                    "facebook_full_name": result.get("name"),
                }
                email = {
                    "email_address": (
                        [doc.email_address] if doc.email_address else None
                    )
                }
                visuals = {
                    "profile_photo": {
                        "profile_picture": result.get("profile_picture"),
                        "facebook_profile_picture": result.get(
                            "profile_picture"),
                    }
                }
                if not result.get("profile_picture"):
                    if timeline := await enrich_timeline(result.get("id")):
                        data = merge(data, timeline)
                    else:
                        visuals["profile_photo"][
                            "facebook_profile_picture"] = (
                            result.get("profile_picture")
                        )

                network_signature = {"user_id": {
                    "facebook_user_id": [result.get("id")]}}
                if followers := result.get("followers"):
                    followers = parse_numeric_string(followers)
                    online_signature = {
                        "online_signature": {"fb_followers_count": followers}
                    }
                    network_signature = {
                        **network_signature, **online_signature}
                biographic_details = {
                    "description_bio_intro": {
                        "introduction": result.get("description")}
                }
                personal_details = {
                    "name": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "full_name": full_name,
                    },
                    "email": email,
                    "visuals": visuals,
                }
                data["personal_details"] = personal_details
                data["network_signature"] = network_signature
                data["biographic_details"] = biographic_details

                data["urn"] = doc.urn
                data["source"] = "facebook"
                data["resource"] = self.resource
                data["search_id"] = doc.search_id
                _doc = SearchResponseDoc(**data)
                docs.append(_doc)
            except Exception as e:
                print(str(e))
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="FacebookAPI",
                    search_step="search",
                    message=f"Error during search {str(e)}",
                    docs_count=len(docs),
                    step_point="error"
                )

        return docs

    async def _city_helper(self, city) -> Dict:
        _city = {}
        try:
            response = await api.async_search.filters(
                body={"query": city, "filter_type": "city"},
            )
            results = (
                response.body.get("data", {})
                .get("node", {})
                .get("filter_values", {})
                .get("edges", [])
            )
        except Exception as e:
            print(e)
            return _city
        # TODO: maybe make choice more smart cause response is list of
        # object with probability
        if results:
            _c = results[0].get("node").get("value_object", {})
            _city = {
                "id": _c.get("id"),
                "name": _c.get("name"),
                "location": _c.get("location"),
            }
        return _city

    async def _education_helper(self, education) -> Dict:
        _education = {}
        try:
            response = await api.async_search.filters(
                body={"query": education, "filter_type": "education"},
            )
            results = (
                response.body.get("data", {})
                .get("node", {})
                .get("filter_values", {})
                .get("edges", [])
            )
        except Exception as e:
            print(e)
            return _education
        # NOTE: easy results reducer by exact match. Should replaced by
        # smart analyser
        results = get_occurrences_and_values(results, value=education)
        results = results.get(education, {}).get("values")
        if results:
            _edu = results[0].get("value_object", {})
            _education = {
                "id": _edu.get("id"),
                "name": _edu.get("name"),
                "location": _edu.get("location"),
            }
        return _education

    async def _work_helper(self, work) -> Dict:
        _work = {}
        try:
            response = await api.async_search.filters(
                body={"query": work, "filter_type": "work"},
            )
            results = (
                response.body.get("data", {})
                .get("node", {})
                .get("filter_values", {})
                .get("edges", [])
            )
        except Exception as e:
            print(e)
            return _work
        # NOTE: easy results reducer by exact match. Should replaced by
        # smart analyser
        results = get_occurrences_and_values(results, value=work)
        results = results.get(work, {}).get("values")
        if results:
            _edu = results[0].get("value_object", {})
            _work = {
                "id": _edu.get("id"),
                "name": _edu.get("name"),
                "location": _edu.get("location"),
            }
        return _work

    async def enrich(self, doc: EnrichRequestDoc) -> EnrichResponseDoc | None:
        data = {}
        try:
            if timeline := await enrich_timeline(doc.source_id):
                data = merge(data, timeline, strategy=Strategy.ADDITIVE)
                print("Timeline enriched", data)
        except Exception as e:
            print('enrich error timeline: ', str(e))
        try:
            if enriched_about := await self._enrich_about(doc):
                data = merge(data, drop_none(enriched_about),
                             strategy=Strategy.ADDITIVE)
                print("About enriched", data)
        except Exception as e:
            print('enrich error enriched_about: ', str(e))
        try:
            if enriched_posts := await self._enrich_posts(
                    doc,
                    limit=settings.VETRIC_FACEBOOK_API_CANDIDATE_POSTS_LIMIT):
                data = merge(data, enriched_posts, strategy=Strategy.ADDITIVE)
        except Exception as e:
            print('enrich error enriched_posts: ', str(e))
        try:

            if enriched_checkins := await self._enrich_checkings(doc):
                data = merge(data, enriched_checkins,
                             strategy=Strategy.ADDITIVE)
        except Exception as e:
            print('enrich error enriched_checkins: ', str(e))

        try:
            if enriched_uploaded_media := await self._enrich_uploaded_media(
                    doc,
                    limit=(settings.
                           VETRIC_FACEBOOK_API_CANDIDATE_UPLOADED_MEDIA_LIMIT)):
                data = merge(data, enriched_uploaded_media,
                             strategy=Strategy.ADDITIVE)
        except Exception as e:
            print('enrich error enriched_uploaded_media: ', str(e))
        try:
            if enriched_friends := await self._enrich_friends(
                    doc,
                    limit=settings.VETRIC_FACEBOOK_API_CANDIDATE_FRIENDS_LIMIT):
                data = merge(data, enriched_friends)
        except Exception as e:
            print('enrich error enriched_friends: ', str(e))

        try:

            if enriched_places_lived := await self._enrich_places_lived(doc):
                data = merge(data, enriched_places_lived)
        except Exception as e:
            print('enrich error enriched_places_lived: ', str(e))
        try:
            if enriched_pages_liked := await self._enrich_pages_liked(
                    doc,
                    limit=(settings.
                           VETRIC_FACEBOOK_API_CANDIDATE_PAGES_LIKED_LIMIT)):
                data = merge(data, enriched_pages_liked)
        except Exception as e:
            print('enrich error enriched_about: ', str(e))
        try:
            if enriched_following := await self._enrich_following(
                    doc,
                    limit=settings.VETRIC_FACEBOOK_API_CANDIDATE_FOLLOWING_LIMIT):
                data = merge(data, enriched_following)
        except Exception as e:
            print('enrich error enriched_about: ', str(e))

        # Not needed cause we already have facebook picture in good quality
        # enriched_timeline = await self._enrich_timeline(doc)
        # also code became to be legacy
        # for enriched_timeline_doc in enriched_timeline:
        #    enriched_timeline_doc = enriched_timeline_doc.model_dump_json()
        #    enriched_timeline_doc = json.loads(enriched_timeline_doc)
        #    in_docs.append(enriched_timeline_doc)
        if data:
            data = merge(data, {
                "urn": doc.urn,
                "source": "facebook",
                "search_id": doc.search_id
            })
        return EnrichResponseDoc(**data) if data else None

    async def _enrich_about(
            self,
            doc: EnrichRequestDoc
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        data = {}
        try:
            response = await api.async_profiles.about(profile_id)
            response_body = response.body
            spec = VtrcFbSpecs.about_spec_transform
            mapped = glom(response_body, spec, default={})

            if mapped.get("facebook_checkins"):
                for check_in in mapped.get("facebook_checkins"):
                    if subtitle := check_in.get("subtitle"):
                        extend_check_in(check_in, subtitle)
            facebook_locations = mapped.get("facebook_location")
            location = {
                "check_ins": {"fb_check_ins": mapped.get("facebook_checkins")},
                "hometown": facebook_locations.get("fb_hometown") if facebook_locations else None,
                "current_city": facebook_locations.get("fb_current_city") if facebook_locations else None,
                "places_lived": {"fb_places_lived":facebook_locations.get("fb_places_lived") if facebook_locations else None,}
            }

            family_members = []
            if _family_members := mapped.get("facebook_family_members", []):
                for family_member in _family_members:
                    elements = []
                    for val in family_member.values():
                        empty = True if not val else False
                        elements.append(empty)
                    if not all(elements):
                        family_members.append(family_member)

            url = {}
            username = {}
            contact_info = mapped.get("facebook_contact_info") or {}
            if contact_info.get("platforms"):
                for platform in contact_info.get("platforms"):
                    if platform.get("url"):
                        url_key = f"fb_{platform.get('platform_name').lower()}_url"
                        url[url_key] = platform.get("url")
                    if platform.get("username"):
                        username_key = f"fb_{platform.get('platform_name').lower()}_username"
                        username[username_key] = platform.get("username")

            personal_details = {
                "location": location,
                "phone": {"fb_phone": contact_info.get("fb_contact_phone")},
                "email": {"fb_email_address": contact_info.get(
                    "fb_contact_email")},
                "gender": {"fb_gender": mapped.get("facebook_gender")},
                "birth_year_birthday": {"birthday": {
                    "fb_birthday": mapped.get("facebook_birthday")}},
                "languages": {"fb_languages": mapped.get(
                    "facebook_languages")},
                "name": {"nickname": {"fb_nicknames": mapped.get(
                    "fb_nicknames")}},
                "websites": {"websites": contact_info.get("fb_contact_websites")}
            }
            facebook_relationships = mapped.get("facebook_relationships")
            bio_details = {
                "work": {"facebook_work": mapped.get("facebook_work")},
                "education": {
                    "facebook_schools": mapped.get("facebook_education")},
                "marital_status_relatives": {
                    "fb_marital_status": (
                        facebook_relationships if facebook_relationships else None),
                },
            }
            if family_members:
                bio_details["marital_status_relatives"][
                    "facebook_family_members"
                ] = family_members
            network_signature = {
                "url": url if url else None,
                "username": username if username else None,
                "online_signature": {
                    "fb_followers": mapped.get("facebook_followers")},
            }
            data = {}
            if personal_details:
                data["personal_details"] = personal_details
            if bio_details:
                data["biographic_details"] = bio_details
            if network_signature:
                data["network_signature"] = network_signature
        except Exception as e:
            print('enrich error about: ', str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="FacebookAPIReducer",
                search_step="enrich",
                message=f"Error during enrich about: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return None
        try:
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="enrich",
                message=("Found about data"),
                step_point="processing",
            )
        except Exception as e:
            logger.error(f"Unable to send service log: {str(e)}")

        return data if data else None

    async def _enrich_posts(
        self,
        doc: EnrichRequestDoc,
        limit: int = 100
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id

        mapped = []
        end_cursor = None
        has_next_page = True
        while (has_next_page and
               len(mapped) < limit):
            try:
                body = None
                if end_cursor:
                    body = {"end_cursor": end_cursor}
                response = await api.async_profiles.feed(profile_id, body=body)
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="FacebookAPI",
                    search_step="enrich",
                    message=f"Error during enrich feed: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcFbSpecs.new_feed_spec
            if response_body:
                mapped_posts = glom(response_body, spec)
                mapped.extend(mapped_posts)
                end_cursor = response_body.get(
                    "page_info", {}).get("end_cursor")
                has_next_page = response_body.get(
                    "page_info", {}).get("has_next_page", False)
                if (not end_cursor
                        or not has_next_page
                        or len(mapped) > limit):
                    if len(mapped) > limit:
                        mapped = mapped[:limit]
                    has_next_page = False
                    break

        for post in mapped:
            post_author = post.get("post_author")
            if isinstance(
                    post.get("post_author"), list) and len(post_author) > 0:
                post["post_author"] = post.get("post_author", [])[0]

        try:
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="enrich",
                message=(f"Found {len(mapped)} posts"),
                docs_count=len(mapped),
                step_point="processing",
            )
        except Exception as e:
            logger.error(f"Unable to send service log: {str(e)}")

        return {"posts": mapped} if mapped else None

    async def _enrich_checkings(
            self,
            doc: EnrichRequestDoc) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        try:
            response = await api.async_profiles.checkins(profile_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="FacebookAPI",
                search_step="enrich",
                message=f"Error during enrich checkins: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return

        spec = VtrcFbSpecs.checkins_spec
        mapped = glom(response_body, spec, default=[])

        try:
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="enrich",
                message=(f"Found {len(mapped)} checkins"),
                docs_count=len(mapped),
                step_point="processing",
            )
        except Exception as e:
            logger.error(f"Unable to send service log: {str(e)}")

        data = {}
        if mapped:
            data = dotty(data)
            data.setdefault(
                "personal_details.location.check_ins.fb_check_ins", mapped)
            data = data.to_dict()

        return data if data else None

    async def _enrich_uploaded_media(
        self, doc: EnrichRequestDoc,
        limit: int = 100
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        mapped = []
        try:
            response = await api.async_profiles.uploaded_media(
                profile_id,
            )
            response_body = response.body
            spec = VtrcFbSpecs.uploaded_media_spec
            # TODO: fb_post_text always None
            # TODO: post_author always list, should be 1st element of list
            mapped = glom(response_body, spec, default=[]) or []
            if len(mapped) > limit:
                mapped = mapped[:limit]
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="FacebookAPI",
                search_step="enrich",
                message=f"Error during enrich uploaded media: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return

        try:
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="enrich",
                message=(f"Found {len(mapped)} uploaded media"),
                docs_count=len(mapped),
                step_point="processing",
            )
        except Exception as e:
            logger.error(f"Unable to send service log: {str(e)}")

        return {"posts": mapped} if mapped else None

    async def _enrich_friends(
            self,
            doc: EnrichRequestDoc,
            limit: int = 100) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id

        mapped = []
        end_cursor = None
        has_next_page = True
        while (has_next_page and
                len(mapped) < limit):
            try:
                body = None
                if end_cursor:
                    body = {"end_cursor": end_cursor}
                response = await api.async_profiles.friends(
                    profile_id,
                    body=body)
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="FacebookAPI",
                    search_step="enrich",
                    message=f"Error during enrich friends: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcFbSpecs.friends_spec
            if response_body:
                mapped_following = glom(response_body, spec)
                mapped.extend(mapped_following)
                end_cursor = response_body.get(
                    "page_info", {}).get("end_cursor")
                has_next_page = response_body.get(
                    "page_info", {}).get("has_next_page", False)
                if not end_cursor or not has_next_page:
                    has_next_page = False
                    break

        try:
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="ResultAPIReducer",
                search_step="enrich",
                message=(f"Found {len(mapped)} uploaded media"),
                docs_count=len(mapped),
                step_point="processing",
            )
        except Exception as e:
            logger.error(f"Unable to send service log: {str(e)}")

        return {"connections":
                {"friends":
                 {"facebook": mapped}}} if mapped else None

    async def _enrich_places_lived(
        self, doc: EnrichRequestDoc
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id

        try:
            response = await api.async_profiles.about_tabs_places_lived(
                profile_id)
            response_body = response.body
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="FacebookAPI",
                search_step="enrich",
                message=f"Error during enrich places lived: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return

        spec = VtrcFbSpecs.about_tabs_places_lived_spec
        mapped = glom(response_body, spec, default=[])

        return (
            {
                "personal_details": {
                    "location": {"places_lived": {"fb_places_lived": mapped}}
                }
            }
            if mapped
            else None
        )

    async def _enrich_pages_liked(
        self, doc: EnrichRequestDoc,
        limit: int = 100
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id

        mapped = []
        end_cursor = None
        has_next_page = True
        while (has_next_page and
               len(mapped) < limit):
            try:
                body = None
                if end_cursor:
                    body = {"end_cursor": end_cursor}
                response = await api.async_profiles.pages_liked(
                    profile_id,
                    body=body)
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="FacebookAPI",
                    search_step="enrich",
                    message=f"Error during enrich pages liked: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcFbSpecs.liked_pages_spec
            if response_body:
                # NOTE: response could be empty
                if mapped_following := glom(response_body, spec):
                    mapped.extend(mapped_following)
                response_body = dotty(response_body)
                page_info = response_body.get(
                    "pagination", {})
                end_cursor = None
                has_next_page = None
                if page_info and isinstance(page_info, dict):
                    end_cursor = page_info.get("end_cursor")
                    has_next_page = page_info.get("has_next_page",
                                                  False)
                if not has_next_page:
                    break
                elif (not end_cursor
                      or not has_next_page
                        or len(mapped) > limit):
                    if len(mapped) > limit:
                        mapped = mapped[:limit]
                    has_next_page = False
                    break

        return {"interests": {"pages": mapped}} if mapped else None

    async def _enrich_following(
        self, doc: EnrichRequestDoc, limit: int = 100
    ) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id

        mapped = []
        end_cursor = None
        has_next_page = True
        while (has_next_page and
               len(mapped) < limit):
            try:
                body = None
                if end_cursor:
                    body = {"end_cursor": end_cursor}
                response = await api.async_profiles.following(
                    profile_id,
                    body=body)
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="FacebookAPI",
                    search_step="enrich",
                    message=f"Error during enrich following: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcFbSpecs.following_spec
            if response_body:
                mapped_following = glom(response_body, spec)
                mapped.extend(mapped_following)
                end_cursor = response_body.get(
                    "page_info", {}).get("end_cursor")
                has_next_page = response_body.get(
                    "page_info", {}).get(
                    "has_next_page", False)
                if not end_cursor or not has_next_page:
                    has_next_page = False
                    break

        return {"connections":
                {"following":
                 {"facebook": mapped}}} if mapped else None

    """
    async def _enrich_timeline(
            self,
            doc: EnrichRequestDoc) -> List[FacebookEnrichDoc]:
        profile_id = doc.source_id
        docs = []

        try:
            response = await api.async_profiles.timeline(
                profile_id
            )
            response_body = response.body
        except Exception as e:
            print(str(e))
            return docs

        user_data = response_body.get("data").get("user")
        if (photo_dict := user_data.get("profile_photo")) is not None:
            hd_profile_pic = photo_dict.get("image").get("uri")
        else:
            hd_profile_pic = None

        data = {}
        personal_details = {
            "visuals": {
                "profile_photo": {
                    "facebook_profile_picture": hd_profile_pic
                }
            }
        }
        data["personal_details"] = personal_details
        data["urn"] = doc.urn

        _doc = FacebookEnrichDoc(**data)
        docs.append(_doc)

        return docs
    """
