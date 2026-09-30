import uuid
from core.models import PersonModel, CandidateModel

from core.documents import EnrichRequestDoc
from core.dotty_dictionary import dotty
from core.utils.urn import build_urn


def get_person_work(person: PersonModel):
    try:
        if positions := (person.biographic_details.work.linkedin_work.
                         positions):
            company_names = []
            for position in positions:
                company_name = position.company_name
                remove_prefixes = ['the']
                remove_sufixes = ['inc', 'llc']
                if company_name.lower().endswith('.'):
                    company_name = company_name.replace(".", "")
                for prefix in remove_prefixes:
                    if company_name.lower().startswith(prefix):
                        company_name = company_name.replace(prefix, "")
                for sufix in remove_sufixes:
                    if company_name.lower().endswith(sufix):
                        company_name = company_name.replace(sufix, "")
                if company_name.find(" ") != -1:
                    company_name = company_name[0: company_name.find(
                        " ")]
                company_names.append(company_name)
            return company_names
    except Exception:
        pass


def get_person_city(person: PersonModel):
    try:
        location = (person.personal_details.location.
                    current_city_region_country.linkedin_location)
        return location
    except Exception:
        pass


def get_person_education(person: PersonModel):
    try:
        if person.biographic_details.education.linkedin_schools:
            education = (person.biographic_details.education.
                         linkedin_schools[0].school_name)
            return education
    except Exception:
        pass


async def create_enrich_doc(doc, search_id):
    candidate = await CandidateModel.get(uuid.UUID(doc.id))
    if candidate:
        candidate_dict = dotty(candidate.model_dump())
        source_id_key = f'network_signature.user_id.{candidate.source}_user_id'
        username_key = (f'network_signature.username.{candidate.source}'
                        '_username')
        profile_url_key = (f'network_signature.url.{candidate.source}'
                           '_profile_url')

        source_id = candidate_dict.get(source_id_key)
        username = candidate_dict.get(username_key)
        profile_url = candidate_dict.get(profile_url_key)

        if source_id:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                source_id=source_id,
                source=candidate.source
            )
        elif profile_url:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                profile_url=str(profile_url),
                source=candidate.source
            )
        elif username:
            return EnrichRequestDoc(
                urn=doc.urn,
                search_id=str(search_id),
                username=username,
                source=candidate.source
            )
    return None


async def create_enrich_doc_list(doc, search_id):
    candidate = await CandidateModel.get(uuid.UUID(doc.id))
    if candidate:
        candidate_dict = dotty(candidate.model_dump())
        source_id_key = f'network_signature.user_id.{candidate.source}_user_id'
        username_key = (f'network_signature.username.{candidate.source}'
                        '_username')
        profile_url_key = (f'network_signature.url.{candidate.source}'
                           '_profile_url')

        source_ids = candidate_dict.get(source_id_key)
        usernames = candidate_dict.get(username_key)
        profile_urls = candidate_dict.get(profile_url_key)

        return_docs = []

        if source_ids:
            for source_id in source_ids:
                return_docs.append(EnrichRequestDoc(
                    urn=doc.urn,
                    search_id=str(search_id),
                    source_id=source_id,
                    source=candidate.source
                ))
        elif profile_urls:
            for profile_url in profile_urls:
                return_docs.append(EnrichRequestDoc(
                    urn=doc.urn,
                    search_id=str(search_id),
                    profile_url=str(profile_url),
                    source=candidate.source
                ))
        elif usernames:
            for username in usernames:
                return_docs.append(EnrichRequestDoc(
                    urn=doc.urn,
                    search_id=str(search_id),
                    username=username,
                    source=candidate.source
                ))
        if return_docs:
            return return_docs
    return None


async def create_enrich_doc_list_candidate_urn(doc, search_id):
    candidate = await CandidateModel.get(uuid.UUID(doc.id))
    if candidate:
        candidate_dict = dotty(candidate.model_dump())
        source_id_key = f'network_signature.user_id.{candidate.source}_user_id'
        username_key = (f'network_signature.username.{candidate.source}'
                        '_username')
        profile_url_key = (f'network_signature.url.{candidate.source}'
                           '_profile_url')

        source_ids = candidate_dict.get(source_id_key)
        usernames = candidate_dict.get(username_key)
        profile_urls = candidate_dict.get(profile_url_key)

        return_docs = []

        candidate_urn = build_urn("candidates", str(candidate.id))
        if source_ids:
            for source_id in source_ids:
                return_docs.append(EnrichRequestDoc(
                    urn=candidate_urn,
                    search_id=str(search_id),
                    source_id=source_id,
                    source=candidate.source
                ))
        elif profile_urls:
            for profile_url in profile_urls:
                return_docs.append(EnrichRequestDoc(
                    urn=candidate_urn,
                    search_id=str(search_id),
                    profile_url=str(profile_url),
                    source=candidate.source
                ))
        elif usernames:
            for username in usernames:
                return_docs.append(EnrichRequestDoc(
                    urn=candidate_urn,
                    search_id=str(search_id),
                    username=username,
                    source=candidate.source
                ))
        if return_docs:
            return return_docs
    return None


def resolve_value(candidate, flow_step, request_params, key):
    if key.startswith("candidate."):
        return getattr(candidate, key.replace("candidate.", ""), None)
    if key == "flow_step":
        return flow_step
    if key.startswith("request."):
        return request_params.get(key.replace("request.", ""))
    return None


def match_condition(value, operator, expected):
    if operator == "eq":
        return value == expected
    if operator == "not":
        return value != expected
    if operator == "in":
        return value in expected
    if operator == "not_in":
        return value not in expected
    return False


def rule_matches(rule, candidate, flow_step, request_params):
    for raw_key, expected in rule["when"].items():
        if ":" in raw_key:
            key, op = raw_key.split(":", 1)
        else:
            key, op = raw_key, "eq"

        value = resolve_value(candidate, flow_step, request_params, key)
        if not match_condition(value, op, expected):
            return False

    return True


def apply_primary_rules(candidate, flow_step, request_params, rules):
    for rule in rules:
        if rule_matches(rule, candidate, flow_step, request_params):
            for field, value in rule["set"].items():
                setattr(candidate, field, value)
            break  # first-match wins


def normalize_email(email: str) -> str:
    return email.strip().lower()


def build_emails_groups(data):
    emails_list = data.get("emails") or []
    emails = set()

    for item in emails_list:
        email = item.get("email")
        if not email:
            continue

        normalized = normalize_email(email)

        emails.add(normalized)

    return list(emails) if emails else None
