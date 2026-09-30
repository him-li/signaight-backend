from typing import List, Dict

from services.FacebookAPI.executor import FacebookAPI
from services.InstagramAPI.executor import InstagramAPI
from services.LinkedinAPI.executor import LinkedinAPI


def build_executors_list(sources_resouces: List[Dict],
                         executors_needs="searchIn",
                         flow_step="search"):
    executors_list = []

    executors = {
        "facebook_vetric": {
            "name": "facebookAPIVetric_" + flow_step,
            "uses": FacebookAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "vtrc_facebook",
                               "flow_step": flow_step},
        },
        "facebook_social_links": {
            "name": "facebookAPISocialLinks_" + flow_step,
            "uses": FacebookAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "slinks_facebook",
                               "flow_step": flow_step},
        },
        "instagram_vetric": {
            "name": "instagramAPIVetric_" + flow_step,
            "uses": InstagramAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "vtrc_instagram",
                               "flow_step": flow_step},
        },
        "instagram_social_links": {
            "name": "instagramAPISocialLinks_" + flow_step,
            "uses": InstagramAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "slinks_instagram",
                               "flow_step": flow_step},
        },
        "linkedin_vetric": {
            "name": "linkedinAPIVetric_" + flow_step,
            "uses": LinkedinAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "vtrc_linkedin",
                               "flow_step": flow_step},
        },
        "linkedin_social_links_name": {
            "name": "linkedinAPISocialLinks_" + flow_step,
            "uses": LinkedinAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "slinks_linkedin_name",
                               "flow_step": flow_step},
        },
        "linkedin_social_links_email": {
            "name": "linkedinAPISocialLinks_" + flow_step,
            "uses": LinkedinAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "slinks_linkedin_email",
                               "flow_step": flow_step},
        },
        "linkedin_social_links_emailV2": {
            "name": "linkedinAPISocialLinks_" + flow_step,
            "uses": LinkedinAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "slinks_linkedin_emailV2",
                               "flow_step": flow_step},
        },
        "linkedin_epieos": {
            "name": "linkedinAPIEpieos_" + flow_step,
            "uses": LinkedinAPI,
            "needs": executors_needs,
            "uvicorn_kwargs": {"name": "epieos_linkedin",
                               "flow_step": flow_step},
        },
    }
    for source_resource in sources_resouces:
        source = source_resource.get("source")
        resource = source_resource.get("resource")
        executors_key = source + "_" + resource
        executor_value = executors.get(executors_key)
        executors_list.append(executor_value)

    return executors_list
