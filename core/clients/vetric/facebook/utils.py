import re
import pendulum

_bidi_re = re.compile(r'[\u200E\u200F]')


def clean_text_bidi(s):
    if not s:
        return s
    return _bidi_re.sub('', s).strip()


def parse_education_period(period):
    if not period:
        return None
    if "Class of" in period:
        return {"date_from": None, "date_to": period[-4:]}
    if "present" in period.lower():
        if "-" in period:
            parts = [p.strip() for p in period.split("-", 1)]
            return {"date_from": parts[0] if parts[0] else None,
                    "date_to": None}
        return {"date_from": None, "date_to": None}
    if "-" in period:
        parts = [p.strip() for p in period.split("-", 1)]
        return {"date_from": parts[0] or None, "date_to": parts[1] or None}
    return {"date_from": period, "date_to": None}


def extract_school_name(title):
    if not title:
        return None
    if title.startswith("Went to"):
        return clean_text_bidi(title[len("Went to "):].strip())
    # look for " at " (space-around) to avoid matching 'at' inside words
    lower = title
    if " at " in lower:
        return clean_text_bidi(title.split(" at ", 1)[1].strip())
    # fallback: if "Studied at" exists, remove the prefix
    if title.startswith("Studied at"):
        return clean_text_bidi(title[len("Studied at "):].strip())
    return None


def extract_studied_field(title):
    if not title:
        return None
    # "Studied X at Y" -> X
    if title.startswith("Studied ") and " at " in title:
        # remove leading "Studied " and split on " at "
        return clean_text_bidi(
            title[len("Studied "):].split(" at ", 1)[0].strip())
    # "Studied X" (without 'at')
    if title.startswith("Studied ") and "Studied at" not in title:
        return clean_text_bidi(title[len("Studied "):].strip())
    return None


def extract_workplace_name(title):
    if not title:
        return None
    if title.startswith("Works at"):
        return clean_text_bidi(title[len("Works at "):].strip())
    if " at " in title:
        return clean_text_bidi(title.split(" at ", 1)[1].strip())
    return None


def extract_job_position(title):
    if not title:
        return None
    if title.startswith("Works at"):
        return clean_text_bidi(title[len("Works at "):].strip())
    if " at " in title:
        return clean_text_bidi(title.split(" at ", 1)[0].strip())
    return None


def parse_work_period(period):
    if not period:
        return None
    if "present" in period.lower():
        if "-" in period:
            parts = [p.strip() for p in period.split("-", 1)]
            return {"date_from": parts[0] if parts[0] else None,
                    "date_to": None}
        return {"date_from": None, "date_to": None}
    if "-" in period:
        parts = [p.strip() for p in period.split("-", 1)]
        return {"date_from": parts[0] or None, "date_to": parts[1] or None}
    return {"date_from": period, "date_to": None}


def parse_moved_subtitle(sub):
    if not sub:
        return None
    m = re.search(r"\b(19|20)\d{2}\b", sub)
    if m:
        return m.group(0)
    return sub.strip()


def is_type(typ, needle):
    if not typ:
        return False
    return needle.lower() in typ.lower()


def map_single_place(raw):
    title = clean_text_bidi(raw.get("title"))
    typ = clean_text_bidi(raw.get("field_type"))
    subtitle = clean_text_bidi((raw.get("subtitles") or [None])[0])
    moved_at = parse_moved_subtitle(subtitle)
    return {
        "title": title,
        "type": typ,
        "subtitle": subtitle,
        "moved_at": moved_at,
        "entity_id": raw.get("entity_id"),
        "image": raw.get("image"),
    }


def map_places_list_to_normalized(places_list):
    if not places_list:
        return {"fb_current_city": None,
                "fb_hometown": None,
                "fb_place_lived": None}

    mapped = [map_single_place(p) for p in places_list]

    fb_current_city = {}
    fb_hometown = {}
    moved_entries = []

    for p in mapped:
        title = p.get("title")
        typ = p.get("type")
        moved_at = p.get("moved_at")
        entity_id = p.get("entity_id")
        location_picture = p.get("image")

        if is_type(typ, "current_city") or is_type(typ, "current city"):
            if title:
                fb_current_city["fb_current_city"] = title
            if location_picture:
                fb_current_city["fb_location_picture"] = location_picture
            if entity_id:
                fb_current_city["fb_location_id"] = entity_id
        elif is_type(typ, "hometown"):
            if title:
                fb_hometown["fb_hometown"] = title
            if location_picture:
                fb_hometown["fb_location_picture"] = location_picture
            if entity_id:
                fb_hometown["fb_location_id"] = entity_id
        elif is_type(typ, "moved_city") or is_type(typ, "moved"):
            moved_entries.append(
                {"fb_moved_to": title,
                 "fb_moved_at": moved_at,
                 "fb_location_id": entity_id,
                 "fb_location_picture": location_picture})

    if moved_entries:
        def year_val(entry):
            ma = entry.get("moved_at")
            if isinstance(ma, str) and re.fullmatch(r"(19|20)\d{2}", ma):
                return int(ma)
            return None

    return {
        "fb_current_city": fb_current_city,
        "fb_hometown": fb_hometown,
        "fb_places_lived": moved_entries if moved_entries else None,
    }


def parse_marital_status(relationship):
    if not relationship:
        return None
    entity_id = relationship.get("entity_id")
    partner_name = relationship.get("title")
    profile_picture = relationship.get("image")
    status = relationship.get("subtitles")[
        0].split(" ")[0] if relationship.get("subtitles") else None
    return {
        "fb_marital_status": status,
        "fb_partner": {
            "fb_family_member_name": partner_name,
            "fb_user_id": entity_id,
            "fb_profile_picture": profile_picture,
        } if partner_name or entity_id or profile_picture else None
    }


def parse_languages(basic_info):
    if not basic_info:
        return None
    languages = None
    for info in basic_info:
        if info.get("field_type") == "languages":
            languages = info.get("title", "")

    language_dict_list = None
    if languages:
        languages_list = []
        for part in languages.split("and"):
            languages_list.extend(part.split(","))

            languages_list = [
                language.strip() for language in languages_list if
                language.strip()
            ]
        language_dict_list = [{"language": language}
                              for language in languages_list]

    return language_dict_list


def parse_birthday(basic_info):
    if not basic_info:
        return None
    for info in basic_info:
        if info.get("field_type") == "birthday":
            birthday_str = info.get("title")
            try:
                birthday = (
                    pendulum.parse(
                        birthday_str, strict=False).date().isoformat()
                    if birthday_str
                    else None
                )
                return str(birthday)
            except Exception:
                return None


def parse_gender(basic_info):
    if not basic_info:
        return None
    for info in basic_info:
        if info.get("field_type") == "gender":
            gender = info.get("title", "").lower()
            return gender


def parse_contact_info(contact_info):
    if not contact_info:
        return None
    email = None
    phone = None
    websites = []
    platforms = []
    for info in contact_info:
        if info.get("field_type") == "profile_email":
            email = info.get("title")
        if info.get("field_type") == "profile_phone":
            phone = info.get("title")
        elif info.get("field_type") == "website":
            websites.append({"url": info.get("title")})
        elif info.get("field_type") == "screenname" and info.get("platform"):
            if ("x.com" in info.get("platform", "")
                    or "x.com" in info.get("url", "")):
                platforms.append({"twitter": {"username": info.get(
                    "title"), "url": info.get("url")}})
            elif ("instagram" in info.get("platform", "")
                    or "instagram" in info.get("url", "")):
                platforms.append({"instagram": {"username": info.get(
                    "title"), "url": info.get("url")}})
            if ("linkedin" in info.get("platform", "")
                    or "linkedin" in info.get("url", "")):
                platforms.append({"linkedin": {"username": info.get(
                    "title"), "url": info.get("url")}})

    return {
        "fb_contact_email": email,
        "fb_contact_phone": phone,
        "fb_contact_websites": websites if websites else None,
        "fb_contact_platforms": platforms if platforms else None,
    }
