from functools import reduce


class Utils:
    def __init__(self):
        self.source_list = ['facebook', 'instagram', 'linkedin']

    def create_dict_for_path(self, person: dict, attribute_path: str):
        nested_path = attribute_path.split('.')
        last_key = nested_path[-1]
        inner_dict = person
        for key in nested_path[:-1]:
            if key not in inner_dict or inner_dict[key] is None:
                inner_dict[key] = {}
            inner_dict = inner_dict[key]

        if last_key not in inner_dict:
            inner_dict[last_key] = {}

        return person

    def update_attribute(
        self,
        person: dict,
        candidate: dict,
        attribute_path: str
    ):
        source = candidate.get('source')
        if source is None or source not in self.source_list:
            return person

        nested_path = attribute_path.format(source=source).split('.')
        value = reduce(
            lambda d, k: d.get(k, {}) if isinstance(d, dict) else None,
            nested_path,
            candidate)

        if value is None:
            return person

        inner_dict = person
        for key in nested_path[:-1]:
            if key not in inner_dict or inner_dict[key] is None:
                inner_dict[key] = {}
            inner_dict = inner_dict[key]

        inner_dict[nested_path[-1]] = value

        return person

    def update_list_attribute(
            self,
            person: dict,
            candidate: dict,
            attribute_path: str
    ):
        source = candidate.get('source')
        if source is None or source not in self.source_list:
            return person

        nested_path = attribute_path.format(source=source).split('.')
        value = reduce(lambda d, k: d.get(k) if isinstance(d, dict) else None,
                       nested_path,
                       candidate)

        if value is None:
            return person

        inner_dict = person
        for key in nested_path[:-1]:
            if key not in inner_dict or inner_dict[key] is None:
                inner_dict[key] = {}
            inner_dict = inner_dict[key]

        if (nested_path[-1] not in inner_dict or
                inner_dict[nested_path[-1]] is None):
            inner_dict[nested_path[-1]] = value if isinstance(
                value, list) else [value]
        elif isinstance(inner_dict[nested_path[-1]], list):
            if isinstance(value, list):
                inner_dict[nested_path[-1]].extend(value)
            elif not any(existing_value == value for existing_value in
                         inner_dict[nested_path[-1]]):
                inner_dict[nested_path[-1]].append(value)

        return person
