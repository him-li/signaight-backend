import pandas

from core.logging import logger
from core.models.geo_trace import GeoTrace, Features
from core.clients.mapbox.client import api

# NOTE: deprecated and moved to core//models/utils/update_geotrace.py


async def geotrace_update(person):
    location_dict = person.personal_details.location.model_dump()
    locations = {key: val for key, val in location_dict.items() if val}
    check_ins = []
    if location_dict.get('check_ins'):
        if check_ins := location_dict.get(
                'check_ins', {}).get("fb_check_ins", []):
            check_ins_dict = {f"check_in_{checkin.get('title')}": checkin.get(
                'title') for checkin in check_ins if checkin}
            locations.update(**check_ins_dict)
        if google_reviews_list := location_dict.get(
                'check_ins', {}).get("google_reviews", []):
            reviews_dict = {f"google_review_{review.get('address')}": review.get(
                'address') for review in google_reviews_list if review}
            locations.update(**reviews_dict)
        locations.pop("check_ins")
    [locations] = pandas.json_normalize(
        locations, sep=".").to_dict(
        orient='records')
    location_len = len(locations.keys())
    geo_trace = person.geo_trace if person.geo_trace else None
    geo_trace_features = []
    try:
        if geo_trace and len(geo_trace.features) == location_len:
            geo_trace_features = person.geo_trace.features
            feature_names = [feature.properties.place_name for feature in
                             geo_trace_features]
            location_items = locations.values()
            matching_locations = [name for loc in location_items for name in
                                  feature_names if loc in name]
            if len(matching_locations) == location_len:
                pass
            else:
                geo_trace_features = []
    except Exception:
        pass
    if len(geo_trace_features) == 0 or not (len(geo_trace_features) ==
                                            location_len):
        geo_trace_features = []
        for location_key, location_value in locations.items():
            # api search call here location
            if (location_value is not False and location_value != "False" and
                    location_value is not None and location_value != "None"):
                try:
                    response = api.search.mapbox(location_value)
                    response_body = response.body
                    mbox_retrive_data = response_body.get('features', [])[0]
                except Exception:
                    logger.info(
                        f'{location_value} - No matches found in retrive')
                    continue
                if not mbox_retrive_data:
                    logger.info(
                        f'{location_value} - No matches found in retrive')
                    continue
                properties = mbox_retrive_data.get('properties', {})
                geometry = mbox_retrive_data.get('geometry', {})
                if 'check_in' in location_key:
                    location_type = 'check_ins'
                    check_in_title = location_key.replace("check_in_", "")
                    try:
                        check_in = find_checkin_by_partial_key(
                            check_ins, check_in_title)
                        date = check_in.get("date")
                    except Exception as e:
                        print(str(e))
                elif 'hometown' in location_key:
                    location_type = 'residence'
                    date = None
                elif 'current_city' in location_key:
                    location_type = 'residence'
                    date = None
                else:
                    location_type = 'entities'
                    date = None
                feature = Features(**{
                    "id": mbox_retrive_data.get('id'),
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": properties.get('mapbox_id'),
                        "wikidata": properties.get('wikidata'),
                        "short_code": None,
                        "place_name": mbox_retrive_data.get('place_name'),
                        "location_type": location_type,
                        "date": date
                    },
                    "geometry": {
                        "coordinates": geometry.get('coordinates'),
                        "type": geometry.get('type', "Point")
                    }
                })
                geo_trace_features.append(feature)
        if geo_trace_features:
            person.geo_trace = GeoTrace(
                type="FeatureCollection",
                features=geo_trace_features
            )
        return person.geo_trace
    return person.geo_trace


def find_checkin_by_partial_key(check_ins, partial_key):
    return next(
        (checkin for checkin in check_ins if
         partial_key in checkin.get("title", "")),
        None
    )
