from .crud import ServiceStepLogCRUD


async def get_service_step_logs_crud() -> ServiceStepLogCRUD:
    return ServiceStepLogCRUD()
