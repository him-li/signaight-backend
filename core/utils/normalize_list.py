def normalize_to_list(value):
    if not value:
        return []

    if isinstance(value, list):
        return [v for v in value if v]

    return [value]
