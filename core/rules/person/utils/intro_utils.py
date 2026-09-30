from core.models.description_bio_intro import DescriptionBioIntro


def build_intro_dict(intro: DescriptionBioIntro):
    intro_dict = intro.model_dump()
    data_dict = {}
    if intro.instagram_bio:
        data_dict.setdefault("instagram_bio", intro_dict.get("instagram_bio"))
    if twitter_desc := intro.twitter_description:
        if twitter_desc.description_text:
            data_dict.setdefault(
                "twitter_description_text",
                intro_dict.get("twitter_description").get("description_text"))
        if twitter_desc.description_symbols:
            data_dict.setdefault(
                "twitter_description_symbols",
                intro_dict.get(
                    "twitter_description").get("description_symbols"))
        if twitter_desc.description_hashtags:
            data_dict.setdefault(
                "twitter_description_hashtags",
                intro_dict.get(
                    "twitter_description").get("description_hashtags"))

    if fb_intro := intro.fb_profile_intro:
        if fb_intro.fb_profile_intro_text:
            data_dict.setdefault("fb_profile_intro",
                                 intro_dict.get("fb_profile_intro_text"))
    if intro.xing_profile_about_me:
        data_dict.setdefault("xing_profile_about_me",
                             intro_dict.get("xing_profile_about_me"))
    if intro.google_bio:
        data_dict.setdefault("google_bio",
                             intro_dict.get("google_bio"))

    return data_dict
