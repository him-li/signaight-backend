import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT, FIELD_TEXT
from iso639 import Lang
from isocodes import countries

from core.clients.mapbox.client import api as mapbox_api
from core.logging import logger
from core.utils import (check_position_location_in_country,)
from core.rules.person.utils import (update_heuristics_score,
                                     determine_person_lives_in_country,
                                     create_position_model_list_additive)

from ..base import PersonBaseActions


langs = [Lang("en"), Lang("he")]


class StrongAffinityWithCountryActions(PersonBaseActions):

    @rule_action(params=[{'fieldType': FIELD_SELECT,
                          'name': 'country',
                          'label': 'Country of education',
                          'options': [{
                              'label': c.get('name'),
                              'name': c.get('alpha_2')}
                              for c in countries.items]
                          }])
    def set_long_stay_in_country_by_educational_history(self, country):
        if country == "IL":
            heuristic = {
                "title": ("Long stay in Israel - educational "
                          "history/students exchange"),
                "description": ("{} spent a semester of more in Israel as part"
                                " of an academic program").format(
                                    self.get_person_name()),
                "score": 8
            }
            self.alerts.strong_affinity_with_israel = update_heuristics_score(
                self.alerts.strong_affinity_with_israel, heuristic)

    @rule_action(params=[{'fieldType': FIELD_SELECT,
                          'name': 'language',
                          'label': 'Language to set',
                          'options': [{'label': lg.name, 'name': lg.pt1}
                                      for lg in sorted(langs)]
                          }])
    def set_lang_native_seaker(self, language):
        heuristic = {
            "title": "Hebrew Speaker",
            "description": ("{} fluency in Hebrew is an evidence for strong"
                            " affinity with Israel or Israelis").format(
                                self.get_person_name()),
            "score": 6
        }
        grades = {
            "Elementary": 2,
            "Limited": 4,
            "Professional": 6,
            "Full": 8,
            "Native": 10
        }
        try:
            li_languages = self.person.personal_details.languages.li_languages
        except AttributeError:
            li_languages = []
        if not isinstance(li_languages, list):
            return
        for item in li_languages:
            try:
                iso_lang = Lang(item.language)
            except (ValueError, LookupError):
                iso_lang = None
            if not iso_lang:
                continue
            if iso_lang.pt1 == language:
                try:
                    for grade, value in grades.items():
                        if grade in item.proficiency:
                            heuristic['score'] = value
                            break
                except Exception:
                    pass

            self.alerts.strong_affinity_with_israel = update_heuristics_score(
                self.alerts.strong_affinity_with_israel, heuristic)

    @rule_action(params=[{'fieldType': FIELD_SELECT,
                          'name': 'country',
                          'label': 'Headquarter office country',
                          'options': [{
                              'label': c.get('name'),
                              'name': c.get('alpha_2')}
                              for c in countries.items]
                          }])
    def set_company_affiliated_with_country(self, country):
        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return False
        except Exception:
            return False

        scores = 0
        for position in positions:
            if check_position_location_in_country(country, position):
                if position.duration:
                    if position.duration.years:
                        duration = position.duration.years * 12
                    else:
                        duration = 0
                    if position.duration.months:
                        duration += position.duration.months
                date_to = (pendulum.parse(position.period.date_to,
                                          strict=False)
                           if position.period.date_to and not "Present"
                           else pendulum.now())

                timedelta_from_today = pendulum.today().diff(
                    date_to).in_years()
                if position.period.date_from:
                    date_from = pendulum.parse(position.period.date_from,
                                               strict=False)
                    duration = date_to.diff(date_from).in_months()
                else:
                    duration = 25

                if timedelta_from_today > 10:
                    timedelta_multiplier = 0.2
                elif timedelta_from_today > 5:
                    timedelta_multiplier = 0.4
                elif timedelta_from_today > 3:
                    timedelta_multiplier = 0.8
                else:
                    timedelta_multiplier = 1

                if duration > 24:
                    duration_multiple = 10
                elif duration > 6:
                    duration_multiple = 8
                else:
                    duration_multiple = 6

                position_score = timedelta_multiplier * duration_multiple
                scores += position_score
            else:
                pass
        total_scores = scores if scores <= 10 else 10
        country_name = countries.get(alpha_2=country).get("name", country)
        heuristic = {
            "title": "Long Stay in {} - work experience".format(country_name),
            "description": (
                "{person} has work experience in {country_name}".format(
                    person=self.get_person_name(), country_name=country_name)),
            "score": total_scores
        }
        if total_scores:
            if country == "IL":
                (self.alerts
                 .strong_affinity_with_israel) = update_heuristics_score(
                     self.alerts.strong_affinity_with_israel, heuristic)
            elif country == "US":
                self.alerts.strong_affinity_with_usa = update_heuristics_score(
                    self.alerts.strong_affinity_with_usa, heuristic)
        else:
            pass

    @rule_action(
        params={
            'country': FIELD_TEXT
        }
    )
    def set_person_lives_in_country(self, country):
        country_name = countries.get(alpha_2=country).get("name", country)
        person_location = self.person.personal_details.location
        in_country_locations = determine_person_lives_in_country(
            country, person_location)

        if len(in_country_locations) > 0:
            if len(in_country_locations) == 1:
                score = 8
            if len(in_country_locations) >= 2:
                score = 10

            heuristic = {
                "title": (f"Lives in {country_name}"),
                "description": ("{} lives in {country}".format(
                    self.get_person_name(), country=country)),
                "score": score
            }
            self.alerts.strong_affinity_with_israel = update_heuristics_score(
                self.alerts.strong_affinity_with_israel, heuristic)

    @rule_action(
        params={
            'country': FIELD_TEXT
        }
    )
    def set_person_has_checkins_in_country(self, country):
        country_checkins = []
        score = 0
        try:
            country_name = countries.get(alpha_2=country).get("name", country)
            if check_ins := (self.person.personal_details.location.check_ins.
                             fb_check_ins):
                check_ins_region_list = [
                    check_in.region for check_in in check_ins]
                if check_ins_region_list:
                    for region_i, region in enumerate(check_ins_region_list):
                        if country_name in region:
                            country_checkins.append(check_ins[region_i])
                            continue
                        try:
                            resp = mapbox_api.search.mapbox(region)
                            resp_body = resp.body
                            if features := resp_body.get("features"):
                                if isinstance(features, list):
                                    for result_i, result in enumerate(
                                            features):
                                        if result.get("relevance") == 1:
                                            relevant_result = features[
                                                result_i]
                                            relevant_context = (
                                                relevant_result.get("context"))
                                            for context in relevant_context:
                                                if country_name in context.get(
                                                        "text"):
                                                    country_checkins.append(
                                                        check_ins[region_i])
                                                    break
                                            break
                        except Exception:
                            pass

            country_checkins_count = len(country_checkins)
            if country_checkins_count:
                if country_checkins_count <= 3:
                    score += 4
                elif country_checkins_count >= 4:
                    score += 7

                try:
                    country_checkins.sort(key=lambda checkin: checkin.date)
                    first_checkin_date_str = country_checkins[0].date
                    last_checkin_date_str = country_checkins[-1].date
                    first_checkin_date = pendulum.parse(
                        first_checkin_date_str, strict=False)
                    last_checkin_date = pendulum.parse(
                        last_checkin_date_str, strict=False)

                    date_diff = last_checkin_date.diff(
                        first_checkin_date).in_months()
                    if date_diff == 1:
                        score += 2
                    elif date_diff >= 2:
                        score += 3

                    last_checkin_recency = pendulum.now().diff(
                        last_checkin_date).in_years()
                    if last_checkin_recency == 0:
                        score += 3
                    elif last_checkin_recency <= 10:
                        score += 2

                except Exception as e:
                    logger.info(e)

                if score:
                    if score > 10:
                        score = 10
                    heuristic = {
                        "title": "Check Ins in {}".format(country_name),
                        "description": (
                            "{person} has check ins in {country_name}".format(
                                person=self.get_person_name(),
                                country_name=country_name)),
                        "score": score
                    }
                    if country == "IL":
                        self.alerts.strong_affinity_with_israel = (
                            update_heuristics_score(
                                self.alerts.strong_affinity_with_israel,
                                heuristic))
                    else:
                        pass

        except Exception as e:
            logger.info(e)
