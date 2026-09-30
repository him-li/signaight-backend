import pendulum
import re

from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT

from core.clients.mapbox.client import api as mapbox_api
from core.models.flags import FlagSubCategory
from core.models.position import Position
from core.rules.person.utils import (
    extract_location_and_checkins,
    get_alpha2_safe)
from core.rules.person.utils.group_geo_trace__by_country import group_by_country
from core.rules.person.utils.update_flag_category import update_person_flag
from core.rules.person.utils.work.work_positions_for_watchlist_countries import create_position_model_list_tagged

from ..base import PersonBaseActions

def find_countries(text: str, countries:list[str]):
        mapping = {c.lower(): c for c in countries if c.strip()}
        parts = sorted(mapping.keys(), key=len, reverse=True)
        if not parts:
            return []
        pat = re.compile(r'\b(?:' + '|'.join(map(re.escape, parts)) + r')\b', re.I)
        result = set()
        for m in pat.finditer(text):
            canonical = mapping.get(m.group(0).lower())
            if canonical:
                result.add(canonical)

        return list(result)
    
def should_request(country: str, detected_countries: set[str]) -> bool:
    """
    Returns True if we need to request Mapbox for this country,
    False if it's already detected in the list.
    """
    return country not in detected_countries

class WatchlistCountriesActions(PersonBaseActions):
    @rule_action(params={
        "red_countries": FIELD_SELECT,
        "orange_countries": FIELD_SELECT,
        "blue_countries": FIELD_SELECT,
    })
    def set_person_watchlist_countries(self,
                                       red_countries,
                                       orange_countries,
                                       blue_countries):
        try:
            try:
                in_red_country = False
                detected_locations = set()
                locations_factors = []
                check_ins_factors = []
                work_factors = []
                red_country_work = []
                orange_country_work = []
                blue_country_work = []
                red_country_checkins = []
                orange_country_checkins = []
                blue_country_checkins = []
                red_country_entities = []
                orange_country_entities = []
                blue_country_entities = []
                check_in_dates = []
                in_orange_country = False
                location = self.person.personal_details.location

                location_check_ins_dict = extract_location_and_checkins(
                    location)

                location_list = location_check_ins_dict.get("locations", [])
                check_ins_list = location_check_ins_dict.get("check_ins", [])
                for location_data in location_list:
                    location = location_data.get('location').lower()
                    if should_request(location, detected_locations):
                        try:                        
                            resp = mapbox_api.search.mapbox(location)
                            detected_locations.add(location)
                            resp_body = resp.body
                            if features := resp_body.get("features"):
                                if not isinstance(features, list):
                                    continue
                                for result_i, result in enumerate(
                                        features):
                                    if result.get("relevance") != 1:
                                        continue
                                    if "country" in result.get("id"):
                                        for country in red_countries:
                                            if country in result.get(
                                                    "text"):
                                                red_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': result})
                                                continue
                                        for country in orange_countries:
                                            if country in result.get(
                                                    "text"):
                                                orange_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': result})
                                                continue
                                        for country in blue_countries:
                                            if country in result.get(
                                                    "text"):
                                                blue_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': result})

                                    relevant_result = features[
                                        result_i]
                                    relevant_context = (
                                        result.get("context"))
                                    for context in relevant_context:
                                        if "country" not in context.get("id"):
                                            continue
                                        for country in red_countries:
                                            if country in context.get(
                                                    "text"):
                                                red_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': relevant_result})
                                                continue
                                        for country in orange_countries:
                                            if country in context.get(
                                                    "text"):
                                                orange_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': relevant_result})
                                                continue
                                        for country in blue_countries:
                                            if country in context.get(
                                                    "text"):
                                                blue_country_entities.append(
                                                    country)
                                                locations_factors.append({**location_data, 'data': relevant_result})
                                    break
                        except Exception:
                            pass
                        
                   

                
                try:
                    check_ins_model_list = location.check_ins.fb_check_ins
                    now = pendulum.now()

                    for i, check_in in enumerate(check_ins_list):
                        try:
                            resp = mapbox_api.search.mapbox(check_in.get('location'))
                            resp_body = resp.body
                            if features := resp_body.get("features"):
                                if not isinstance(features, list):
                                    continue
                                for result_i, result in enumerate(
                                        features):
                                    if result.get("relevance") != 1:
                                        continue
                                    relevant_result = features[
                                        result_i]
                                    relevant_context = (
                                        relevant_result.get("context"))
                                    for context in relevant_context:
                                        if "country" not in context.get("id"):
                                            continue
                                        for country in red_countries:
                                            if country in context.get(
                                                    "text"):
                                                check_in_obj = (
                                                    check_ins_model_list[i]
                                                )
                                                check_in_date = (
                                                    pendulum.parse(
                                                        check_in_obj.date,
                                                        strict=False))
                                                check_in_dates.append(
                                                    check_in_date)
                                                in_red_country = True
                                                red_country_checkins.append(
                                                    country)
                                                check_ins_factors.append({**check_in, 'data': relevant_result})
                                                break
                                        for country in orange_countries:
                                            if country in context.get(
                                                    "text"):
                                                check_in_obj = (
                                                    check_ins_model_list[i])
                                                check_in_date = (
                                                    pendulum.parse(
                                                        check_in_obj.date,
                                                        strict=False))
                                                check_in_dates.append(
                                                    check_in_date)
                                                in_orange_country = True
                                                orange_country_checkins.append(
                                                    country)
                                                check_ins_factors.append({**check_in, 'data': relevant_result})
                                                break

                                        for country in blue_countries:
                                            if country in context.get(
                                                    "text"):
                                                check_in_obj = (
                                                    check_ins_model_list[i])
                                                check_in_date = (
                                                    pendulum.parse(
                                                        check_in_obj.date,
                                                        strict=False))
                                                check_in_dates.append(
                                                    check_in_date)
                                                blue_country_checkins.append(
                                                    country)
                                                check_ins_factors.append({**check_in, 'data': relevant_result})
                                                break
                                    break
                        except Exception:
                            pass
                except Exception:
                    pass
            except Exception:
                pass
            try:
                positions = create_position_model_list_tagged(self.person)
                for position_data in positions:
                    position = position_data.get('position')
                    if (position.period.date_to == "Present" or
                            not position.period.date_to):
                        position_location = position.location
                        if should_request(position_location, detected_locations):
                            try:
                                resp = mapbox_api.search.mapbox(position_location)
                                detected_locations.add(position_location)
                                resp_body = resp.body
                                if features := resp_body.get("features"):
                                    if not isinstance(features, list):
                                        continue
                                    for result_i, result in enumerate(
                                            features):
                                        if result.get("relevance") != 1:
                                            continue
                                        relevant_result = features[
                                            result_i]
                                        relevant_context = (
                                            relevant_result.get("context"))
                                        for context in relevant_context:
                                            if "country" not in context.get("id"):
                                                continue
                                            for country in red_countries:
                                                if country in context.get(
                                                        "text"):
                                                    red_country_work.append(
                                                        country)
                                                    work_factors.append({**position_data, 'data': relevant_result})
                                                    break
                                            for country in orange_countries:
                                                if country in context.get(
                                                        "text"):
                                                    orange_country_work.append(
                                                        country)
                                                    work_factors.append({**position_data, 'data': relevant_result})
                                                    break
                                            for country in blue_countries:
                                                if country in context.get(
                                                        "text"):
                                                    blue_country_work.append(
                                                        country)
                                                    work_factors.append({**position_data, 'data': relevant_result})
                                                    break
                                        break
                            except Exception:
                                pass
            except Exception:
                pass
            try:
                features = self.person.geo_trace.features
                grouped_by_country = group_by_country(features)
                need_to_check = []
                for grouped_country, items in grouped_by_country.items():
                    matches_red = [country for country in red_countries if country.lower() in grouped_country.lower()]
                    if matches_red:
                        need_to_check.extend(items)
                    matches_orange = [country for country in orange_countries if country.lower() in grouped_country.lower()]
                    if matches_orange:
                        need_to_check.extend(items)
                    matches_blue = [country for country in blue_countries if country.lower() in grouped_country.lower()]
                    if matches_blue:
                        need_to_check.extend(items)
                for feature in need_to_check:
                    properties = feature.get('properties', {})
                    origin_place_name = properties.get('place_name', '')
                    place_name = origin_place_name.lower()
                    location_type = properties.get('location_type', None)
                    if should_request(place_name, detected_locations):
                        now = pendulum.now()
                        try:
                            resp = mapbox_api.search.mapbox(place_name)
                            resp_body = resp.body
                            if features_data := resp_body.get("features"):
                                if not isinstance(features_data, list):
                                    continue
                                for result_i, result in enumerate(
                                            features_data):
                                        if result.get("relevance") < 0.45:
                                            continue
                                        relevant_result = features_data[
                                            result_i]
                                        relevant_context = (
                                            relevant_result.get("context"))
                                        for context in relevant_context:
                                            if "country" not in context.get("id"):
                                                continue
                                            for country in red_countries:
                                                if country in context.get(
                                                        "text"):
                                                    if location_type != 'check_ins':
                                                        red_country_entities.append(country)
                                                        locations_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                    else:
                                                        check_ins_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                        red_country_checkins.append(country)
                                                        if properties.get('date'):
                                                            check_in_date = (
                                                                pendulum.parse(
                                                                    properties.get('date'),
                                                                    strict=False))
                                                            check_in_dates.append(
                                                                check_in_date)
                                                    break
                                            for country in orange_countries:
                                                if country in context.get(
                                                        "text"):
                                                    if location_type != 'check_ins':
                                                        orange_country_entities.append(country)
                                                        locations_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                    else:
                                                        check_ins_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                        orange_country_checkins.append(country)
                                                        if properties.get('date'):
                                                            check_in_date = (
                                                                pendulum.parse(
                                                                    properties.get('date'),
                                                                    strict=False))
                                                            check_in_dates.append(
                                                                check_in_date)
                                                    break
                                            for country in blue_countries:
                                                if country in context.get(
                                                        "text"):
                                                    if location_type != 'check_ins':
                                                        blue_country_entities.append(country)
                                                        locations_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                    else:
                                                        check_ins_factors.append({'location': origin_place_name, 'platform': 'map_box', 'data': relevant_result})
                                                        blue_country_checkins.append(country)
                                                        if properties.get('date'):
                                                            check_in_date = (
                                                                pendulum.parse(
                                                                    properties.get('date'),
                                                                    strict=False))
                                                            check_in_dates.append(
                                                                check_in_date)
                                                    break
                                        break
                        except Exception:
                            pass
                        finally:
                            detected_locations.add(place_name)
            except Exception:
                pass

            country_entities_codes = ""
            country_entities = []
            if (
                red_country_entities
                or orange_country_entities
                or blue_country_entities
                or red_country_work
                or orange_country_work
                or blue_country_work
            ):
                country_entities = list(
                    set(
                        [
                            *red_country_entities,
                            *orange_country_entities,
                            *blue_country_entities,
                            *red_country_work,
                            *orange_country_work,
                            *blue_country_work,
                        ]
                    )
                )

                # Convert to codes
                country_entities_codes = ", ".join(
                    code for c in country_entities if (code := get_alpha2_safe(c))
                )
            if locations_factors or work_factors:
                try:
                    sub_category = FlagSubCategory(
                        sub_category="Locations in Watchlist Countries",
                        severity=6.0,
                        description=country_entities_codes,
                        factors=[
                            {
                                "field": "locations",
                                "platform": data.get("platform"),
                                "source": {
                                    "insight": data.get("location"),
                                    "text": data.get("location"),
                                    "location": data.get("data"),
                                },
                            }
                            for data in locations_factors
                        ]
                        + [
                            {
                                "field": "locations",
                                "platform": data.get("platform"),
                                "source": {
                                    "insight": (data.get("position") or Position()).company_name,
                                    "photo": (data.get("position") or Position()).company_logo_url,
                                    "url": (data.get("position") or Position()).company_logo_url,
                                    "text": (data.get("position") or Position()).title,
                                    "location": data.get("data"),
                                },
                            }
                            for data in work_factors
                        ],
                    )

                    self.flag.watchlist_countries = update_person_flag(
                        self.flag.watchlist_countries,
                        sub_categories=[sub_category],
                        category="Watchlist Countries",
                        description=country_entities_codes,
                    )
                except Exception:
                    pass

            country_checkins_codes = ""
            country_checkins = []

            if red_country_checkins or orange_country_checkins or blue_country_checkins:
                country_checkins = list(
                    set(
                        [
                            *red_country_checkins,
                            *orange_country_checkins,
                            *blue_country_checkins,
                        ]
                    )
                )
                try:
                    country_checkins_codes = ", ".join(
                        code for c in country_checkins if (code := get_alpha2_safe(c))
                    )
                except Exception:
                    pass

            if check_in_dates:
                last_check_in_score = 0
                for date in check_in_dates:
                    try:
                        time_delta = now.diff(date).in_years()
                        if time_delta <= 5:
                            last_check_in_score = 4
                        elif time_delta > 5 and time_delta <= 10:
                            last_check_in_score = 2
                        elif time_delta > 10:
                            last_check_in_score = 1
                    except Exception:
                        pass

                if in_red_country:
                    last_check_in_score += 4
                elif in_orange_country:
                    last_check_in_score += 2
                sub_category = FlagSubCategory(
                    sub_category="Check Ins in Watchlist Countries",
                    severity=float(last_check_in_score),
                    description=country_checkins_codes,
                    factors=[
                        {
                            "field": "locations",
                            "platform": check_ins_data.get("platform"),
                            "source": {
                                "insight": check_ins_data.get("location"),
                                "text": check_ins_data.get("name"),
                                "photo": check_ins_data.get("image"),
                                "url": check_ins_data.get("url"),
                                "date": check_ins_data.get("date"),
                                "location": check_ins_data.get("data")
                            },
                        }
                        for check_ins_data in check_ins_factors
                    ],
                )
                try:
                    contries_list = list(
                        set(
                            [
                                *country_checkins,
                                *country_entities,
                            ]
                        )
                    )
                    country_codes = ", ".join(
                        code for c in contries_list if (code := get_alpha2_safe(c))
                    )
                    self.flag.watchlist_countries = update_person_flag(
                        self.flag.watchlist_countries,
                        sub_categories=[sub_category],
                        category="Watchlist Countries",
                        description=country_codes,
                    )
                except Exception:
                    pass

        except Exception:
            pass
