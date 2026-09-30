from fastapi import APIRouter

from ..config import settings
from .projects.api import router as projects_router

# from .candidates.api import router as candidates_router
from .persons.api import router as persons_router
from .users.api import router as users_router
from .flows.api import router as flows_router
from .mappings.api import router as mappings_router
from .events.api import router as events_router
from .alerts.api import router as alerts_router
from .evaluation.api import router as evaluation_router
from .flags.api import router as flags_router
from .limits.api import router as limits_router
from .service_logs.api import router as service_logs_router
from .auth.api import router as auth_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (auth_router, "auth", "auth"),
    (projects_router, "projects", "projects"),
    (persons_router, "persons", "persons"),
    (flows_router, "flows", "flows"),
    (mappings_router, "mappings", "mappings"),
    (events_router, "events", "events"),
    (users_router, "users", "users"),
    (alerts_router, "alerts", "alerts"),
    (evaluation_router, "evaluation", "evaluation"),
    (flags_router, "flags", "flags"),
    (limits_router, "limits", "limits"),
    (service_logs_router, "service-logs", "service-logs"),
)

for router_item in routers:
    router, prefix, tags = router_item

    if tags:
        if isinstance(tags, str):
            tags = [tags]
        include_api(router, prefix=f"/{prefix}", tags=tags)
    else:
        include_api(router, prefix=f"/{prefix}")
