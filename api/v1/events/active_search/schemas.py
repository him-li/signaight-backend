from core.models import UUIDModel, ActiveSearchEvent


class ActiveSearchEventCreate(ActiveSearchEvent):
    pass


class ActiveSearchEventRead(ActiveSearchEvent, UUIDModel):
    pass


class ActiveSearchEventUpdate(ActiveSearchEvent):
    pass
