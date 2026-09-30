from ..base import PersonBaseActions
from core.rules.person.utils import (
    update_evaluation_factors_weighted_average,
    build_intro_dict,
    build_fb_pages_photo_text_list,
    create_positions_list_additive,
    create_skills_model_list)
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT

from core.clients.ds_app import api as ds_app_api
from core.clients.mapbox.client import api as mapbox_api
from core.logging import logger
from core.utils import build_person_urn


class CuriosityActions(PersonBaseActions):

    @rule_action(params={
        "emoticons": FIELD_SELECT,
        "indicative_terms": FIELD_SELECT,
    })
    def set_person_international_travel_intro(self,
                                              emoticons,
                                              indicative_terms):

        def count_emoticons(text):
            return sum(text.count(emoticon) for emoticon in emoticons if text)

        def count_terms(text):
            return sum(text.count(term) for term in indicative_terms if text)

        emoticons_count = 0
        term_count = 0
        score = 0
        bio_intro = self.person.biographic_details.description_bio_intro

        if bio_intro:
            emoticons_count += count_emoticons(bio_intro.introduction)
            emoticons_count += count_emoticons(bio_intro.instagram_bio)
            emoticons_count += count_emoticons(bio_intro.linkedin_headline)
            if bio_intro.twitter_description:
                emoticons_count += count_emoticons(
                    bio_intro.twitter_description.description_text)
                term_count += count_terms(
                    bio_intro.twitter_description.description_text)
            term_count += count_terms(bio_intro.introduction)
            term_count += count_terms(bio_intro.instagram_bio)
            term_count += count_terms(bio_intro.linkedin_headline)

        if emoticons_count or term_count:
            if emoticons_count > 2:
                score = 8
            if emoticons_count > 3:
                score = 9
            if term_count:
                score += 9
            if score > 10:
                score = 10
            factor = {
                "title": "{} has international travel indicatives".format(
                    self.get_person_name()),
                "score": score,
                "weight": 1
            }
            self.evaluation.curiosity = (
                update_evaluation_factors_weighted_average(
                    self.evaluation.curiosity, factor))

    @rule_action()
    def set_person_international_travel_checkins(self):
        check_ins = None
        try:
            check_ins = (self.person.personal_details.location.
                         check_ins.fb_check_ins)
        except Exception as e:
            logger.info(str(e))
        posts = self.person.posts
        try:
            home_country = (self.person.personal_details.location.
                            current_city_region_country.linkedin_location)
        except Exception:
            home_country = None
        if home_country:
            different_countries = []
            check_ins_abroad = 0
            national_park_checkins = 0
            if check_ins:
                for check_in in check_ins:
                    location = check_in.region
                    context_country = get_location_in_coutry(location)
                    if context_country:
                        context_country = context_country[0]
                        if context_country.lower() != home_country.lower():
                            check_ins_abroad += 1
                            if context_country not in different_countries:
                                different_countries.append(context_country)

                try:
                    check_ins_list = [check_in.model_dump()
                                      for check_in in check_ins]
                    check_ins_req = {'hash': str(
                        check_ins_list), 'checkins': check_ins_list}
                    national_parks_res = (
                        ds_app_api.ds_request.curiosity_international_travels(
                            body=check_ins_req,
                            headers={
                                'x-remote-context':
                                    build_person_urn(self.person.id)
                            }))
                    national_parks_res_body = national_parks_res.body
                    for checkin in national_parks_res_body.get("checkins"):
                        if checkin.get("is_curious"):
                            national_park_checkins += 1
                except Exception:
                    pass

            if posts:
                for post in posts:
                    location = None
                    try:
                        location = (
                            post.instagram_post_location.
                            instagram_location_name)
                    except Exception:
                        pass

                    if location:
                        context_country = get_location_in_coutry(location)
                        if context_country:
                            context_country = context_country[0]
                            if context_country.lower() != home_country.lower():
                                check_ins_abroad += 1
                                if context_country not in different_countries:
                                    different_countries.append(context_country)

                try:
                    posts_list = [
                        {'title': (post.instagram_post_location.
                                   instagram_location_name)}
                        for post in posts if post.instagram_post_location]
                    posts_req = {'hash': str(
                        posts_list), 'checkins': posts_list}
                    posts_national_parks_res = (
                        ds_app_api.ds_request.curiosity_international_travels(
                            body=posts_req,
                            headers={
                                'x-remote-context':
                                    build_person_urn(self.person.id)
                            }
                        ))
                    posts_nat_parks_res_body = posts_national_parks_res.body
                    for post in posts_nat_parks_res_body.get("checkins"):
                        if post.get("is_curious"):
                            national_park_checkins += 1
                except Exception as e:
                    logger.info(str(e))

            abroad_count_score = 0
            if check_ins_abroad > 3:
                abroad_count_score = 4
            if check_ins_abroad >= 5:
                abroad_count_score = 4.5
            if check_ins_abroad >= 6:
                abroad_count_score = 5
            if check_ins_abroad >= 8:
                abroad_count_score = 6

            countries_count = len(different_countries)
            countries_score = 0
            if countries_count >= 3:
                countries_score += 1.5
            if countries_count >= 5:
                countries_score += 2

            score = (abroad_count_score + countries_score +
                     national_park_checkins)

            if score:
                if score > 10:
                    score = 10

                factor = {
                    "title": (
                        "{} has international travel check_ins".format(
                            self.get_person_name())),
                    "score": score,
                    "weight": 1
                }
                self.evaluation.curiosity = (
                    update_evaluation_factors_weighted_average(
                        self.evaluation.curiosity, factor))

    @rule_action()
    def set_has_reading_learning_platforms(self):
        platforms = []
        network_signature = self.person.network_signature

        def check_and_append_platform(candidate, platform_name):
            if candidate and platform_name not in platforms:
                platforms.append(platform_name)

        try:
            m_p = network_signature.matched_profiles

            if m_p.khanacademy:
                check_and_append_platform(
                    m_p.khanacademy.primary_candidate, "khanacademy")
            if m_p.goodreads:
                check_and_append_platform(
                    m_p.goodreads.primary_candidate, "goodreads")
            if m_p.medium:
                check_and_append_platform(
                    m_p.medium.primary_candidate, "medium")
            if m_p.duolingo:
                check_and_append_platform(
                    m_p.duolingo.primary_candidate, "duolingo")
            if m_p.wattpad:
                check_and_append_platform(
                    m_p.wattpad.primary_candidate, "wattpad")
            if m_p.scribd:
                check_and_append_platform(
                    m_p.scribd.primary_candidate, "scribd")
            if m_p.edx:
                check_and_append_platform(
                    m_p.edx.primary_candidate, "edx")
            if m_p.teamtreehouse:
                check_and_append_platform(
                    m_p.teamtreehouse.primary_candidate, "teamtreehouse")
            if m_p.datacamp:
                check_and_append_platform(
                    m_p.datacamp.primary_candidate, "datacamp")
            if m_p.academia:
                check_and_append_platform(
                    m_p.academia.primary_candidate, "academia")
            if m_p.scholar:
                check_and_append_platform(
                    m_p.scholar.primary_candidate, "scholar")
            if m_p.babelio:
                check_and_append_platform(
                    m_p.babelio.primary_candidate, "babelio")
            if m_p.wikipedia:
                check_and_append_platform(
                    m_p.wikipedia.primary_candidate, "wikipedia")
            if m_p.inkitt:
                check_and_append_platform(
                    m_p.inkitt.primary_candidate, "inkitt")

        except Exception:
            pass

        try:
            id = network_signature.user_id

            check_and_append_platform(id.khanacademy_user_id, "khanacademy")
            check_and_append_platform(id.goodreads_user_id, "goodreads")
            check_and_append_platform(id.medium_user_id, "medium")
            check_and_append_platform(id.duolingo_user_id, "duolingo")
            check_and_append_platform(id.wattpad_user_id, "wattpad")
            check_and_append_platform(id.scribd_user_id, "scribd")
            check_and_append_platform(id.edx_user_id, "edx")
            check_and_append_platform(
                id.teamtreehouse_user_id, "teamtreehouse")
            check_and_append_platform(id.datacamp_user_id, "datacamp")
            check_and_append_platform(id.academia_user_id, "academia")
            check_and_append_platform(id.scholar_user_id, "scholar")
            check_and_append_platform(id.babelio_user_id, "babelio")
            check_and_append_platform(id.wikipedia_user_id, "wikipedia")
            check_and_append_platform(id.inkitt_user_id, "inkitt")

        except Exception:
            pass

        try:
            url = network_signature.url

            check_and_append_platform(
                url.khanacademy_profile_url, "khanacademy")
            check_and_append_platform(url.goodreads_profile_url, "goodreads")
            check_and_append_platform(url.duolingo_profile_url, "duolingo")
            check_and_append_platform(url.wattpad_profile_url, "wattpad")
            check_and_append_platform(url.scribd_profile_url, "scribd")
            check_and_append_platform(url.edx_profile_url, "edx")
            check_and_append_platform(
                url.teamtreehouse_profile_url, "teamtreehouse")
            check_and_append_platform(url.datacamp_profile_url, "datacamp")
            check_and_append_platform(url.academia_profile_url, "academia")
            check_and_append_platform(url.scholar_profile_url, "scholar")
            check_and_append_platform(url.babelio_profile_url, "babelio")
            check_and_append_platform(url.wikipedia_profile_url, "wikipedia")
            check_and_append_platform(url.inkitt_profile_url, "inkitt")

        except Exception:
            pass

        if platforms:
            score = 0
            if len(platforms) == 2:
                score = 8
            if len(platforms) == 3:
                score = 9
            if len(platforms) >= 4:
                score = 10

            if score:

                factor = {
                    "title": (
                        "{} has profiles in reading and learning platforms"
                        "".format(
                            self.get_person_name())),
                    "score": score
                }
                self.evaluation.curiosity = (
                    update_evaluation_factors_weighted_average(
                        self.evaluation.curiosity, factor))

    @rule_action()
    def set_person_foodie_intro(self):
        intro_model = self.person.biographic_details.description_bio_intro
        intro_dict = build_intro_dict(intro_model)

        req_body = {
            "hash": str(intro_dict),
            "intro": intro_dict
        }
        try:
            ds_response = ds_app_api.ds_request.foodie_intro(
                body=req_body,
                headers={'x-remote-context': build_person_urn(self.person.id)}
            )
            intro_res = ds_response.body
        except Exception:
            intro_res = {}

        score = 0
        if intro_res:
            response = intro_res.get("intro_response")
            # foodie_keywords = response.get("foodie_keywords")
            indicative_terms_count = response.get("indicative_terms_count")
            foodlover_synonyms_count = response.get("foodlover_synonyms_count")
            # foodie_emojis = response.get("foodie_emojis")
            indicative_emojis_count = response.get("indicative_emojis_count")

            if not indicative_terms_count and indicative_emojis_count:
                if indicative_emojis_count == 1:
                    score = 3
                if indicative_emojis_count == 2:
                    score = 6
                if indicative_emojis_count >= 3:
                    score = 8
            elif indicative_terms_count and not indicative_emojis_count:
                if indicative_terms_count == 1:
                    score = 7
                if indicative_terms_count == 2:
                    score = 9
                if indicative_terms_count >= 3:
                    score = 10
            elif indicative_terms_count and indicative_emojis_count:
                if indicative_terms_count == 1:
                    score = 6
                if indicative_terms_count == 2:
                    score = 8
                if indicative_terms_count >= 3:
                    score = 9
                if indicative_emojis_count:
                    score += 1

            if foodlover_synonyms_count:
                score += 2

        if score:
            if score > 10:
                score = 10

            factor = {
                "title": (
                    "{}'s social media intro/bio indicate interest in"
                    " food culture.".format(
                        self.get_person_name())),
                "score": score
            }
            self.evaluation.curiosity = (
                update_evaluation_factors_weighted_average(
                    self.evaluation.curiosity, factor))

    @rule_action()
    def set_person_foodie_pages(self):
        pages_model = self.person.interests.pages
        pages_list = build_fb_pages_photo_text_list(pages_model)

        req_body = {
            "hash": str(pages_list),
            "pages": pages_list
        }

        try:
            ds_response = ds_app_api.ds_request.foodie_pages(
                body=req_body,
                headers={'x-remote-context': build_person_urn(self.person.id)}
            )
            pages_res = ds_response.body
        except Exception:
            pages_res = []

        foodie_pages_count = 0
        score = 0
        if pages_res and pages_res.get("pages"):
            for page in pages_res.get("pages"):
                if page.get("is_foodie"):
                    foodie_pages_count += 1

        if foodie_pages_count == 2:
            score = 4
        if foodie_pages_count == 3:
            score = 5
        if foodie_pages_count == 4:
            score = 6
        if foodie_pages_count == 5:
            score = 7
        if foodie_pages_count == 6:
            score = 8
        if foodie_pages_count == 7:
            score = 9
        if foodie_pages_count >= 8:
            score = 10

        if score:
            factor = {
                "title": (
                    "{}'s social media pages/groups indicate interest in"
                    " food culture.".format(
                        self.get_person_name())),
                "score": score
            }
            self.evaluation.curiosity = (
                update_evaluation_factors_weighted_average(
                    self.evaluation.curiosity, factor))

    @rule_action()
    def set_person_tuned_curiosity_score(self):
        try:
            linkedin_experience = create_positions_list_additive(self.person)
            linkedin_skills = [skill.name
                               for skill in
                               create_skills_model_list(self.person)]
            try:
                check_ins = ([check_in.model_dump() for check_in in
                              self.person.personal_details.location.
                              check_ins.fb_check_ins])
            except Exception:
                check_ins = []
            try:
                linkedin_courses = [course.course_name for course in
                                    self.person.biographic_details.work.
                                    linkedin_work.courses]
            except Exception:
                linkedin_courses = []

            try:
                current_region = (self.person.personal_details.location.
                                  current_city_region_country.
                                  linkedin_location)
            except Exception:
                current_region = "Unkown"

            req_data = {
                'linkedin_experience': linkedin_experience,
                'linkedin_skills': linkedin_skills,
                'check_ins': check_ins,
                'linkedin_courses': linkedin_courses,
                'current_region': current_region,
            }
            req_body = {'persons': [req_data], "hash": str(req_data)}
            res = ds_app_api.ds_request.curiosity_tuned_score(
                body=req_body)
            res_body = res.body
            for person in res_body.get("scores"):
                score = person.get("score")

            if score:
                score = score / 10
                if score > 10:
                    score = 10
                factor = {
                    "title": (
                        "{} work experience, skills, courses and other data"
                        " show curiosity.".format(
                            self.get_person_name())),
                    "score": score
                }
                self.evaluation.curiosity = (
                    update_evaluation_factors_weighted_average(
                        self.evaluation.curiosity, factor))
        except Exception as e:
            logger.info(e)


def get_location_in_coutry(location):
    try:
        location_res = mapbox_api.search.mapbox(location)
        response_body = location_res.body
        data = response_body.get('features', [])[0]
    except Exception:
        logger.info(
            f'{location} - No matches found in retrive')
        return
    if not data:
        logger.info(
            f'{location} - No matches found in retrive')
        return
    context = data.get("context", [])
    context_country = [context_item.get("text") for
                       context_item in context if
                       "country" in context_item.get("id")]
    if context_country:
        return context_country[0]
