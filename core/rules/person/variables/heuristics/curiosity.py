from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_SELECT

from ..base import PersonBaseVariables


class CuriosityVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has specific emoticons in profiles intro',
        params={
            "emoticons": FIELD_SELECT,
            "indicative_terms": FIELD_SELECT,
        }
    )
    def person_international_travel_intro(self, emoticons, indicative_terms):
        try:
            if not self.person.biographic_details.description_bio_intro:
                return False
        except Exception:
            return False
        attributes_to_check = [
            'introduction',
            'instagram_bio',
            'linkedin_headline',
            'twitter_description.description_text'
        ]

        for attribute in attributes_to_check:
            attr_value = self.person.biographic_details.description_bio_intro
            for attr in attribute.split('.'):
                attr_value = getattr(attr_value, attr, None)
                if attr_value is None:
                    break

            if attr_value and any(emoticon in attr_value for
                                  emoticon in emoticons):
                return True

            if attr_value and any(indicative_term in attr_value for
                                  indicative_term in indicative_terms):
                return True

        return False

    @boolean_rule_variable()
    def person_has_reading_learning_platforms(self):
        try:
            if m_p := (self.person.network_signature.
                       matched_profiles):
                if (
                    (m_p.khanacademy and m_p.khanacademy.primary_candidate) or
                    (m_p.duolingo and m_p.duolingo.primary_candidate) or
                    (m_p.goodreads and m_p.goodreads.primary_candidate) or
                    (m_p.medium and m_p.medium.primary_candidate) or
                        (m_p.wattpad and m_p.wattpad.primary_candidate) or
                        (m_p.scribd and m_p.scribd.primary_candidate) or
                        (m_p.edx and m_p.edx.primary_candidate) or
                        (m_p.teamtreehouse and
                         m_p.teamtreehouse.primary_candidate) or
                        (m_p.datacamp and m_p.datacamp.primary_candidate) or
                        (m_p.academia and m_p.academia.primary_candidate) or
                        (m_p.scholar and m_p.scholar.primary_candidate) or
                        (m_p.babelio and m_p.babelio.primary_candidate) or
                        (m_p.wikipedia and m_p.wikipedia.primary_candidate) or
                        (m_p.inkitt and m_p.inkitt.primary_candidate)):
                    return True
        except Exception:
            pass
        try:
            if id := self.person.network_signature.user_id:
                if (id.duolingo_user_id or
                    id.goodreads_user_id or
                    id.khanacademy_user_id or

                    id.wattpad_user_id or
                    id.scribd_user_id or
                    id.edx_user_id or
                    id.teamtreehouse_user_id or
                    id.datacamp_user_id or
                    id.academia_user_id or
                    id.scholar_user_id or
                    id.babelio_user_id or
                    id.wikipedia_user_id or
                        id.inkitt_user_id):
                    return True
        except Exception:
            pass
        try:
            if url := self.person.network_signature.url:
                if (url.duolingo_profile_url or
                    url.goodreads_profile_url or
                    url.khanacademy_profile_url or
                    url.wattpad_profile_url or
                    url.scribd_profile_url or
                    url.edx_profile_url or
                    url.teamtreehouse_profile_url or
                    url.datacamp_profile_url or
                    url.academia_profile_url or
                    url.scholar_profile_url or
                    url.babelio_profile_url or
                    url.wikipedia_profile_url or
                        url.inkitt_profile_url):
                    return True
        except Exception:
            pass
        return False

    @boolean_rule_variable()
    def person_has_data_for_tuned_curiosity_score(self):
        person = self.person
        try:
            try:
                work = person.biographic_details.work
                try:
                    if work.linkedin_work.positions:
                        return True
                except Exception:
                    pass
                try:
                    if work.linkedin_work.skills:
                        return True
                except Exception:
                    pass
            except Exception:
                pass
            try:
                location = person.personal_details.location
                try:
                    if location.check_ins.fb_check_ins:
                        return True
                except Exception:
                    pass
            except Exception:
                pass

        except Exception:
            pass
        return False
