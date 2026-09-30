from flatten_json import unflatten_list

from core.documents.base import SearchRequestSchema
from core.models import SignAIghtSchema, UUIDModel
from uuid import UUID

class PersonCreate(SearchRequestSchema):
    #project_id: UUID

    def model_dump_as_person(self):
        data = {}
        full_name = []
        if self.f_name:
            data["personal_details.name.first_name.f_name"] = self.f_name
            full_name.append(self.f_name)
        if self.l_name:
            data["personal_details.name.last_name.l_name"] = self.l_name
            full_name.append(self.l_name)
        if full_name:
            data["personal_details.name.full_name.full_name"] = " ".join(full_name)
        if self.email_address:
            data["personal_details.email.email_address.0"] = self.email_address
        # TODO: add support for all fields
        return unflatten_list(data, separator='.')

class PersonReadShort(UUIDModel):
    pass
