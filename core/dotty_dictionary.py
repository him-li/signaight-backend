import json
from collections.abc import MutableMapping
from dotty_dictionary import (
    Dotty as OriginDotty,
    DottyEncoder
)


class Dotty(OriginDotty): #noqa

    def __contains__(self, item):
        def search_in(items, data):
            """Recursively search for deep key in dict.
            :param list items: List of dictionary keys
            :param data: Portion of dictionary to operate on
            :return bool: Predicate of key existence
            """
            it = items.pop(0)
            if it.isdigit():
                idx = int(it)
                if idx < len(data):
                    if items:
                        return search_in(items, data[idx])
                    else:
                        return data[idx]
                else:
                    return False

            if not data:
                return False

            if items and it in data:
                return search_in(items, data[it])
            return it in data
        return search_in(self._split(item), self._data)

class SafeDottyEncoder(DottyEncoder):
 
    def default(self, obj):
        """Return dict data of Dotty when possible or encode with standard format
        :param object: Input object
        :return: Serializable data
        """
        try:
            if hasattr(obj, '_data'):
                return obj._data
            else:
                return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def dotty(
    dictionary: MutableMapping = None,
    no_list: bool = False,
) -> Dotty:
    """Factory function for Dotty class.

    Create Dotty wrapper around existing or new dictionary.

    Parameters:
        dictionary: Any dictionary or dict-like object
        no_list: If set to True then numeric keys will NOT be converted to list indices

    Returns:
        Dotty instance
    """
    return Dotty(
        dictionary,
        separator=".",
        esc_char="\\",
        no_list=no_list,
        json_encoder=SafeDottyEncoder,
    )
