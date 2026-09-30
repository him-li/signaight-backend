import uuid
from typing import Union
from urnparse import URN8141, NSIdentifier, NSSString


class SignAIghtURN:

    def __init__(self, urn):
        urn = URN8141.from_string(urn)
        self.namespace_id = urn.namespace_id
        self.resource = urn.specific_string.parts[0]
        self.id_type = urn.specific_string.parts[1]
        self.id = urn.specific_string.parts[2]

    @classmethod
    def parse(cls, urn):
        return cls(urn)

    @classmethod
    def build(
        cls,
        resource: str,
        id: Union[str, uuid.UUID],
        id_type='uuid'
    ):
        nid = NSIdentifier('signaight')
        nss = NSSString(f'{resource}:{id_type}:{str(id)}', encoded=True)
        urn = URN8141(nid=nid, nss=nss)
        return str(urn)


# Deprecated and used for backward compatibility
def parse_urn(urn: str) -> str:
    urn = SignAIghtURN.parse(urn)
    return urn.id


# Deprecated and used for backward compatibility
def build_urn(
        resource: str,
        id: Union[str, uuid.UUID],
        id_type='uuid'):
    return SignAIghtURN.build(resource, id, id_type)


def build_person_urn(id: Union[str, uuid.UUID]):
    return build_urn("persons", id)


def check_urn_resource(urn: str) -> str:
    urn = SignAIghtURN.parse(urn)
    return urn.resource
