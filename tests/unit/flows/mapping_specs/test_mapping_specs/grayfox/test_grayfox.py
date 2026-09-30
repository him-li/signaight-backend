import uuid
from datetime import datetime
from glom import glom

from faker import Faker

from core.models.interests import (
    TelegramGroup,
    TelegramMessage)

from core.models import Candidate


from core.clients.grayfox import GrfxSpecs
from core.dotty_dictionary import dotty
from core.utils import clean_dict

from tests.unit.flows.mapping_specs.mapping_targets import Targets

fake = Faker()


class TestMappingsSpecs:
    def test_grfx_get_request_details(self):
        # target = Targets.grfx_get_request_details
        # target = Targets.grfx_new_nuphar
        target = Targets.grfx_phone_972506355101

        spec = GrfxSpecs.get_request_details_spec
        result = glom(target, spec)
        assert result
        search_id = uuid.uuid4()
        f_name = fake.name()
        l_name = fake.name()
        full_name = f_name + " " + l_name
        searched_at = datetime.now()

        for candidate in result.values():
            if candidate and isinstance(candidate, dict):
                candidate = clean_dict(candidate)
                if len(candidate.keys()) == 1:
                    continue
                candidate = dotty(candidate)

                candidate.setdefault("search_id", str(search_id))
                candidate.setdefault(
                    "personal_details.name.first_name.f_name", str(f_name))
                candidate.setdefault(
                    "personal_details.name.last_name.l_name", str(l_name))
                candidate.setdefault(
                    "personal_details.name.full_name.full_name",
                    str(full_name))
                candidate.setdefault("searched_at", str(searched_at))
                candidate = Candidate(**candidate)

                assert candidate
            elif candidate and isinstance(candidate, list):
                for cand in candidate:
                    cand = clean_dict(cand)
                    if len(cand.keys()) == 1:
                        continue
                    cand = dotty(cand)

                    cand.setdefault("search_id", str(search_id))
                    cand.setdefault(
                        "personal_details.name.first_name.f_name", str(f_name))
                    cand.setdefault(
                        "personal_details.name.last_name.l_name", str(l_name))
                    cand.setdefault(
                        "personal_details.name.full_name.full_name",
                        str(full_name))
                    cand.setdefault("searched_at", str(searched_at))
                    cand = Candidate(**cand)

                    assert cand

    def test_grfx_active_search(self):
        target = Targets.grfx_active_search
        spec = GrfxSpecs.get_active_search_results
        result = glom(target, spec)
        assert result
        search_id = uuid.uuid4()
        searched_at = datetime.now()
        source = "grayfox_active_search"

        for candidate in result:
            if candidate:
                candidate = clean_dict(candidate)
                if len(candidate.keys()) == 1:
                    continue
                candidate = dotty(candidate)

                candidate.setdefault("source", source)
                candidate.setdefault("search_id", str(search_id))
                candidate.setdefault("searched_at", str(searched_at))
                candidate = Candidate(**candidate)

                assert candidate

    def test_grfx_get_request_details_phone_with_telegram_groups(self):
        target = Targets.grfx_phone_with_telegram_groups
        spec = GrfxSpecs.get_request_details_spec
        result = glom(target, spec)

        assert result and "telegram_groups" in result

        tg_data = result.get("telegram_groups")
        tg_dotty = dotty(tg_data)
        assert tg_dotty.get("interests")
        assert tg_dotty.get("interests.groups")
        groups = tg_dotty.get("interests.groups.telegram_groups")
        assert isinstance(groups, list)

        for group in groups:
            assert group.get("title")
            assert group.get("telegram_public_group_id")
            assert group.get("messages") is not None

            for message in group.get("messages"):
                assert message.get("date")
                assert message.get("message_id")
                assert message.get("reply_to_message_id")
                assert message.get("text")
                assert TelegramMessage(**message)

            assert TelegramGroup(**group)
