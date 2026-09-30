from glom import glom
from pydantic import AnyHttpUrl

from core.clients.vetric.instagram import api as instagram_api, VtrcIgSpecs
from core.clients.vetric.facebook import api as facebook_api, VtrcFbSpecs
from core.dotty_dictionary import dotty
from core.utils.instagram_username import extract_instagram_username


async def enrich_connection_info(connection_data):
    connection_url = connection_data.connection_url
    connection_platform = connection_data.connection_platform
    connection_username = connection_data.connection_username
    if connection_url and not connection_platform:
        connection_platform = connection_url.host.split('.')[1].lower()
    if connection_platform.lower() == 'instagram':
        try:
            connection_info = await _enrich_instagram_connection(
                connection_url=connection_url,
                username=connection_username)
            return (connection_platform, connection_info)
        except Exception as e:
            print(f"Error retrieving Instagram connection info: {e}")
    elif connection_platform.lower() == 'facebook':
        try:
            connection_info = await _enrich_facebook_connection(
                connection_url=connection_url,
                username=connection_username)
            return (connection_platform, connection_info)
        except Exception as e:
            print(f"Error retrieving Facebook connection info: {e}")


async def _enrich_facebook_connection(connection_url: AnyHttpUrl = None,
                                      username: str = None):
    if not connection_url and username:
        connection_url = f"https://facebook.com/{username}"

    res = await facebook_api.async_general.resolve_url(
        params={"url": str(connection_url)})
    res_body = res.body
    spec = VtrcFbSpecs.url_resolver_spec
    mapped = glom(res_body, spec, default={})
    source_id = mapped.get("id")
    timeline_res = await facebook_api.async_profiles.timeline(
        source_id)
    timeline_body = timeline_res.body
    timeline_spec = VtrcFbSpecs.timeline_specs
    timeline_mapped = glom(timeline_body, timeline_spec, default=[])

    return {
        "facebook_full_name": timeline_mapped.get("facebook_full_name"),
        "facebook_user_id": source_id,
        "facebook_profile_url": str(connection_url),
        "facebook_profile_picture": timeline_mapped.get("profile_picture"),
    }


async def _enrich_instagram_connection(connection_url: AnyHttpUrl = None,
                                       username: str = None):
    if connection_url and not username:
        username = extract_instagram_username(str(connection_url))
        if not username:
            return

    res = await instagram_api.async_user.usernameinfo(
        username)
    res_body = res.body
    spec = VtrcIgSpecs.usernameinfo_spec
    username_mapped = glom(res_body, spec, default={})
    source_id = username_mapped.get("user_id")
    user_info_res = await instagram_api.async_user.info(format(int(source_id)))
    user_info_body = user_info_res.body
    user_info_spec = VtrcIgSpecs.info_spec
    user_info_mapped = glom(user_info_body, user_info_spec, default={})
    user_info_mapped = dotty(user_info_mapped)

    return {
        "instagram_user_id": source_id,
        "instagram_username": username,
        "instagram_full_name": username_mapped.get("full_name"),
        "instagram_profile_picture": username_mapped.get("profile_pic_url"),
        "instagram_is_private": user_info_mapped.get(
            "network_signature.misc.instagram_is_private"),
        "instagram_is_verified": user_info_mapped.get(
            "network_signature.misc.instagram_is_verified")
    }
