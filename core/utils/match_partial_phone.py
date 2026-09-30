import re

def match_partial_phone2(masked: str, real: str) -> bool:
    """
    Compare a partially masked phone (e.g. '+**********33') with a real phone (e.g. '+14545454433').
    Returns True if the visible digits of the masked phone appear in order in the real number.
    """
    if not masked or not real:
        return False

    # Normalize: keep only + and digits
    masked_clean = re.sub(r"[^\d\+*]", "", masked)
    real_clean = re.sub(r"[^\d\+]", "", real)

    # Remove '+' to compare digits only
    masked_digits = masked_clean.lstrip('+')
    real_digits = real_clean.lstrip('+')

    # Extract only visible digits from masked phone
    visible_digits = ''.join(ch for ch in masked_digits if ch.isdigit())

    # Quick rejection: visible digits must appear in the real number (usually at the end)
    if not real_digits.endswith(visible_digits):
        return False

    return True
