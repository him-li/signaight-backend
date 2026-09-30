def clean_dict(d):
    if not isinstance(d, dict):
        return d

    keys_to_delete = []
    for key, value in d.items():
        if value is None or value == [] or value == {}:
            keys_to_delete.append(key)
        elif isinstance(value, dict):
            clean_dict(value)
            if not value:  # Check if the dict became empty after cleaning
                keys_to_delete.append(key)
        elif isinstance(value, list):
            d[key] = [clean_dict(item)
                      for item in value if item not in (None, [], {})]
            if not d[key]:  # Check if the list is empty after cleaning
                keys_to_delete.append(key)

    for key in keys_to_delete:
        del d[key]

    return d
