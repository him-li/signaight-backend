from fastapi import APIRouter

from .search.api import router as search_router
from .active_search.api import router as active_search_router
from .recalculation.api import router as recalculation_router

router = APIRouter()

router.include_router(search_router, prefix="/search", tags=["events"])
router.include_router(active_search_router,
                      prefix="/active-search", tags=["events"])
router.include_router(recalculation_router,
                      prefix="/recalculation", tags=["events"])
