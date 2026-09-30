from isocodes import countries

from core.models.location import Location
from core.utils import check_location_in_country

def check_person_lives_locations(location):
    locations = []
    if location.location:
        locations.append(location.location)
    if current_city := location.current_city:
        if fb_current_city := current_city.fb_current_city:
            locations.append(fb_current_city)
    if current_lat_long := location.current_lat_long:
        if fb_lives_in_lat := current_lat_long.fb_lives_in_lat:
            locations.append(fb_lives_in_lat)
        if fb_lives_in_long := current_lat_long.fb_lives_in_long:
            locations.append(fb_lives_in_long)
    if hometown := location.hometown:
        if fb_hometown := hometown.fb_hometown:
            locations.append(fb_hometown)
    if places_lived := location.places_lived:
        if fb_places_lived := places_lived.fb_places_lived:
            for place in fb_places_lived:
                if place.fb_moved_to:
                    locations.append(place.fb_moved_to)
                if place.fb_moved_at:
                    locations.append(place.fb_moved_at)
    if current_country := location.current_country:
        if linkedin_location_country := (current_country.
                                         linkedin_location_country):
            locations.append(linkedin_location_country)
    if current_city_region_country := location.current_city_region_country:
        if linkedin_location := current_city_region_country.linkedin_location:
            locations.append(linkedin_location)
    if twitter_location := location.twitter_location:
        locations.append(twitter_location)
    if current_location := location.current_location:
        if xing_location := current_location.xing_location:
            locations.append(xing_location)
    return locations


def determine_person_lives_in_country(country, location):
    country_name = countries.get(alpha_2=country).get("name", country)
    locations = check_person_lives_locations(location)
    matching_locations = []
    for location in locations:
        if check_location_in_country(country, location):
            matching_locations.append(location)
        if country_name in location:
            matching_locations.append(location)
    return matching_locations


def extract_location_and_checkins(data: Location):
    data = data.model_dump()
    result = {"locations": [], "check_ins": []}

    def add_location(loc, platform):
        if loc and isinstance(loc, str) and loc.strip():
            result["locations"].append({
                "location": loc.strip(),
                "platform": platform
            })

    def add_checkin(loc, platform, date=None, name=None, image=None, url=None):
        if loc and isinstance(loc, str) and loc.strip():
            item = {
                "location": loc.strip(),
                "platform": platform
            }
            if date:
                item["date"] = date
            if name:
                item["name"] = name
            if image:
                item["image"] = image
            if url:
                item["url"] = url
            result["check_ins"].append(item)

    # Flat single-location fields
    home_town = data.get("hometown") or {}
    current_city = data.get("current_city") or {}
    add_location(current_city.get("fb_current_city"), "facebook")
    add_location(home_town.get("fb_hometown"), "facebook")
    add_location(data.get("linkedin_country_code"), "linkedin")
    add_location(data.get("twitter_location"), "twitter")
    add_location(data.get("icq_location"), "icq")
    add_location(data.get("runkeeper_location"), "runkeeper")
    add_location(data.get("goodreads_location"), "goodreads")
    add_location(data.get("garminconnect_location"), "garminconnect")
    add_location(data.get("flickr_location"), "flickr")
    add_location(data.get("foursquare_location"), "foursquare")
    add_location(data.get("cashapp_location"), "cashapp")
    add_location(data.get("truecaller_country_code"), "truecaller")
    add_location(data.get("microsoft_location"), "microsoft")
    add_location(data.get("yelp_location"), "yelp")

    # Nested current_* blocks
    current_city_region_country = data.get("current_city_region_country") or {}
    add_location(current_city_region_country.get("linkedin_location"), "linkedin")

    current_country = data.get("current_country") or {}
    add_location(current_country.get("linkedin_location_country"), "linkedin")

    check_ins = data.get("check_ins") or {}

    fb_check_ins = check_ins.get("fb_check_ins") or []
    for r in fb_check_ins:
        add_checkin(
            r.get("region"),
            "facebook",
            date=r.get("date"),
            name=r.get("title"),
            image=r.get("event_image"),
            url=r.get("url")
        )

    return result

