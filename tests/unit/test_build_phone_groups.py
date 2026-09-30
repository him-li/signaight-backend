from core.clients.grayfox.mapping.utils import build_phones_groups
import pytest
from tests.unit.business_rules.profiles import *  # noqa


@pytest.mark.anyio
async def test_build_phone_groups(grayfox_with_phones_and_partially_data):
    associate, not_associate = build_phones_groups(
        grayfox_with_phones_and_partially_data
    )
    assert associate is not None
    assert "+15072880549" in associate
    assert not_associate is not None
    assert "+15073989876" in not_associate


@pytest.mark.anyio
async def test_build_phone_groups_without_phones(
    grayfox_without_phones_and_partially_data,
):
    associate, not_associate = build_phones_groups(
        grayfox_without_phones_and_partially_data
    )
    assert associate is None
    assert "+1-507-398-7667" in not_associate


@pytest.mark.anyio
async def test_build_phone_groups_without_metadatas(grayfox_without_metadata_phones):
    associate, not_associate = build_phones_groups(grayfox_without_metadata_phones)
    assert "+7869106068" in associate
    assert "+7869106075" in not_associate
