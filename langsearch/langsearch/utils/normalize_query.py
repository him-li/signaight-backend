"""Utility to normalize search queries by removing personal information."""

import re
from typing import Optional


def normalize_query(query: str, person_info: Optional[dict] = None) -> str:
    """
    Normalize a search query by replacing personal information with placeholders.
    
    This function removes PII (Personally Identifiable Information) from queries
    to create a standardized form for statistics tracking.
    
    Args:
        query: The original search query string
        person_info: Optional dict with person information to help identify PII
        
    Returns:
        A normalized query string with PII replaced by placeholders
    """
    normalized = query
    
    if person_info:
        # Replace full name (firstname lastname)
        firstname = person_info.get("firstname", "").strip()
        lastname = person_info.get("lastname", "").strip()
        if firstname and lastname:
            full_name = f"{firstname} {lastname}"
            # Replace quoted full name
            normalized = re.sub(
                re.escape(f'"{full_name}"'),
                '"[NAME]"',
                normalized,
                flags=re.IGNORECASE
            )
            # Replace unquoted full name
            normalized = re.sub(
                re.escape(full_name),
                "[NAME]",
                normalized,
                flags=re.IGNORECASE
            )
            # Replace individual names
            normalized = re.sub(
                re.escape(f'"{firstname}"'),
                '"[FIRSTNAME]"',
                normalized,
                flags=re.IGNORECASE
            )
            normalized = re.sub(
                re.escape(f'"{lastname}"'),
                '"[LASTNAME]"',
                normalized,
                flags=re.IGNORECASE
            )
            normalized = re.sub(
                re.escape(firstname),
                "[FIRSTNAME]",
                normalized,
                flags=re.IGNORECASE
            )
            normalized = re.sub(
                re.escape(lastname),
                "[LASTNAME]",
                normalized,
                flags=re.IGNORECASE
            )
        
        # Replace email addresses
        email = person_info.get("email", "").strip()
        if email:
            normalized = re.sub(
                re.escape(email),
                "[EMAIL]",
                normalized,
                flags=re.IGNORECASE
            )
        
        # Replace phone numbers (various formats)
        homephone = person_info.get("homephone", "").strip()
        cellphone = person_info.get("cellphone", "").strip()
        for phone in [homephone, cellphone]:
            if phone:
                # Remove common phone formatting characters
                phone_pattern = re.escape(phone)
                # Also match with common formatting
                phone_variants = [
                    phone,
                    phone.replace("-", ""),
                    phone.replace(" ", ""),
                    phone.replace("(", "").replace(")", ""),
                    f"({phone[:3]}) {phone[3:6]}-{phone[6:]}" if len(phone) == 10 else phone,
                ]
                for variant in phone_variants:
                    if variant and variant != phone:
                        normalized = re.sub(
                            re.escape(variant),
                            "[PHONE]",
                            normalized,
                            flags=re.IGNORECASE
                        )
                normalized = re.sub(
                    phone_pattern,
                    "[PHONE]",
                    normalized,
                    flags=re.IGNORECASE
                )
        
        # Replace addresses
        address = person_info.get("address", "").strip()
        if address:
            normalized = re.sub(
                re.escape(address),
                "[ADDRESS]",
                normalized,
                flags=re.IGNORECASE
            )
        
        # Replace date of birth
        dob = person_info.get("dob", "").strip()
        if dob:
            # Match various date formats
            dob_patterns = [
                re.escape(dob),
                dob.replace("/", "-"),
                dob.replace("-", "/"),
            ]
            for pattern in dob_patterns:
                normalized = re.sub(
                    pattern,
                    "[DOB]",
                    normalized,
                    flags=re.IGNORECASE
                )
        
        # Replace location information
        city = person_info.get("city", "").strip()
        state = person_info.get("state", "").strip()
        zip_code = person_info.get("zip", "").strip()
        
        if city:
            normalized = re.sub(
                re.escape(city),
                "[CITY]",
                normalized,
                flags=re.IGNORECASE
            )
        if state:
            normalized = re.sub(
                re.escape(state),
                "[STATE]",
                normalized,
                flags=re.IGNORECASE
            )
        if zip_code:
            normalized = re.sub(
                re.escape(zip_code),
                "[ZIP]",
                normalized,
                flags=re.IGNORECASE
            )
        
        # Replace city, state zip combinations
        if city and state:
            location_variants = [
                f'"{city}, {state}"',
                f'"{city} {state}"',
                f"{city}, {state}",
                f"{city} {state}",
            ]
            if zip_code:
                location_variants.extend([
                    f'"{city}, {state} {zip_code}"',
                    f"{city}, {state} {zip_code}",
                ])
            for variant in location_variants:
                normalized = re.sub(
                    re.escape(variant),
                    "[LOCATION]",
                    normalized,
                    flags=re.IGNORECASE
                )
        
        # Replace country
        country = person_info.get("country", "").strip()
        if country:
            normalized = re.sub(
                r'\b' + re.escape(country) + r'\b',
                "[COUNTRY]",
                normalized,
                flags=re.IGNORECASE
            )
    
    # Generic patterns for common PII (fallback if person_info not provided)
    # Handle quoted names (common pattern: "First Last")
    # This catches names in quotes that weren't replaced by person_info
    normalized = re.sub(
        r'"([A-Z][a-z]+ [A-Z][a-z]+)"',
        '"[NAME]"',
        normalized
    )
    
    # Handle unquoted full names (two capitalized words)
    # Only match if not already a placeholder (simple check)
    if '[NAME]' not in normalized:
        normalized = re.sub(
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',
            '[NAME]',
            normalized
        )
    
    # Common country names (fallback if not in person_info)
    common_countries = [
        'Iran', 'USA', 'United States', 'UK', 'United Kingdom',
        'Canada', 'Australia', 'Germany', 'France', 'Italy',
        'Spain', 'Netherlands', 'Belgium', 'Switzerland', 'Austria',
        'Sweden', 'Norway', 'Denmark', 'Finland', 'Poland',
        'Russia', 'China', 'Japan', 'India', 'Brazil',
        'Mexico', 'Argentina', 'Chile', 'Colombia', 'Peru'
    ]
    for country in common_countries:
        normalized = re.sub(
            r'\b' + re.escape(country) + r'\b',
            '[COUNTRY]',
            normalized,
            flags=re.IGNORECASE
        )
    # Email pattern
    normalized = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL]',
        normalized
    )
    
    # Phone number patterns (US format)
    normalized = re.sub(
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        '[PHONE]',
        normalized
    )
    normalized = re.sub(
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',
        '[PHONE]',
        normalized
    )
    
    # ZIP code pattern
    normalized = re.sub(
        r'\b\d{5}(-\d{4})?\b',
        '[ZIP]',
        normalized
    )
    
    # Date patterns (MM/DD/YYYY, MM-DD-YYYY, etc.)
    normalized = re.sub(
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        '[DATE]',
        normalized
    )
    
    return normalized

