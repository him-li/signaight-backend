from typing import List
from glom import glom
from core.clients.vetric.facebook import api, VtrcFbSpecs
from core.documents.base import EnrichResponseDoc


async def enrich_timeline(
            candidate_id
    ) -> List[EnrichResponseDoc]:
    person_id = candidate_id
    mapped = {}
    try:
        response = await api.async_profiles.timeline(
               person_id)
        response_body = response.body
        timeline_specs = VtrcFbSpecs.timeline_specs
        timeline_mapped = glom(response_body, timeline_specs)
        if timeline_mapped:
            full_name = timeline_mapped.get("facebook_full_name")

            first_name = None
            last_name = None

            if isinstance(full_name, str):
                parts = full_name.strip().split()
                if len(parts) == 1:
                    first_name = parts[0]
                elif len(parts) >= 2:
                    first_name = parts[0]
                    last_name = " ".join(parts[1:])
            big_facebook_picture = timeline_mapped.get(
                    "profile_picture")
            mapped = {
                "personal_details": {
                    "visuals": {
                        "profile_photo": {
                            "facebook_profile_picture": big_facebook_picture
                        },
                        "fb_cover_photo": timeline_mapped.get("facebook_cover_photo"),
                    },
                    "name": {
                        "full_name": {"facebook_full_name": full_name},
                        "first_name": {"facebook_f_name": first_name},
                        "last_name": {"facebook_l_name": last_name},
                    },
                    "gender":{
                        "fb_gender": timeline_mapped.get("facebook_gender")
                    }
                    
                },
                "network_signature": {
                    "username" : {
                        "facebook_username": timeline_mapped.get("facebook_username")
                    },
                    "url" :{
                        "facebook_profile_url": timeline_mapped.get("facebook_profile_url")
                    },
                    "user_id" :{
                        "facebook_user_id": timeline_mapped.get("profile_id")
                    },
                    "online_signature": {
                        "fb_followers_count": timeline_mapped.get("followers"),
                        "fb_friends_count": timeline_mapped.get("friends"),
                        "fb_following_count": timeline_mapped.get("following")
                    }
                }
            }
            if timeline_mapped.get("fb_profile_intro"):
                mapped["biographic_details"] = {
                        "description_bio_intro": {
                            "fb_profile_intro": timeline_mapped.get(
                                "fb_profile_intro"
                            )
                        }
                    }
        return mapped

    except Exception as e:
        print(str(e))
        return None
