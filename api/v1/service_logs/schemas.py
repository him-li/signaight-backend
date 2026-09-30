from core.models import UUIDModel, ServiceStepLog


class ServiceStepLogRead(ServiceStepLog, UUIDModel):
    pass


class ServiceStepLogCreate(ServiceStepLog):
    pass
