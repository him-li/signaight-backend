import asyncio
import json
import hashlib
from core.utils.image_utils import get_image_quality_cached
from core.utils.urn import build_person_urn
import httpx
import redis.asyncio as async_redis
from asyncio import sleep
from glom import glom
from pathlib import Path
from slugify import slugify
from typing import List

from core.clients.grayfox import (api, GrfxSpecs, active_search_api)
from core.config import settings
from core.documents import (
    SearchResponseDoc,
    SearchRequestDoc,
    ActiveSearchRequestDoc,
    ActiveSearchResponseDoc,
)
from core.clients.grayfox.slack_notification import notify_slack
from core.dotty_dictionary import dotty
from core.logging import logger
from core.utils import clean_dict
from core.redis import get_redis_client
from core.config import settings


async_redis_client = get_redis_client(async_mode=True)

class GrayfoxAPI():

    async def search(
            self,
            doc: SearchRequestDoc
    ) -> List[SearchResponseDoc]:
        docs = []
        if doc.email_address:
            query_type = 'email'
            query_value = doc.email_address
        elif doc.phone_number:
            query_type = 'phone'
            query_value = doc.phone_number
        else:
            return docs

        if settings.ENVIRONMENT in ['local', 'testing']:
            logger.debug("Grayfox working inmode with local data only!!!")
            match query_type:
                case "email":
                    filename = slugify(query_value, separator="_",
                                       replacements=[['@', ' at ']])
                case "phone":
                    filename = slugify(query_value, separator="_",
                                       replacements=[['+', '']])
                case _:
                    return docs
            client_dir = Path(__file__).parent
            json_path = client_dir / "data" / f'{filename}.json'
            if json_path.exists() and json_path.is_file():
                with open(json_path, 'r', encoding='utf-8') as f:
                    response_body = json.load(f)
            else:
                return docs
        else:
            data = {"type": query_type, "query": query_value}

            '''
            # DEPRECATION: our standard REST client with caching has been
            # replaced for custom httpx client with manual caching due cached
            # empty data responses from grayfox with status 200
            try:
                response = await api.async_search.submit(data=data)
                response_body = response.body
                try:
                    credits = response_body.get("credits", 0)
                    notify_slack("search", "submit", data, credits)
                except Exception as e:
                    logger.error(f"Error notifying slack: {str(e)}")
            except Exception as e:
                logger.info(str(e))
                return docs
            for _ in range(10):
                try:
                    response = await api.async_search.get(params=data)
                    response_body = response.body
                    profiles = response_body.get("data", {})
                    if profiles:
                        break
                    else:
                        await sleep(60)
            '''

            data_key_base = ("external-apis-cache:{}:"
                        "https://eye-6adaad69fa3d.profileintel.com/api:{}")
            data_key_hash = hashlib.sha256(
                            json.dumps(data).encode()).hexdigest()
            try:
                # Check cache for data presence
                if response_body := await async_redis_client.get(
                                data_key_base.format('POST', data_key_hash)):
                    # Notifying slack about cached data, no real request needed
                    # f****g API provider will cry cause get less money from us.
                    # Mazal tov!
                    notify_slack("search", "submit", data, None)
                else:
                    # Now we are sad, cause a lost of some money,
                    # but thats ok, cause new person in search
                    logger.info("Make request to grayfox for data request")
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            'https://eye-6adaad69fa3d.profileintel.com/api',
                            headers={'x-api-key': settings.GRAYFOX_API_KEY},
                            data=data
                        )
                    # If not 200 something get wrong
                    if response.status_code not in [200,201]:
                        logger.error("Unable submit search request to grayfox")
                        return docs
                    response_body = response.json()
                    # saving response into cache
                    await async_redis_client.set(
                        data_key_base.format('POST', data_key_hash),
                        json.dumps(response_body),
                        ex=864000000000 # cache for 100 days
                    )
                    # Make our financial managers cry on bills
                    try:
                        credits = response_body.get("credits", 0)
                        notify_slack("search", "submit", data, credits)
                    except Exception as e:
                        logger.error(f"Error notifying slack: {str(e)}")

                # OK lets go and get some real data but from cache first
                if response_body := await async_redis_client.get(
                                data_key_base.format('GET', data_key_hash)):
                    response_body = json.loads(response_body.decode())
                else:
                    # API provider has no smart app architect and we can detect
                    # success only checking payload which always came ...
                    # Tadaaaa!!! with status 200 if http sequence
                    #  request/response made without errors
                    # Dig! Dig! Dig!
                    for _ in range(10):
                        logger.info("Make request to grayfox for data")
                        async with httpx.AsyncClient() as client:
                            response = await client.get(
                                'https://eye-6adaad69fa3d.profileintel.com/api',
                                headers={'x-api-key': settings.GRAYFOX_API_KEY},
                                params=data
                            )
                        if response.status_code not in [200,201]:
                            logger.error("Unable submit search "
                                                "request to grayfox")
                            return docs
                        response_body = response.json()
                        # checking for proper payload
                        if response_body.get("data"):
                            print(f"grabbed: {response_body}")
                            await async_redis_client.set(
                                data_key_base.format('GET', data_key_hash),
                                json.dumps(response_body),
                                ex=864000000000 # cache for 100 days
                            )
                            break
                        else:
                            # No luck! wait 60 seconds for another try
                            await sleep(60)
            except Exception as e:
                logger.error(str(e))
                return docs


        try:
            spec = GrfxSpecs.get_request_details_spec
            mapped_results = glom(response_body, spec)

            for result in mapped_results.values():
                if result and isinstance(result, dict):
                    result = clean_dict(result)
                    if len(result.keys()) == 1:
                        continue
                    result = dotty(result)
                    if (result.get("source") == 'facebook' and
                            not result.get("network_signature")):
                        result['source'] = 'facebook_grfx'
                    elif (result.get("source") == 'facebook_entity' or
                          result.get("source") == 'facebook_phone_user_id_mix' or
                          result.get("source") == 'mindjolt'
                          ):
                        result['source'] = 'facebook'
                    associated, discovery = result.get('personal_details.phone.grfx_phones', (None, None))
                    if doc.phone_number:
                        associated = [
                            phone for phone in associated
                            if phone != doc.phone_number
                        ] if associated else None
                        discovery = [
                            phone for phone in discovery
                            if phone != doc.phone_number
                        ] if discovery else None
                    associated_emails = result.get('personal_details.email.associated_email') or None
                    if doc.email_address:
                        associated_emails = [
                            email for email in associated_emails
                            if email != doc.email_address
                        ] if associated_emails else None
                    result.setdefault(
                        "personal_details.email.associated_email", associated_emails)
                    result.setdefault(
                        "personal_details.phone.associated_phones", associated)
                    result.setdefault(
                        "personal_details.phone.discovery_phones", discovery)
                    result.setdefault(
                        "personal_details.name.first_name.f_name", doc.f_name)
                    result.setdefault(
                        "personal_details.name.last_name.l_name", doc.l_name)
                    result.setdefault(
                        "personal_details.name.full_name.full_name", doc.name)
                    images = result.get('personal_details.grfx_images', None)
                    if images:
                        destinations = [picture for picture in images if picture]
                        data = {
                            "destination": [str(p) for p in destinations] 
                        }
                        try:
                            logger.info(f"Image quality for unmapped images {data}")
                            response = await get_image_quality_cached(
                                data,
                                headers={
                                    'x-remote-context': build_person_urn(doc.search_id)
                                }
                            )
                            logger.info(response)
                            sorted_pics_by_quality = sorted(
                                response.items(),
                                key=lambda x: (
                                    x[1].get('scores', {}).get('face_score', -1),
                                    x[1].get('scores', {}).get('artifact_score', -1)
                                ),
                                reverse=True
                            )
                            logger.info(sorted_pics_by_quality)
                            images = []
                            for pic, metadata in sorted_pics_by_quality:
                                quality = metadata.get('scores', {}).get('face_score', -1)

                                if pic and quality >= 0.75:
                                    images.append(pic)
                            if images:
                                result.setdefault('personal_details.visuals.unmapped_photos', images)
                            
                        except Exception:
                            logger.error("Error getting image quality")
                    result["resource"] = 'grayfox'
                    result["urn"] = doc.urn
                    result["search_id"] = doc.search_id
                    result = result.to_dict()
                    _doc = SearchResponseDoc(**result)
                    docs.append(_doc)
                elif result and isinstance(result, list):
                    for candidate in result:
                        candidate = clean_dict(candidate)
                        if len(candidate.keys()) == 1:
                            continue
                        candidate = dotty(candidate)
                        if candidate.get("source") == 'facebook':
                            candidate['source'] = 'facebook_grfx'
                        elif candidate.get("source") == 'facebook_entity' or candidate.get("source") == 'mindjolt':
                            candidate['source'] = 'facebook'
                        candidate.setdefault(
                            "personal_details.name.first_name.f_name",
                            doc.f_name)
                        candidate.setdefault(
                            "personal_details.name.last_name.l_name",
                            doc.l_name)
                        candidate.setdefault(
                            "personal_details.name.full_name.full_name",
                            doc.name)
                        associated, discovery = candidate.get('personal_details.phone.grfx_phones', (None, None))
                        associated_emails = result.get('personal_details.email.associated_email') or None
                        if doc.email_address:
                            associated_emails = [
                                email for email in associated_emails
                                if email != doc.email_address
                            ] if associated_emails else None
                        candidate.setdefault(
                            "personal_details.email.associated_email", associated_emails)
                        candidate.setdefault(
                            "personal_details.phone.associated_phones", associated)
                        candidate.setdefault(
                            "personal_details.phone.discovery_phones", discovery)
                        images = candidate.get('personal_details.grfx_images', None)
                        if images:
                            destinations = [picture for picture in images if picture]
                            data = {
                                "destination": [str(p) for p in destinations] 
                            }
                            try:
                                logger.info(f"Image quality for unmapped images {data}")
                                response = await get_image_quality_cached(
                                    data,
                                    headers={
                                        'x-remote-context': build_person_urn(doc.search_id)
                                    }
                                )
                                logger.info(response)
                                sorted_pics_by_quality = sorted(
                                    response.items(),
                                    key=lambda x: (
                                        x[1].get('scores', {}).get('face_score', -1),
                                        x[1].get('scores', {}).get('artifact_score', -1)
                                    ),
                                    reverse=True
                                )
                                logger.info(sorted_pics_by_quality)
                                images = []
                                for pic, metadata in sorted_pics_by_quality:
                                    quality = metadata.get('scores', {}).get('face_score', -1)

                                    if pic and quality >= 0.70:
                                        images.append(pic)
                                if images:
                                    candidate.setdefault('personal_details.visuals.unmapped_photos', images)
                            
                            except Exception:
                                logger.error("Error getting image quality")
                        candidate["resource"] = 'grayfox'
                        candidate["urn"] = doc.urn
                        candidate["search_id"] = doc.search_id
                        candidate = candidate.to_dict()
                        _doc = SearchResponseDoc(**candidate)
                        docs.append(_doc)
        except Exception as e:
            logger.info(e)
            pass
        return docs

    async def active_search(
            self,
            doc: ActiveSearchRequestDoc
    ) -> List[ActiveSearchResponseDoc]:
        docs = []
        if settings.ENVIRONMENT == 'local':
            return docs
        params = {}
        if doc.title:
            params["keywords_title"] = doc.title
        if doc.education:
            params["keywords_school"] = doc.education
        if doc.location:
            params["locations"] = doc.location

        try:
            response = await active_search_api.async_active_search.submit(
                params=params)
            response_body = response.body
        except Exception as e:
            logger.info(str(e))
            return docs
        for _ in range(30):
            try:
                response = await active_search_api.async_active_search.results(
                    params=params)
                response_body = response.body
                profiles = response_body.get("data", {}).get("items", {})
                if profiles:
                    break
                else:
                    await sleep(10)
            except Exception as e:
                logger.info(str(e))
                return docs

        spec = GrfxSpecs.get_active_search_results
        mapped_results = glom(response_body, spec)

        try:
            for result in mapped_results:
                if result:
                    result = clean_dict(result)
                    if len(result.keys()) == 1:
                        continue
                    result = dotty(result)
                    if result.get(
                            "network_signature.url.linkedin_profile_url"):
                        result["resource"] = 'grayfox'
                        result["source"] = 'grayfox_active_search'

                        result["urn"] = doc.urn
                        result["search_id"] = doc.search_id
                        result = result.to_dict()
                        _doc = ActiveSearchResponseDoc(**result)
                        docs.append(_doc)
        except Exception as e:
            logger.info(e)
            pass
        return docs
