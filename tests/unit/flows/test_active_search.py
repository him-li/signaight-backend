import pytest
import time

from core.models import ActiveSearchEventModel
from core.flows.active_search import active_search_flow
from core.config import settings


@pytest.mark.anyio
class TestGrayfoxFlow:

    @pytest.mark.skip(reason="Review required")
    async def test_active_search_flow(self):
        searches = [
            {
                "title": "project manager"
            },
        ]
        active_searches = []

        for search in searches:
            now = time.time()
            data = {"created_at": now, **search}
            active_search = ActiveSearchEventModel(
                **data
            )
            await active_search.save()
            active_searches.append(active_search)

        host = (settings.JINA_REMOTE_FLOW_LINKEDIN
                if settings.JINA_REMOTE_FLOW_LINKEDIN else None)

        for active_search in active_searches:
            start_time = time.time()
            await active_search_flow(active_search.id,
                                     active_search.title,
                                     active_search.education,
                                     active_search.location,
                                     host)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))
