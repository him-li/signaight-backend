import json
import logging
from langsearch.models.matcher_results import (
    ExtractedCandidate,
    UnifiedPerson,
    FirstNameSchema,
    LastNameSchema,
    FullNameSchema,
    PhoneNumberSchema,
    EmailAddressSchema,
    ImageSchema,
)
from langsearch.utils.utils import value_counter, merge_value_rankings
from typing import List

logger = logging.getLogger(__name__)


def merge_extracted_candidates(
    candidates: List[dict],
    unified_person: UnifiedPerson
) -> UnifiedPerson:
    f_names = []
    l_names = []
    full_names = []
    phone_numbers = []
    email_addresses = []
    images = []

    for candidate in candidates:
        try:
            candidate = ExtractedCandidate(**candidate)
            source = candidate.source if hasattr(candidate, 'source') and candidate.source else None

            if candidate.f_name:
                f_names.append(candidate.f_name)

            if candidate.l_name:
                l_names.append(candidate.l_name)

            if candidate.full_name:
                full_names.append(candidate.full_name)

            if candidate.phone_number:
                phone_numbers.append(candidate.phone_number)

            if candidate.email_address:
                email_addresses.append(candidate.email_address)

            if candidate.images:
                for image in candidate.images:
                    images.append(image)

            if candidate.locations and len(candidate.locations) > 0:
                unified_person.locations.extend(candidate.locations)
            if candidate.work_experience and len(candidate.work_experience) > 0:
                unified_person.work_experience.extend(candidate.work_experience)
            if candidate.education and len(candidate.education) > 0:
                unified_person.education.extend(candidate.education)
            if (candidate.network_signature
                    and len(candidate.network_signature) > 0):
                unified_person.network_signature.extend(candidate.network_signature)
        except Exception as e:
            logger.error(f"Error merging candidate {getattr(candidate, 'source', 'unknown')}: {e}")
            continue
    try:
        f_names_counter = value_counter(f_names)
        l_names_counter = value_counter(l_names)
        full_names_counter = value_counter(full_names)
        phone_numbers_counter = value_counter(phone_numbers)
        email_addresses_counter = value_counter(email_addresses)
        images_counter = value_counter(images)

        if unified_person.f_name.f_name:
            f_names_counter = merge_value_rankings(unified_person.f_name.f_name, f_names_counter)
        if unified_person.l_name.l_name:
            l_names_counter = merge_value_rankings(unified_person.l_name.l_name, l_names_counter)
        if unified_person.full_name.full_name:
            full_names_counter = merge_value_rankings(unified_person.full_name.full_name, full_names_counter)
        if unified_person.phone_number.phone_number:
            phone_numbers_counter = merge_value_rankings(unified_person.phone_number.phone_number, phone_numbers_counter)
        if unified_person.email_address.email_address:
            email_addresses_counter = merge_value_rankings(unified_person.email_address.email_address, email_addresses_counter)
        if unified_person.images.image:
            images_counter = merge_value_rankings(unified_person.images.image, images_counter)

        unified_person.f_name.f_name = f_names_counter
        unified_person.l_name.l_name = l_names_counter
        unified_person.full_name.full_name = full_names_counter
        unified_person.phone_number.phone_number = phone_numbers_counter
        unified_person.email_address.email_address = email_addresses_counter
        unified_person.images.image = images_counter
    except Exception as e:
        logger.error(f"Error merging value counters: {e}")

    return unified_person
