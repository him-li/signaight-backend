import asyncio
import pandas
from core.logging import logger
from core.clients.mapbox.client import api
from ..geo_trace import GeoTrace, Features


async def geotrace_update(person):
    raw_locations = person.personal_details.location.model_dump()

    locations, check_ins = _extract_locations(raw_locations)
    locations = _normalize(locations)

    if can_reuse_existing_trace(person.geo_trace, locations):
        return person.geo_trace

    features = await _build_features(locations, check_ins)

    if features:
        person.geo_trace = GeoTrace(
            type="FeatureCollection",
            features=dedupe_geo_features(features)
        )

    return person.geo_trace


def _extract_locations(location_dict):
    locations = {k: v for k, v in location_dict.items() if v}

    try:
        check_ins = location_dict.get(
            "check_ins", {}).get("fb_check_ins", [])
    except Exception:
        check_ins = []

    try:
        google_reviews = location_dict.get(
            "check_ins", {}).get("google_reviews", [])
    except Exception:
        google_reviews = []

    if check_ins:
        locations.update({
            f"check_in_{c['title']}": c["title"]
            for c in check_ins if c
        })

    if google_reviews:
        locations.update({
            f"google_review_{r['address']}": r["address"]
            for r in google_reviews if r
        })

    locations.pop("check_ins", None)
    return locations, check_ins


def _normalize(locations):
    """Flatten dict into a single-level dict."""
    [flat] = pandas.json_normalize(
        locations, sep=".").to_dict(orient="records")
    return flat


def can_reuse_existing_trace(geo_trace, locations):
    if not geo_trace:
        return False
    features = (
        geo_trace.get("features") if isinstance(geo_trace, dict) else geo_trace.features
    )
    if len(features) != len(locations):
        return False

    feature_names = {f.properties.place_name for f in features}
    location_values = list(locations.values())

    matches = [
        loc for loc in location_values
        for name in feature_names
        if loc in name
    ]

    return len(matches) == len(locations)


async def _build_features(locations, check_ins):
    tasks = []
    values = list(locations.values())

    for value in values:
        if _is_valid_value(value):
            tasks.append(_fetch_mapbox(value))
        else:
            tasks.append(asyncio.sleep(0, result=None))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    features = []
    for key, value, mbox in zip(locations.keys(), locations.values(), results):
        if not mbox:
            continue
        location_type, date = _resolve_location_type(key, check_ins)
        features.append(_create_feature(mbox, location_type, date))

    return features


def _is_valid_value(value):
    return value not in (None, "None", False, "False")


async def _fetch_mapbox(value):
    def call():
        try:
            response = api.search.mapbox(value)
            features = response.body.get("features", [])
            return features[0] if features else None
        except Exception as e:
            logger.warning(f"Mapbox lookup failed for '{value}': {e}")
            return None

    return await asyncio.to_thread(call)


def _resolve_location_type(key, check_ins):
    if key.startswith("check_in_"):
        title = key.replace("check_in_", "")
        check_in = find_checkin_by_partial_key(check_ins, title)
        return "check_ins", (check_in.get("date") if check_in else None)

    if any(tag in key for tag in ("hometown", "current", "location")):
        return "residence", None

    return "entities", None


def _create_feature(mbox, location_type, date):
    props = mbox.get("properties", {})
    geom = mbox.get("geometry", {})

    return Features(
        id=mbox.get("id"),
        type="Feature",
        properties={
            "mapbox_id": props.get("mapbox_id"),
            "wikidata": props.get("wikidata"),
            "short_code": None,
            "place_name": mbox.get("place_name"),
            "location_type": location_type,
            "date": date,
        },
        geometry={
            "coordinates": geom.get("coordinates"),
            "type": geom.get("type", "Point"),
        }
    )


def find_checkin_by_partial_key(check_ins, partial_key):
    return next(
        (c for c in check_ins if partial_key in c.get("title", "")),
        None
    )


def dedupe_geo_features(features):
    seen = set()
    unique = []

    for feat in features:
        key = (
            getattr(feat, "id", None)
            or feat.properties.mapbox_id
            or feat.properties.place_name
        )

        if key and key not in seen:
            seen.add(key)
            unique.append(feat)

    return unique
