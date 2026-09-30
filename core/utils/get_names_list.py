from glom import glom, Coalesce
import re
from core.clients.ds_app import api as ds_app_api
from core.utils.urn import build_person_urn
from core.logging import logger
from core.dotty_dictionary import Dotty


def is_valid_name(name: str) -> bool:
    """
    Validate that extracted text is a realistic name.
    """

    words = name.split()

    # reject too many words
    if not (2 <= len(words) <= 4):
        return False

    # reject placeholders
    banned = {"none", "unknown", "name"}
    if any(w.lower() in banned for w in words):
        return False

    return True


def extract_name(response: str) -> str | None:
    """
    Extract a person's name from an LLM response.

    Supported formats:
    1. Markdown bold: **John Smith**
    2. Plain text name: John Smith

    Returns None if the response looks like an explanation or sentence.
    """

    if not response:
        return None

    response = response.strip()

    # markdown bold
    match = re.search(r"\*\*([A-Za-zÀ-ÖØ-öø-ÿ' -]{2,80})\*\*", response)
    if match:
        name = match.group(1).strip()
        if is_valid_name(name):
            return name

    # plain name (2-3 capitalized words)
    match = re.search(
        r"\b([A-Z][a-zÀ-ÖØ-öø-ÿ'-]+(?:\s+[A-Z][a-zÀ-ÖØ-öø-ÿ'-]+){1,2})\b",
        response,
    )
    if match:
        name = match.group(1).strip()
        if is_valid_name(name):
            return name

    return None


async def name_resolution(person):
    try:
        person_id = person.get("id")
        emails = (
            person.get("personal_details", {}).get("email", {}).get("email_address")
        )
        names_list = get_names_list(person)
        if names_list:
            body = {
                "hash": str(names_list),
                "names": names_list,
                "additional_data": {"email": emails[0] if emails else ""},
            }
            response = await ds_app_api.async_ds_request.name_resolution(
                body=body, headers={"x-remote-context": build_person_urn(person_id)}
            )
            response_body = response.body
            result_name = response_body.get("names")
            extracted_name = extract_name(result_name[0] if result_name else "")
            print("--name-resolution", names_list, extracted_name)
            return extracted_name
        return None
    except Exception as e:
        logger.error(f"Name resolution error {str(e)}")
        return ""

def normalize_name(name: str | None) -> str | None:
    if not name or not isinstance(name, str):
        return None

    name = re.sub(r"\s+", " ", name.strip())

    if len(name.split()) < 2:
        return None

    banned = {"none", "unknown", "null"}
    if any(w.lower() in banned for w in name.split()):
        return None

    return name

def ensure_dict(obj):
    if isinstance(obj, dict):
        return obj

    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if isinstance(obj, Dotty):
        return obj.to_dict()

    if hasattr(obj, "__dict__"):
        return vars(obj)


def get_names_list(person: dict) -> list[str]:
    names = set()
    
    person = ensure_dict(person)

    # personal_details.name
    person_name = glom(person, Coalesce("personal_details.name", default={})) or {}

    # full_name values
    for v in person_name.get("full_name", {}).values():
        n = normalize_name(v)
        if n:
            names.add(n)

    f_names = glom(person_name,"first_name", default={})
    l_names = glom(person_name, "last_name", default={})

    social_keys = {
        k.split("_")[0] for k in list(f_names.keys()) + list(l_names.keys()) if "_" in k
    }

    for social in social_keys:
        f = next((v for k, v in f_names.items() if k.startswith(social) and v), "")
        l = next((v for k, v in l_names.items() if k.startswith(social) and v), "")

        combined = normalize_name(f"{f} {l}".strip())
        if combined:
            names.add(combined)

    # matched_profiles
    matched_profiles = glom(person, "network_signature.matched_profiles", default={})
    for platform_data in matched_profiles.values():

        if not isinstance(platform_data, dict):
            continue

        primary = platform_data.get("primary_candidate")

        if not primary:
            continue

        for candidate in primary.values():

            # full_name
            n = normalize_name(glom(candidate, "full_name", default=None))
            if n:
                names.add(n)

            # f_name + l_name
            f = glom(candidate, "f_name", default="")
            l = glom(candidate, "l_name", default="")

            combined = normalize_name(f"{f} {l}".strip())
            if combined:
                names.add(combined)

    return sorted(names)
