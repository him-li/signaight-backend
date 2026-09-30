from .helpers import _clean_input, _parse_number, _digits_only_keep_plus


def normalize_phone_to_e164(phone: str, iso_country: str | None) -> str | None:
    if not phone or not isinstance(phone, str):
        return None

    s = _clean_input(phone)

    # 2. Try parse as-is with the provided iso_country
    if iso_country:
        res = _parse_number(s, iso_country.upper())
        if res:
            return res
    # 1. If the phone already starts with +, try parsing as international
    if s.startswith("+"):
        res = _parse_number(s, None)
        if res:
            return res


    # 3. Try digits-only with region (clean common separators)
    digits = _digits_only_keep_plus(s)
    if digits and digits != s:
        if digits.startswith("+"):
            res = _parse_number(digits, None)
            if res:
                return res
        if iso_country:
            res = _parse_number(digits, iso_country.upper())
            if res:
                return res

    # 4. Try common trunk removal (leading 0) with region hint
    digits_no_trunk = digits.lstrip("0")
    if digits_no_trunk and digits_no_trunk != digits:
        if iso_country:
            res = _parse_number(digits_no_trunk, iso_country.upper())
            if res:
                return res
        # also try without region to let library infer
        res = _parse_number(digits_no_trunk, None)
        if res:
            return res

    # 5. Final attempt: let libphonenumber infer region without hint
    res = _parse_number(s, None)
    if res:
        return res

    return None
