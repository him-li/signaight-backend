from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class IntroVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_with_intro(self):
        if bio_details := self.person.biographic_details:
            if bio_intro := bio_details.description_bio_intro:
                if bio_intro.instagram_bio:
                    return True
                if twitter_desc := bio_intro.twitter_description:
                    if (twitter_desc.description_text or
                        twitter_desc.description_symbols or
                            twitter_desc.description_hashtags):
                        return True
                if fb_intro := bio_intro.fb_profile_intro:
                    if fb_intro.fb_profile_intro_text:
                        return True
                if bio_intro.xing_profile_about_me:
                    return True
                if bio_intro.google_bio:
                    return True

        return False
