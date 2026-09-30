import copy
import collections
# import uuid
from typing import List, Dict, Optional  # , Union
from datetime import date

from core.documents import SearchRequestDoc, EnrichRequestDoc
from core.logging import logger
from core.clients.mapbox.client import api as mapbox_api
from core.utils.normalize_list import normalize_to_list
from .urn import build_urn


def build_search_docarray(
    name: str,
    person_id: str,
    sources_resources: List[Dict],
    search_id: str,
    f_name: str,
    l_name: str,
    email_address: str,
    options={},
):
    docs = []
    for source_resource in sources_resources:
        doc = SearchRequestDoc(
            name=name,
            urn=build_urn("persons", str(person_id)),
            source=source_resource["source"],
            resource=source_resource["resource"],
            search_id=search_id,
            f_name=f_name,
            l_name=l_name,
            email_address=email_address,
        )
        if city := format(str(options.get("city"))):
            doc.city = city
        if education := format(str(options.get("education"))):
            doc.education = education
        if work := format(str(options.get("work"))):
            doc.work = work
        docs.append(doc)
    return docs


def build_enrich_docarray(
    person_id: str,
    source_ids: Dict,
    sources_resources: List[Dict],
    sources_usernames: Optional[Dict],
    person_candidate: str,
):
    docs = []
    for source_resource in sources_resources:
        source_id = source_ids.get(source_resource["source"])
        source_username = sources_usernames.get(source_resource["source"])
        if source_id is not None:
            doc = EnrichRequestDoc(
                urn=build_urn(str(person_candidate), str(person_id)),
                source_id=source_id,
                resource=source_resource.get("resource"),
                source=source_resource.get("source"),
                username=source_username
            )
            docs.append(doc)
    return docs


def update_nested_dict(d, u):
    if d is None:
        d = {}
    d_copy = copy.deepcopy(d)
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d_copy[k] = update_nested_dict(d_copy.get(k, {}), v)
        elif isinstance(v, list):
            if k in d_copy and d_copy[k]:
                d_copy[k].extend([i for i in v if i not in d_copy[k]])
            else:
                d_copy[k] = v
        else:
            if k not in d_copy or d_copy[k] is None:
                d_copy[k] = v
            elif d_copy[k] is not v and v:
                d_copy[k] = v
    return d_copy


PLATFORMS = ["facebook", "instagram", "linkedin", "twitter", "xing"]


def build_source_ids_dict(person):
    result = {}

    ns = getattr(person, "network_signature", None)
    if not ns:
        return result

    for platform in PLATFORMS:
        values = []

        matched = getattr(ns, "matched_profiles", None)
        if matched:
            platform_match = getattr(matched, platform, None)
            primary = getattr(platform_match, "primary_candidate", None) or {}

            for candidate_data in primary.values():
                values.extend(
                    normalize_to_list(
                        getattr(candidate_data, "profile_id", None)
                    )
                )

        if values:
            result[platform] = list(set(values))

    return result


def build_usernames_dict(person):
    result = {}

    ns = getattr(person, "network_signature", None)
    if not ns:
        return result

    for platform in PLATFORMS:
        values = []

        matched = getattr(ns, "matched_profiles", None)
        if matched:
            platform_match = getattr(matched, platform, None)
            primary = getattr(platform_match, "primary_candidate", None) or {}

            for candidate_data in primary.values():
                values.extend(
                    normalize_to_list(
                        getattr(candidate_data, "profile_username", None)
                    )
                )

        if values:
            result[platform] = list(set(values))

    return result


def build_profile_urls_dict(person):
    result = {}

    ns = getattr(person, "network_signature", None)
    if not ns:
        return result

    for platform in PLATFORMS:
        values = []

        matched = getattr(ns, "matched_profiles", None)
        if matched:
            platform_match = getattr(matched, platform, None)
            primary = getattr(platform_match, "primary_candidate", None) or {}

            for candidate_data in primary.values():
                values.extend(
                    normalize_to_list(
                        getattr(candidate_data, "profile_url", None)
                    )
                )

        if values:
            result[platform] = list(set(map(str, values)))

    return result


def build_sources_resources_list(flow_names, get_flow_collection):
    sources_resources = []
    for flow_name in flow_names:
        flow_source = get_flow_collection(flow_name)[0]
        flow_resource = get_flow_collection(flow_name)[1]
        source_resource = {"source": flow_source, "resource": flow_resource}
        sources_resources.append(source_resource)

    return sources_resources


def http_request_retries(api_path, max_attempts=1, *args, **kwargs):
    resp_body = None
    attempt = 0
    while resp_body is None and attempt < max_attempts:
        attempt += 1
        try:
            response = api_path(*args, **kwargs)
            resp_body = response.body
            return resp_body
        except Exception as e:
            logger.info(e)


def parse_vtrc_li_period(period):

    if year_to := period.get("date_to", {}).get("year"):
        year_to = int(year_to)
        if month_to := period.get("date_to", {}).get("month", 1):
            month_to = int(month_to)
            period["date_to"] = date(year_to, month_to, 1).strftime("%Y-%m-%d")
        else:
            period["date_to"] = date(year_to, 1, 1).strftime("%Y-%m-%d")
    else:
        period["date_to"] = "Present"

    if year_from := period.get("date_from", {}).get("year"):
        year_from = int(year_from)
        if month_from := period.get("date_from", {}).get("month", 1):
            month_from = int(month_from)
            period["date_from"] = date(
                year_from, month_from, 1).strftime("%Y-%m-%d")
        else:
            period["date_from"] = date(year_from, 1, 1).strftime("%Y-%m-%d")
    else:
        period["date_from"] = None
    return period


def check_location_in_country(country, location):
    response = mapbox_api.search.mapbox(location)
    response_body = response.body
    try:
        context = response_body.get('features', [])[0].get(
            'context', [])
    except Exception:
        return False
    for item in context:
        if ("country" in item.get("id", "")
                and item.get("short_code", "").lower(
        ) == country.lower()):
            return True
    return False


def check_position_location_in_country(country, position):
    query = []
    if position.location:
        query.append(position.location)
    if query:
        if check_location_in_country(country, query):
            return True
    return False


def transform_user_info(user_info: Dict):
    user_info = {
        "id": user_info.get("sub"),
        "email": user_info.get("email"),
        "firstname": user_info.get("fields").get("firstname", ""),
        "lastname": user_info.get("fields").get("lastname", ""),
    }
    return user_info
