import pycountry

def get_alpha2_safe(c: str) -> str | None:
    try:
        results = pycountry.countries.search_fuzzy(c)
        if results:
            return getattr(results[0], "alpha_2", None)
    except (LookupError, IndexError):
        return None
    return None
