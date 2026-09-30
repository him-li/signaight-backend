import re
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat


def _clean_input(s: str) -> str:
    if not s:
        return s
    s = s.strip()
    # remove common invisible bidi chars
    for ch in ("\u200e", "\u200f", "\u202a", "\u202c"):
        s = s.replace(ch, "")
    # convert common international prefix 00 -> +
    if s.startswith("00") and not s.startswith("+"):
        s = "+" + s[2:]
    if s.startswith("+"):
        s = s[1:]
    return s


def _digits_only_keep_plus(s: str) -> str:
    if not s:
        return s
    if s.startswith("+"):
        return "+" + re.sub(r'[^0-9]', '', s[1:])
    return re.sub(r'[^0-9]', '', s)


def _parse_number(candidate: str, region_hint: str | None):
    try:
        parsed = phonenumbers.parse(candidate, region_hint)
    except NumberParseException as e:
        return None
    if (phonenumbers.is_valid_number(parsed) or
            phonenumbers.is_possible_number(parsed)):
        try:
            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        except Exception:
            return None
    return None
