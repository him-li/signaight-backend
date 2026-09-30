import pendulum
from business_rules.variables import (
    boolean_rule_variable,
    select_multiple_rule_variable)
from business_rules.fields import FIELD_NUMERIC, FIELD_SELECT, FIELD_TEXT
from iso639 import Lang
from isocodes import countries

from core.clients.mapbox.client import api as mapbox_api
from core.logging import logger
from core.utils import check_position_location_in_country
from core.rules.person.utils import (determine_person_lives_in_country,
                                     check_person_lives_locations,
                                     create_position_model_list_additive)

from ..base import PersonBaseVariables

langs = [Lang("en"), Lang("he")]


class StrongAffinityWithCountryVariables(PersonBaseVariables):

    @select_multiple_rule_variable(
        label=('Schools list where person spent a semester of more'
               ' in Israel as part of an academic program'),
        # options=EducationInstitutions.get_institution_by_country('IL'),
        params=[{
            'field_type': FIELD_NUMERIC,
            'name': 'semesters',
            'label': 'Semesters'
        }]
    )
    def linkedin_education_institutes_more_than_defined_semsesters(
        self,
        semesters=1
    ):
        schools = []
        semesters_in_weeks = semesters*17
        try:
            for school in (self.person.biographic_details.education.
                           linkedin_schools):
                duration = pendulum.duration(
                    years=(int(school.duration.years)
                           if school.duration.years else 0),
                    months=(int(school.duration.months)
                            if school.duration.months else 0)
                )
                date_from = pendulum.parse(school.period.date_from,
                                           strict=False)
                date_to = (pendulum.parse(school.period.date_to, strict=False)
                           if school.period.date_to and not "Present"
                           else pendulum.now())
                period = date_to - date_from
                if (duration.in_weeks() >= semesters_in_weeks
                        or period.in_weeks() >= semesters_in_weeks):
                    schools.append(school.school_name)
        except Exception:
            pass
        return schools

    @boolean_rule_variable(
        label=('Fluency in chosen language is an evidence for strong affinity '
               'with Israel for strong affinity with country of language'),
        params=[
            {
                'field_type': FIELD_SELECT,
                'name': 'target_language',
                'label': 'Language criteria for native speaker',
                # 'options': [lg.name for lg in sorted(langs)]
                'options': [{'label': lg.name, 'name': lg.pt1}
                            for lg in sorted(langs)]
            }
        ]
    )
    def chosen_language_speaker_from_social_networks(self, target_language):
        target_language = Lang(target_language)
        languages_found = []
        try:
            li_languages = self.person.personal_details.languages.li_languages
        except AttributeError:
            li_languages = []
        if isinstance(li_languages, list):
            for item in li_languages:
                try:
                    iso_lang = Lang(item.language)
                    if iso_lang == target_language:
                        languages_found.append(iso_lang.pt1)
                except Exception:
                    pass
        '''
        try:
            fb_languages = self.person.personal_details.languages.fb_languages
        except Exception:
            fb_languages = []
        if isinstance(fb_languages, list):
            for item in fb_languages:
                try:
                    iso_lang = Lang(item)
                    if iso_lang == target_language:
                        languages_found.append(iso_lang.pt1)
                except Exception:
                    pass
        '''

        return True if len(languages_found) > 0 else False

    @boolean_rule_variable(
        label=('Work experience for an chosen country company'),
        params=[
            {
                'field_type': FIELD_SELECT,
                'name': 'country',
                'label': 'Headquarter office country',
                'options': [{'label': c.get('name'), 'name': c.get('alpha_2')}
                            for c in countries.items]
            }
        ]
    )
    def linkedin_work_experience_in_chosen_country(self, country):
        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return False
        except Exception:
            return False
        for position in positions:
            # NOTE: there should position chosen which do not have date-to
            # as probably current position
            return check_position_location_in_country(country, position)
        else:
            return False

    @boolean_rule_variable(
        label='Person lives in specific country',
        params={
            "country": FIELD_TEXT
        }
    )
    def person_lives_in_country(self, country):
        country_name = countries.get(alpha_2=country).get("name", country)
        try:
            person_location = self.person.personal_details.location
        except Exception:
            person_location = None
        if not person_location:
            return False
        locations = check_person_lives_locations(person_location)
        if any(country_name in location for location in locations):
            return True
        if determine_person_lives_in_country(country, person_location):
            return True
        return False

    @boolean_rule_variable(
        label='Has checkins in country',
        params={
            "country": FIELD_TEXT
        }
    )
    def has_checkins_in_country(self, country):
        try:
            country_name = countries.get(alpha_2=country).get("name", country)
            check_ins = getattr(
                getattr(
                    getattr(
                        self.person.personal_details, "location", None
                    ), 
                    "check_ins", None
                ),
                "fb_check_ins",
                None
            )
            if check_ins:
                check_ins_region_list = [
                    check_in.region for check_in in check_ins]
                if check_ins_region_list:
                    for region in check_ins_region_list:
                        if country_name in region:
                            return True
                        try:
                            resp = mapbox_api.search.mapbox(region)
                            resp_body = resp.body
                            if features := resp_body.get("features"):
                                if isinstance(features, list):
                                    for i, result in enumerate(features):
                                        if result.get("relevance") == 1:
                                            relevant_result = features[i]
                                            relevant_context = (
                                                relevant_result.get("context"))
                                            for context in relevant_context:
                                                if country_name in context.get(
                                                        "text"):
                                                    return True
                        except Exception:
                            pass
            return False
        except Exception as e:
            logger.info(e)
            return False
