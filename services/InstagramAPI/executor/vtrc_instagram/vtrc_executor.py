import uuid
from typing import List, Dict
from glom import glom
from mergedeep import merge

from core.documents import (
    SearchRequestDoc,
    SearchResponseDoc,
    EnrichRequestDoc,
    EnrichResponseDoc
)
from core.models.utils import post_service_log
from core.clients.vetric.instagram import api, VtrcIgSpecs

from ..config import settings


class VetricInstagramAPI():

    resource = "vetric"

    async def search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        docs = []
        params = {"q": doc.query}
        try:
            response = await api.async_user.search(
                params=params
            )
            response_body = response.body
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="InstagramAPI",
                search_step="search",
                message=f"Error during search: {str(e)}",
                docs_count=len(docs),
                step_point="error"
            )
            return docs

        spec = VtrcIgSpecs.search_spec

        mapped_response = glom(response_body, spec)
        for result in mapped_response:

            data = {
                "personal_details": {
                    "name": {
                        "first_name": {"f_name": doc.f_name},
                        "last_name": {"l_name": doc.l_name},
                        "full_name": {
                            "full_name": doc.name,
                            "instagram_full_name":
                            result.get("instagram_full_name")}
                    },
                    "email": {
                        "email_address": ([doc.email_address] if
                                          doc.email_address else None)
                    },
                    "visuals": {
                        "profile_photo": {
                            "profile_picture": result.get(
                                "instagram_ld_profile_picture"),
                            "instagram_profile_picture": result.get(
                                "instagram_ld_profile_picture")
                        }
                    }
                },
                "network_signature": {
                    "user_id": {
                        "instagram_user_id":
                            result.get("instagram_user_id")},
                    "username": {
                            "instagram_username":
                            result.get("instagram_username")},
                        "misc": {
                            "instagram_is_private":
                            result.get("instagram_is_private")}
                },
                "urn": doc.urn,
                "source": "instagram",
                "resource": self.resource,
                "search_id": doc.search_id
            }

            _doc = SearchResponseDoc(**data)
            docs.append(_doc)

        return docs

    async def enrich(self,
                     doc: EnrichRequestDoc) -> EnrichResponseDoc | None:
        data = {}
        if enriched_info := await self._enrich_info(doc):
            data = merge(data, enriched_info)

        if enriched_usernameinfo := await self._enrich_usernameinfo(doc):
            data = merge(data, enriched_usernameinfo)

        if enriched_feed := await self._enrich_feed(
                doc,
                limit=settings.VETRIC_INSTAGRAM_API_CANDIDATE_POSTS_LIMIT):
            data = merge(data, enriched_feed)

        if enriched_following := await self._enrich_following(
                doc,
                limit=settings.VETRIC_INSTAGRAM_API_CANDIDATE_FOLLOWING_LIMIT):
            data = merge(data, enriched_following)

        if enriched_followers := await self._enrich_followers(
                doc,
                limit=settings.VETRIC_INSTAGRAM_API_CANDIDATE_FOLLOWERS_LIMIT):
            data = merge(data, enriched_followers)

        if data:
            data['source'] = "instagram"
            data['urn'] = doc.urn
            data['search_id'] = doc.search_id
        return EnrichResponseDoc(**data) if data else None

    async def _enrich_info(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        profile_id = doc.source_id
        try:
            response = await api.async_user.info(
                format(int(profile_id))
            )
            response_body = response.body
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="InstagramAPI",
                search_step="enrich",
                message=f"Error during enrich info: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return

        spec = VtrcIgSpecs.info_spec
        mapped = glom(response_body, spec, default={})

        return mapped if mapped else None

    async def _enrich_feed(
            self,
            doc: EnrichRequestDoc,
            limit: int = 100) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        mapped = []
        max_id = None
        has_next_page = True
        while (has_next_page and
                len(mapped) < limit):
            try:
                response = await api.async_user.feed(
                    format(int(profile_id), params={"max_id": max_id})
                )
                response_body = response.body
            except Exception as e:
                print(str(e))
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="InstagramAPI",
                    search_step="enrich",
                    message=f"Error during enrich feed: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                has_next_page = False
                return

            spec = VtrcIgSpecs.feed_spec
            if response_body:
                mapped_feed = glom(response_body, spec)
                mapped.extend(mapped_feed)
                max_id = response_body.get(
                    "next_max_id") or response_body.get(
                    "pagination", {}).get("cursor")
                has_more = response_body.get(
                    "pagination", {}).get("has_more")
                if not max_id or not has_more:
                    has_next_page = False
                    break

        return {"posts": mapped} if mapped else None

    async def _enrich_following(
            self,
            doc: EnrichRequestDoc,
            limit: int = 100) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        rank_token = uuid.uuid4()
        mapped = []
        max_id = None
        has_next_page = True
        while (has_next_page and
               len(mapped) < limit):
            try:
                response = await api.async_user.following(
                    format(int(profile_id)), params={"rank_token": rank_token,
                                                     "max_id": max_id,
                                                     "cursor": max_id}
                )
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="InstagramAPI",
                    search_step="enrich",
                    message=f"Error during enrich following: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcIgSpecs.following_spec
            if response_body:
                mapped_following = glom(response_body, spec)
                mapped.extend(mapped_following)
                max_id = (response_body.get(
                    "next_max_id") or response_body.get(
                    "pagination", {}).get("cursor"))
                has_more = (response_body.get(
                    "pagination", {}).get("has_more") or
                    response_body.get("has_more"))
                if not max_id or not has_more:
                    has_next_page = False
                    break

        return {"connections":
                {"following":
                 {"instagram": mapped}}} if mapped else None

    async def _enrich_followers(
            self,
            doc: EnrichRequestDoc,
            limit: int = 100) -> List[EnrichResponseDoc]:
        profile_id = doc.source_id
        mapped = []
        cursor = None
        has_next_page = True
        while (has_next_page and
               len(mapped) < limit):
            try:
                response = await api.async_user.followers(
                    format(int(profile_id)), params={"cursor": cursor,
                                                     "max_id": cursor}
                )
                response_body = response.body
            except Exception as e:
                response_body = None
                post_service_log(
                    search_id=doc.search_id,
                    urn=doc.urn,
                    executor="InstagramAPI",
                    search_step="enrich",
                    message=f"Error during enrich followers: {str(e)}",
                    docs_count=1,
                    step_point="error"
                )
                print(str(e))
                has_next_page = False

            spec = VtrcIgSpecs.followers_spec
            if response_body:
                mapped_followers = glom(response_body, spec)
                mapped.extend(mapped_followers)
                has_more = (response_body.get(
                    "pagination", {}).get("has_more") or
                    response_body.get("has_more"))
                cursor = response_body.get(
                    "pagination", {}).get("cursor") or response_body.get(
                    "max_id")
                if not has_more:
                    has_next_page = False
                    break

        return {"connections":
                {"followers":
                 {"instagram": mapped}}} if mapped else None

    async def _enrich_usernameinfo(
            self,
            doc: EnrichRequestDoc) -> Dict | None:
        username = doc.username
        if not username:
            return None
        if isinstance(username, list):
            username = next((u for u in username if u), None)

        try:
            response = await api.async_user.usernameinfo(
                username
            )
            response_body = response.body
        except Exception as e:
            print(str(e))
            post_service_log(
                search_id=doc.search_id,
                urn=doc.urn,
                executor="InstagramAPI",
                search_step="enrich",
                message=f"Error during enrich username info: {str(e)}",
                docs_count=1,
                step_point="error"
            )
            return

        hd_profile_pic = (
            response_body.get("user", {}).
            get("hd_profile_pic_url_info", {}).get("url"))
        personal_details = None
        if hd_profile_pic:
            personal_details = {
                "visuals": {
                    "profile_photo": {
                        "instagram_profile_picture": hd_profile_pic
                    }
                }
            }
        else:
            hd_profile_pic = None

        return ({"personal_details": personal_details}
                if personal_details else None)
