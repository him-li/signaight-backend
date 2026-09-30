from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_SELECT

from core.rules.person.utils import (
    extract_location_and_checkins, create_position_model_list_additive)
from core.clients.mapbox.client import api as mapbox_api

from ..base import PersonBaseVariables


class WatchlistCountriesVariables(PersonBaseVariables):
    @boolean_rule_variable(
        label='Person has location or checkins in watchlist country',
        params={
            "red_countries": FIELD_SELECT,
            "orange_countries": FIELD_SELECT,
            "blue_countries": FIELD_SELECT,
        }
    )
    def person_has_watchlist_countries_location(self,
                                                red_countries,
                                                orange_countries,
                                                blue_countries):
        try:
            try:

                location = self.person.personal_details.location
                watchlist_countries = (
                    red_countries + orange_countries + blue_countries)
                location_check_ins_dict = extract_location_and_checkins(
                location)

                location_list = location_check_ins_dict.get("locations", [])
                check_ins_list = location_check_ins_dict.get("check_ins", [])

                for location_data in location_list:
                    matches_red = [country for country in red_countries if country.lower() in location_data.get('location').lower()]
                    if matches_red:
                        return True
                    matches_orange = [country for country in orange_countries if country.lower() in location_data.get('location').lower()]
                    if matches_orange:
                        return True
                    matches_blue = [country for country in blue_countries if country.lower() in location_data.get('location').lower()]
                    if matches_blue:
                        return True
                    try:
                        resp = mapbox_api.search.mapbox(location_data.get('location'))
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
                                    for country in watchlist_countries:
                                        if country in context.get(
                                                "text"):
                                            return True
                                break
                    except Exception:
                        pass
                for check_in in check_ins_list:
                    if check_in.get('location') in watchlist_countries:
                        return True
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
                                    for country in watchlist_countries:
                                        if country in context.get(
                                                "text"):
                                            return True
                                break
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                features = self.person.geo_trace.features
                for feature in features:
                    name = feature.properties.place_name.lower()
                    try:
                        matches_red = [country for country in red_countries if country.lower() in name]
                        if matches_red:
                           return True
                        matches_orange = [country for country in orange_countries if country.lower() in name]
                        if matches_orange:
                            return True
                        matches_blue = [country for country in blue_countries if country.lower() in name]
                        if matches_blue:
                            return True
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                positions = create_position_model_list_additive(self.person)
                for position in positions:
                    if (position.period.date_to == "Present" or
                            not position.period.date_to):
                        position_location = position.location
                        try:
                            resp = mapbox_api.search.mapbox(position_location)
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
                                        for country in watchlist_countries:
                                            if country in context.get(
                                                    "text"):
                                                return True
                                    break
                        except Exception:
                            pass
            except Exception:
                pass
            return False
        except Exception:
            return False
