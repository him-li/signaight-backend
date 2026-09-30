from core.clients.grayfox.mapping.utils import build_images
import pytest
from tests.unit.business_rules.profiles import *  # noqa


@pytest.mark.anyio
async def test_build_images(grayfox_with_pictures):
    unmapped_images = build_images(
        grayfox_with_pictures
    )
    assert unmapped_images is not None
    assert "https://plex.tv/users/6c938ffc95ffd0a9/avatar?t=1671019238907" in unmapped_images

