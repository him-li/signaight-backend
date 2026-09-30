import pytest

from core.models import FlagModel
from tests.unit.business_rules.test_business_rules import build_person_run_rules
from .rules import *
from .profiles import *


@pytest.mark.anyio
async def test_islamic_extremism_score(
    person, editor, islamic_extremism_rules, profile_fb_post_salafist_text_english
):
    person = await build_person_run_rules(
        person, editor, profile_fb_post_salafist_text_english, islamic_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.islamic_extremism.severity == 6
@pytest.mark.anyio
async def test_islamic_extremism_score_with_islamist(
    person, editor, islamic_extremism_rules, profile_fb_post_islamist_text_english
):
    person = await build_person_run_rules(
        person, editor, profile_fb_post_islamist_text_english, islamic_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.islamic_extremism.severity == 1
   

