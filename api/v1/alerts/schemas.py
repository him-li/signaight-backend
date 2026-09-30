from core.models import UUIDModel, Alerts


class AlertsRead(Alerts, UUIDModel):
    # TODO: make it work as alias to respect schema
    # id: uuid.UUID = Field(alias='id')
    pass


class AlertsCreate(Alerts):
    pass


class AlertsUpdate(Alerts):
    pass
