def extract_profile_source(data: dict) -> str:
    """
    Extracts the social network source (e.g. 'instagram', 'facebook')
    from the profile_url key, ignoring non-profile keys like 'verified'.
    """
    url_dict = data.get("network_signature", {}).get("url", {})
    for key in url_dict.keys():
        if key.endswith("_profile_url"):
            return key.split("_")[0]  # e.g. 'instagram', 'facebook'
    return ""
