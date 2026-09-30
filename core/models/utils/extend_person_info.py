from glom import glom
from urllib.parse import urlparse, unquote_plus

from core.clients.vetric.linkedin import api as vtrc_api, VtLISpecs
from core.dotty_dictionary import dotty
from core.logging import logger
#from core.models import PersonModel
from ..personal_details import PersonalDetails
from ..biographic_details import BiographicDetails


async def extend_personal_details(person):

    # try:
    #    if person.personal_details.name.full_name:
    #        return person
    # except Exception as e:
    #    pass
    try:
        linked_in_url = person.network_signature.url.linkedin_profile_url
    except Exception:
        linked_in_url = None
    if not linked_in_url:
        return person

    try:
        # api lib use quoting itself so we need to pas pure url without quotes
        params = {"url": unquote_plus(str(linked_in_url))}
        response = await vtrc_api.async_profile.resolve_url(params=params)
        resolve_url_body = response.body
    except Exception as e:
        logger.info(e)
        return person
    source_id = glom(resolve_url_body, VtLISpecs.url_resolver_spec)

    try:
        response = await vtrc_api.async_profile.overview(source_id)
        overview_body = response.body
    except Exception as e:
        print(str(e))
        search_state = {
            "is_done": True,
            "status": "Error",
            "description": "Linkedin Overview Error",
        }
        person.search_state = search_state
        return person
    mapped = dotty(glom(overview_body,
                        VtLISpecs.overview_spec,
                        default={}))

    mapped['personal_details.name.full_name.full_name'] = mapped.get(
        "personal_details.name.first_name.f_name", "") + " " + mapped.get(
            "personal_details.name.last_name.l_name", "")

    if mapped.get('biographic_details.work.linkedin_work.positions.period.'
                  'date_to.year'):
        date_to = (str(mapped.get('biographic_details.work.linkedin_work.'
                                  'positions.period.date_to.year')) +
                   "-" +
                   str(mapped.get(
                       'biographic_details.work.linkedin_work.positions.'
                       'period.date_to.month')) + "-01")
        mapped['biographic_details.work.linkedin_work.positions.period.'
               'date_to'] = date_to
    else:
        mapped.pop(
            'biographic_details.work.linkedin_work.positions.period.'
            'date_to')

    if mapped.get('biographic_details.work.linkedin_work.positions.period.'
                  'date_from.year'):
        date_from = (str(mapped.get('biographic_details.work.'
                                    'linkedin_work.positions.period.'
                                    'date_from.year')) +
                     "-" +
                     str(mapped.get(
                         'biographic_details.work.linkedin_work.positions.'
                         'period.date_from.month')) + "-01")
        mapped['biographic_details.work.linkedin_work.positions.period.'
               'date_from'] = date_from
    else:
        mapped.pop(
            'biographic_details.work.linkedin_work.positions.period.'
            'date_from')

    if not mapped.get('biographic_details.work.linkedin_work.positions.'
                      'company_name'):
        mapped.pop('biographic_details.work.linkedin_work.positions')

    if mapped.get('biographic_details.work.linkedin_work.positions'):
        mapped['biographic_details.work.linkedin_work.positions'] = [
            mapped.get('biographic_details.work.linkedin_work.positions')]
    if mapped.get('biographic_details.education.linkedin_schools'):
        mapped['biographic_details.education.linkedin_schools'] = [
            mapped.get('biographic_details.education.linkedin_schools')]

    if person.personal_details:
        if email := person.personal_details.email:
            mapped['personal_details.email'] = email.model_dump()

    personal_details = mapped.get("personal_details")
    biographic_details = mapped.get("biographic_details")

    person.personal_details = PersonalDetails(**personal_details)
    person.biographic_details = BiographicDetails(**biographic_details)
    return person

async def extend_person(person):
    person = await extend_personal_details(person)

