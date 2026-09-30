# flake8: noqa
import pytest
from business_rules import async_run_all, run_all
from mergedeep import merge

from core.models import (
    PersonModel,
    AlertsModel,
    EvaluationModel,
    FlagModel
)
from core.rules.person import (
    PersonVariables,
    PersonActions
)

from .profiles import *
from .rules import *


@pytest.mark.anyio
async def test_education_in_israel_rules(
    person,
    editor,
    education_in_israel_rules,
    education_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        education_in_israel,
        education_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel


@pytest.mark.anyio
async def test_work_change_frequency_rules(
    person,
    editor,
    work_change_frequency_rules,
    frequent_work_change
):
    person = await build_person_run_rules(
        person, editor,
        frequent_work_change,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_work_change_frequency_rules_xing(
    person,
    editor,
    work_change_frequency_rules,
    frequent_work_change_xing
):
    person = await build_person_run_rules(
        person, editor,
        frequent_work_change_xing,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_work_change_frequency_rules_same_company(
    person,
    editor,
    work_change_frequency_rules,
    not_frequent_work_change
):
    person = await build_person_run_rules(
        person, editor,
        not_frequent_work_change,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_frequent_work_change_facebook(
    person,
    editor,
    work_change_frequency_rules,
    frequent_work_change_facebook
):
    person = await build_person_run_rules(
        person, editor,
        frequent_work_change_facebook,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_work_change_frequency_rules_same_company(
    person,
    editor,
    work_change_frequency_rules,
    not_frequent_work_change
):
    person = await build_person_run_rules(
        person, editor,
        not_frequent_work_change,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_work_change_frequency_rules_same_company_thomas(
    person,
    editor,
    work_change_frequency_rules,
    not_frequent_work_change_thomas
):
    person = await build_person_run_rules(
        person, editor,
        not_frequent_work_change_thomas,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_profile_no_job_hopper_katrien(
    person,
    editor,
    work_change_frequency_rules,
    profile_no_job_hopper_katrien
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_job_hopper_katrien,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_no_job_hopper_viara(
    person,
    editor,
    work_change_frequency_rules,
    profile_no_job_hopper_viara
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_job_hopper_viara,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_no_job_hopper_tina(
    person,
    editor,
    work_change_frequency_rules,
    profile_no_job_hopper_tina
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_job_hopper_tina,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_job_hopper_primoz_6_expected(
    person,
    editor,
    work_change_frequency_rules,
    profile_job_hopper_primoz_6_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_job_hopper_primoz_6_expected,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability
    assert alerts.occupational_instability.score == 6


@pytest.mark.anyio
async def test_profile_job_hopper_brane_6_expected(
    person,
    editor,
    work_change_frequency_rules,
    profile_job_hopper_brane_6_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_job_hopper_brane_6_expected,
        work_change_frequency_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability
    assert alerts.occupational_instability.score == 6


@pytest.mark.anyio
async def test_hebrew_lang_native_speaker_rules(
    person,
    editor,
    hebrew_lang_native_speaker_rules,
    hebrew_native_speaker
):
    person = await build_person_run_rules(
        person, editor,
        hebrew_native_speaker,
        hebrew_lang_native_speaker_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel


@pytest.mark.anyio
async def test_work_experience_in_israel_rules(
    person,
    editor,
    work_experience_in_israel_rules,
    profile_with_israeli_company
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_israeli_company,
        work_experience_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel


@pytest.mark.anyio
async def test_work_experience_in_israel_rules_xing(
    person,
    editor,
    work_experience_in_israel_rules,
    profile_with_israeli_company_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_israeli_company_xing,
        work_experience_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel


@pytest.mark.anyio
async def test_profile_with_volunteering(
    person,
    editor,
    volunteering_experience_rules,
    profile_with_volunteering
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering,
        volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values


@pytest.mark.anyio
async def test_profile_with_volunteering_no_duration(
    person,
    editor,
    volunteering_experience_rules,
    profile_with_volunteering_no_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_no_duration,
        volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values


@pytest.mark.anyio
async def test_profile_with_volunteering_only_duration(
    person,
    editor,
    volunteering_experience_rules,
    profile_with_volunteering_only_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_only_duration,
        volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values


@pytest.mark.anyio
async def test_person_score_rules(
    person,
    editor,
    person_score_rules,
    hebrew_native_speaker
):
    person = await sync_build_person_run_rules(
        person, editor,
        hebrew_native_speaker,
        person_score_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert
    assert person.signaight_score == 52


@pytest.mark.anyio
async def test_person_only_score_compatibility_rules_dries(
    person,
    editor,
    person_only_score_compatibility_rules
):
    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()
    evaluation_dict = {
        "courage": {
            "factors": [
                {
                    "title": "Dries Peeters has extreme sports detected",
                    "score": 3,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters has travel check_ins in risky areas",
                    "score": 6.5,
                    "weight": 1
                }
            ],
            "score": 6.5
        },
        "curiosity": {
            "factors": [
                {
                    "title": "Dries Peeters has international travel indicatives",
                    "score": 9,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters has profiles in reading and learning platforms",
                    "score": 8,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters's social media intro/bio indicate interest in food culture.",
                    "score": 9,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters has international travel check_ins",
                    "score": 10,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters work experience, skills, courses and other data show curiosity.",
                    "score": 3.4,
                    "weight": 1
                }
            ],
            "score": 7.88
        },
        "decision_making": {
            "factors": [
                {
                    "title": "Dries Peeters has management positions",
                    "score": 8,
                    "weight": 1
                }
            ],
            "score": 8
        },
        "flexibility": {
            "factors": [
                {
                    "title": "Dries Peeters Skill Set Analysis",
                    "score": 3,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters's work experience shows flexibility when transitioning between industries",
                    "score": 10,
                    "weight": 1
                }
            ],
            "score": 10
        },
        "interpersonal_skills": {
            "factors": [
                {
                    "title": "Dries Peeters shows sociable behaviour",
                    "score": 7,
                    "weight": 1
                }
            ],
            "score": 7
        },
        "language_skills": {
            "factors": [
                {
                    "title": "Dries Peeters has high proficiency in 1 languages and speaks 2 other languages.",
                    "score": 9,
                    "weight": 1
                }
            ],
            "score": 9
        },
        "moral_values": None,
        "resilience": {
            "factors": [
                {
                    "title": "Dries Peeters's posts indicate an optimism score of 9.0",
                    "score": 9,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters work experience and skills show resilience.",
                    "score": 7.11,
                    "weight": 1
                },
                {
                    "title": "Dries Peeters's posts indicate an optimism score of 8.0",
                    "score": 8,
                    "weight": 1
                }
            ],
            "score": 8.036666666666667
        },
        "teamwork": {
            "factors": [
                {
                    "title": "Dries Peeters's experience shows teamwork",
                    "score": 10,
                    "weight": 3
                },
                {
                    "title": "Dries Peeters's posts show team related activities",
                    "score": 10,
                    "weight": 10
                }
            ],
            "score": 10
        },
        "work_under_pressure": {
            "factors": [
                {
                    "title": "Dries Peeters has demonstrated work experience in roles that require the ability to perform effectively under pressure.",
                    "score": 10,
                    "weight": 1
                }
            ],
            "score": 10
        }
    }
    evaluation_dict.setdefault("person", person.id)
    evaluation = EvaluationModel(**evaluation_dict)
    alerts = AlertsModel(person=person)
    flags = FlagModel(person=person)
    run_all(
        rule_list=person_only_score_compatibility_rules,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await evaluation.insert()
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation
    assert person.signaight_score == 95


@pytest.mark.anyio
async def test_person_affinity_with_israel(
    person,
    editor,
    person_israel_affinity_rules,
    hebrew_native_speaker,
    profile_with_israeli_company,
    education_in_israel
):
    bio_details = merge(education_in_israel, profile_with_israeli_company)
    person_data = {**person,
                   **hebrew_native_speaker,
                   **bio_details}
    person = await build_person_run_rules(
        person, editor,
        person_data,
        person_israel_affinity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert evaluation
    assert alerts.strong_affinity_with_israel
    assert len(alerts.strong_affinity_with_israel.heuristics) == 3


@pytest.mark.anyio
async def test_career_break_position(
    person,
    editor,
    career_break_rules,
    career_break_position
):
    person = await build_person_run_rules(
        person, editor,
        career_break_position,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_career_break_position_xing(
    person,
    editor,
    career_break_rules,
    career_break_position_xing
):
    person = await build_person_run_rules(
        person, editor,
        career_break_position_xing,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_career_break_position_facebook(
    person,
    editor,
    career_break_rules,
    career_break_position_facebook
):
    person = await build_person_run_rules(
        person, editor,
        career_break_position_facebook,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_old_career_break_position(
    person,
    editor,
    career_break_rules,
    old_career_break_position
):
    person = await build_person_run_rules(
        person, editor,
        old_career_break_position,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_old_career_break_position_facebook(
    person,
    editor,
    career_break_rules,
    old_career_break_position_facebook
):
    person = await build_person_run_rules(
        person, editor,
        old_career_break_position_facebook,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_old_long_break_between_positions(
    person,
    editor,
    career_break_rules,
    old_long_break_between_positions
):
    person = await build_person_run_rules(
        person, editor,
        old_long_break_between_positions,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_long_break_between_positions(
    person,
    editor,
    career_break_rules,
    long_break_between_positions
):
    person = await build_person_run_rules(
        person, editor,
        long_break_between_positions,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_long_break_between_positions_xing(
    person,
    editor,
    career_break_rules,
    long_break_between_positions_xing
):
    person = await build_person_run_rules(
        person, editor,
        long_break_between_positions_xing,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.occupational_instability


@pytest.mark.anyio
async def test_no_career_break(
    person,
    editor,
    career_break_rules,
    no_career_break_positions
):
    person = await build_person_run_rules(
        person, editor,
        no_career_break_positions,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_multiple_present_positions_no_career_break(
    person,
    editor,
    career_break_rules,
    profile_multiple_present_positions_no_career_break
):
    person = await build_person_run_rules(
        person, editor,
        profile_multiple_present_positions_no_career_break,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_no_career_break_positions_ralitsa(
    person,
    editor,
    career_break_rules,
    no_career_break_positions_ralitsa
):
    person = await build_person_run_rules(
        person, editor,
        no_career_break_positions_ralitsa,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_career_break_student_position(
    person,
    editor,
    career_break_rules,
    profile_career_break_student_position
):
    person = await build_person_run_rules(
        person, editor,
        profile_career_break_student_position,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_career_break_covid(
    person,
    editor,
    career_break_rules,
    profile_career_break_covid
):
    person = await build_person_run_rules(
        person, editor,
        profile_career_break_covid,
        career_break_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_management_title(
    person,
    editor,
    management_positions_rules,
    profile_with_management_title
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_management_title,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.decision_making
    assert evaluation.decision_making.score


@pytest.mark.anyio
async def test_profile_with_management_title_xing(
    person,
    editor,
    management_positions_rules,
    profile_with_management_title_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_management_title_xing,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.decision_making
    assert evaluation.decision_making.score


@pytest.mark.anyio
async def test_profile_with_management_title_facebook(
    person,
    editor,
    management_positions_rules,
    profile_with_management_title_facebook
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_management_title_facebook,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.decision_making
    assert evaluation.decision_making.score


@pytest.mark.anyio
async def test_profile_without_management_title(
    person,
    editor,
    management_positions_rules,
    profile_without_management_title
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_management_title,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.decision_making


@pytest.mark.anyio
async def test_profile_without_minimum_experience(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_management_title(
    person,
    editor,
    management_positions_rules,
    profile_with_management_title
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_management_title,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.decision_making
    assert evaluation.decision_making.score


@pytest.mark.anyio
async def test_profile_with_management_title_xing(
    person,
    editor,
    management_positions_rules,
    profile_with_management_title_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_management_title_xing,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.decision_making
    assert evaluation.decision_making.score


@pytest.mark.anyio
async def test_profile_without_management_title(
    person,
    editor,
    management_positions_rules,
    profile_without_management_title
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_management_title,
        management_positions_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.decision_making


@pytest.mark.anyio
async def test_profile_without_minimum_experience(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 10


@pytest.mark.anyio
async def test_profile_with_minimum_experience(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_without_minimum_experience_internship(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience_internship
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience_internship,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 8


@pytest.mark.anyio
async def test_profile_without_minimum_experience_internship_xing(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience_internship_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience_internship_xing,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 8


@pytest.mark.anyio
async def test_profile_with_minimum_experience_internship(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience_internship
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience_internship,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_minimum_experience_internship_xing(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience_internship_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience_internship_xing,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_journalism_background(
    person,
    editor,
    journalism_background_rules,
    profile_with_journalism_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_journalism_background,
        journalism_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_journalism_background_xing(
    person,
    editor,
    journalism_background_rules,
    profile_with_journalism_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_journalism_background_xing,
        journalism_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_government_background(
    person,
    editor,
    government_background_rules,
    profile_with_government_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background,
        government_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_government_background_xing(
    person,
    editor,
    government_background_rules,
    profile_with_government_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background_xing,
        government_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_international_travel_intro(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_international_travel_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_international_travel_intro,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_intro_only_emojis(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_international_travel_intro_only_emojis
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_international_travel_intro_only_emojis,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_description_bio_intro_empty(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_description_bio_intro_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_description_bio_intro_empty,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_checkins(
    person,
    editor,
    international_travel_checkins_rules,
    profile_with_check_ins
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins,
        international_travel_checkins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_instagram_location_name(
    person,
    editor,
    international_travel_checkins_rules,
    profile_with_instagram_location_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_instagram_location_name,
        international_travel_checkins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_risky_areas_checkins(
    person,
    editor,
    travel_risky_areas_check_ins_rules,
    profile_with_check_ins
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins,
        travel_risky_areas_check_ins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage
    assert evaluation.courage.score == 10


@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
@pytest.mark.anyio
async def test_profile_with_international_travel_risky_areas_instagram_location_name(
    person,
    editor,
    travel_risky_areas_check_ins_rules,
    profile_with_instagram_location_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_instagram_location_name,
        travel_risky_areas_check_ins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage
    assert evaluation.courage.score == 10


@pytest.mark.anyio
async def test_profile_with_profile_with_teamwork_skill_no_endorser(
    person,
    editor,
    teamwork_skill_rules,
    profile_with_teamwork_skill_one_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_one_endorser,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_profile_with_teamwork_skill_six_endorsers(
    person,
    editor,
    teamwork_skill_rules,
    profile_with_teamwork_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_six_endorsers,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_profile_without_teamwork_skill(
    person,
    editor,
    teamwork_skill_rules,
    profile_without_teamwork_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_teamwork_skill,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_location_not_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_location_not_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_location_not_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert not alert


@pytest.mark.anyio
async def test_profile_with_one_location_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_one_location_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_one_location_in_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 8


@pytest.mark.anyio
async def test_profile_with_two_locations_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_two_locations_in_israel_no_linkedin(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel_no_linkedin
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel_no_linkedin,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_two_locations_in_israel_no_city(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel_no_city
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel_no_city,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_six_endorsers(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_six_endorsers,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 10


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_no_endorsers(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_no_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_no_endorsers,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 5


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_xing(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_xing,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 5


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_teamwork_skill_six_endorsers(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_teamwork_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_six_endorsers,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 9


@pytest.mark.anyio
async def test_profile_with_linkedin_skills_empty(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_linkedin_skills_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_skills_empty,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_teamwork_xing_skill_six_endorsers(
    person,
    editor,
    socialble_behaviour_rules,
    profile_teamwork_xing_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing_skill_six_endorsers,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 8


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_teamwork_no_interpersonal(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_teamwork_no_interpersonal
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_no_interpersonal,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_without_teamwork_skill(
    person,
    editor,
    socialble_behaviour_rules,
    profile_without_teamwork_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_teamwork_skill,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_interpersonal_skill(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_interpersonal_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpersonal_skill,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_interpersonal_skill_xing(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_interpersonal_skill_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpersonal_skill_xing,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_post_no_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_post_no_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_no_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_post_with_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_post_with_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_with_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_empty_posts(
    person,
    editor,
    socialble_behaviour_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_cover_no_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_cover_no_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_cover_no_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_profile_with_empty_xing_skills(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_empty_xing_skills
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_empty_xing_skills,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_cover_with_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_cover_with_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_cover_with_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_visuals_empty(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_visuals_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_visuals_empty,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_profile_with_post_no_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_with_post_no_extreme_sports
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_no_extreme_sports,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_without_posts(
    person,
    editor,
    extreme_sports_rules,
    profile_without_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_posts,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


# NOTE: test run took 109.42 seconds
@pytest.mark.anyio
async def test_profile_with_posts_empty(
    person,
    editor,
    extreme_sports_rules,
    profile_with_posts_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_posts_empty,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
@pytest.mark.anyio
async def test_profile_with_posts_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_with_posts_extreme_sports
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_posts_extreme_sports,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage


@pytest.mark.anyio
async def test_profile_with_empty_posts_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_with_linkedin_high_proficiency_languages(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_high_proficiency_languages
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_high_proficiency_languages,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 10


@pytest.mark.anyio
async def test_profile_with_linkedin_2_high_proficiency_languages_1_low(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_2_high_proficiency_languages_1_low
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_2_high_proficiency_languages_1_low,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 8


@pytest.mark.anyio
async def test_profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 5


@pytest.mark.anyio
async def test_profile_with_xing_high_proficiency_languages(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_high_proficiency_languages
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_high_proficiency_languages,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 10


@pytest.mark.anyio
async def test_profile_with_xing_high_2_proficiency_languages_1_low(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_high_2_proficiency_languages_1_low
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_high_2_proficiency_languages_1_low,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 8


@pytest.mark.anyio
async def test_profile_with_xing_1_high_proficiency_language_1_low_1_no_prof(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_1_high_proficiency_language_1_low_1_no_prof
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_1_high_proficiency_language_1_low_1_no_prof,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 5


@pytest.mark.anyio
async def test_profile_work_under_pressure_2_experiences(
    person,
    editor,
    work_under_pressure_rules,
    frequent_work_change
):
    person = await build_person_run_rules(
        person, editor,
        frequent_work_change,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 4


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_8_expected(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_8_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_5_expected_xing(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_5_expected_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_5_expected_xing,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 5


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_8_expected_no_duration(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_8_expected_no_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected_no_duration,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_5_expected_no_duration_xing(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_5_expected_no_duration_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_5_expected_no_duration_xing,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 5


@pytest.mark.anyio
async def test_profile_fb_page_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_page_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7.5


@pytest.mark.anyio
async def test_profile_fb_page_no_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_page_no_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_no_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_pages_empty(
    person,
    editor,
    altruism_rules,
    profile_pages_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_pages_empty,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_interests_empty(
    person,
    editor,
    altruism_rules,
    profile_interests_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_interests_empty,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_interests_None(
    person,
    editor,
    altruism_rules,
    profile_interests_None
):
    person = await build_person_run_rules(
        person, editor,
        profile_interests_None,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_fb_page_no_fb_page_name(
    person,
    editor,
    altruism_rules,
    profile_fb_page_no_fb_page_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_no_fb_page_name,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_no_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_post_text_no_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_no_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_post_text_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 9


@pytest.mark.anyio
async def test_altruism_profile_empty_posts(
    person,
    editor,
    altruism_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_with_skills_flexibility_1_endorse(
    person,
    editor,
    flexibility_rules,
    profile_with_skills_flexible_1_endorse
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_skills_flexible_1_endorse,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 8


@pytest.mark.anyio
async def test_profile_with_skills_flexibility_endorsed(
    person,
    editor,
    flexibility_rules,
    profile_with_skills_flexible_endorsed
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_skills_flexible_endorsed,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 9


@pytest.mark.anyio
async def test_profile_with_no_skills_flexibility(
    person,
    editor,
    flexibility_rules,
    profile_with_no_skills_flexible_1_endorse
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_skills_flexible_1_endorse,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.anyio
async def test_profile_with_no_skills_flexible_only_xing(
    person,
    editor,
    flexibility_rules,
    profile_with_no_skills_flexible_only_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_skills_flexible_only_xing,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_work_flexibility,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 9


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility_xing(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_work_flexibility_xing,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 9


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility_and_skill(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility,
    profile_with_skills_flexible_endorsed
):
    profile_data = merge(profile_with_skills_flexible_endorsed,
                         profile_with_work_flexibility)
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 10
    assert len(evaluation.flexibility.factors) == 2


@pytest.mark.anyio
async def test_profile_fb_post_text_optimism(
    person,
    editor,
    optimism_rules,
    profile_fb_post_text_optimism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_optimism,
        optimism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience


@pytest.mark.anyio
async def test_profile_with_criminal_records_eumw(
    person,
    editor,
    criminal_records_rules,
    profile_with_criminal_records_eumw
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_criminal_records_eumw,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_criminal_records_interpol(
    person,
    editor,
    criminal_records_rules,
    profile_with_criminal_records_interpol
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_criminal_records_interpol,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_interpol_eumw_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_interpol_eumw_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpol_eumw_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_eumw_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_eumw_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_eumw_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_interpol_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_interpol_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpol_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_without_criminal_records(
    person,
    editor,
    criminal_records_rules,
    profile_without_criminal_records
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_criminal_records,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert


@pytest.mark.anyio
async def test_profile_with_criminal_records_score(
    person,
    editor,
    criminal_records_score_rules,
    profile_with_criminal_records_eumw
):
    person = await sync_build_person_run_rules(
        person, editor,
        profile_with_criminal_records_eumw,
        criminal_records_score_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10
    assert person.signaight_score == 0
    assert str(person.compatibility) == "Compatibility.disqualified"


@pytest.mark.anyio
async def test_profile_without_criminal_records_score(
    person,
    editor,
    criminal_records_score_rules,
    profile_without_criminal_records
):
    person = await sync_build_person_run_rules(
        person, editor,
        profile_without_criminal_records,
        criminal_records_score_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    assert person.signaight_score == 40
    assert str(person.compatibility) != "Compatibility.disqualified"


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_user_id(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_user_id
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_user_id,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_matched_profiles(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_matched_profiles,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_url(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_url
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_url,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_facebook_instagram(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_facebook_instagram
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_facebook_instagram,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_fb_post_text_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6


@pytest.mark.anyio
async def test_profile_fb_post_text_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_not_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_not_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_page_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_page_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_not_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_not_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_supporting_israel_empty_posts(
    person,
    editor,
    suporting_israel_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_supporting_israel_empty_pages(
    person,
    editor,
    suporting_israel_rules,
    profile_pages_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_pages_empty,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_and_pages_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_supporting_israel,
    profile_fb_page_supporting_israel
):
    profile_data = {**profile_fb_post_text_supporting_israel,
                    **profile_fb_page_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_post_text_and_pages_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_not_supporting_israel,
    profile_fb_page_not_supporting_israel
):
    profile_data = {**profile_fb_post_text_not_supporting_israel,
                    **profile_fb_page_not_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_page_supporting_israel_posts_not(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_supporting_israel,
    profile_fb_post_text_not_supporting_israel
):
    profile_data = {**profile_fb_page_supporting_israel,
                    **profile_fb_post_text_not_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_page_not_supporting_israel_posts_supporting(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_not_supporting_israel,
    profile_fb_post_text_supporting_israel
):
    profile_data = {**profile_fb_page_not_supporting_israel,
                    **profile_fb_post_text_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6


@pytest.mark.anyio
async def test_profile_teamwork_linkedin(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_linkedin
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_linkedin,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_xing(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_linkedin_duration(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_linkedin_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_linkedin_duration,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_xing_duration(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_xing_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing_duration,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_no_endorser(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_no_endorser,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 3.5


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 5.25


@pytest.mark.anyio
async def test_profile_with_adaptability_agility_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_agility_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_agility_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 9.75


@pytest.mark.anyio
async def test_profile_with_adaptability_agility_versatility_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_agility_versatility_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_agility_versatility_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 10


@pytest.mark.anyio
async def test_profile_with_not_flexible_skill_set(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_not_flexible_skill_set
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_not_flexible_skill_set,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility

@pytest.mark.skip(reason="Value of evaluation.flexibility.score is dramatically lower than required due changes in ds_app")
@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_israeli_company
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_israeli_company,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions_gov_ngo(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_government_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions_gov_ngo_xing(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_government_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background_xing,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_1_industry_1_positions(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_work_under_pressure_score_8_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.anyio
async def test_profile_li_post_text_team_related_3_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_team_related_3_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_team_related_3_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 5


@pytest.mark.anyio
async def test_profile_li_post_text_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 8


@pytest.mark.anyio
async def test_profile_li_post_text_not_team_related(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_not_team_related
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_not_team_related,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_li_post_reaction_team_related_3_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_team_related_3_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_team_related_3_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 5


@pytest.mark.anyio
async def test_profile_li_post_reaction_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 6


@pytest.mark.anyio
async def test_profile_li_post_reaction_not_team_related(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_not_team_related
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_not_team_related,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_li_posts_and_reactions_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_posts_and_reactions_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_posts_and_reactions_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 2
    assert round(evaluation.teamwork.score, 2) >= 7.82

@pytest.mark.skip(reason="No data in evaluation.resilience found. ds_app dependant")
@pytest.mark.anyio
async def test_profile_with_volunteering_one_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_one_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_one_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience
    assert evaluation.resilience.score >= 8

    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7

    assert evaluation.courage
    assert evaluation.courage.score >= 6

@pytest.mark.skip(reason="No data in evaluation.resilience found. ds_app dependant")
@pytest.mark.anyio
async def test_profile_with_volunteering_two_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_two_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_two_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience
    assert evaluation.resilience.score >= 8

    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7

    assert evaluation.courage
    assert evaluation.courage.score >= 6


@pytest.mark.anyio
async def test_profile_with_volunteering_two_not_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_two_not_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_two_not_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.resilience

    assert not evaluation.moral_values

    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_no_endorser_work_under_pressure(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.work_under_pressure


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 6


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_2_endorsers(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_2_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_2_endorsers,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 7


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_5_endorsers(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_5_endorsers,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 7


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score == 10


@pytest.mark.anyio
async def test_profile_with_foodie_intro(
    person,
    editor,
    foodie_intro_rules,
    profile_with_foodie_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_foodie_intro,
        foodie_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 10


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
async def test_profile_with_no_foodie_intro(
    person,
    editor,
    foodie_intro_rules,
    profile_with_no_foodie_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_foodie_intro,
        foodie_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_fb_page_foodie(
    person,
    editor,
    foodie_pages_rules,
    profile_fb_page_foodie
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_foodie,
        foodie_pages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score >= 4


@pytest.mark.anyio
async def test_profile_fb_page_not_foodie(
    person,
    editor,
    foodie_pages_rules,
    profile_fb_page_not_foodie
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_not_foodie,
        foodie_pages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_2_positions_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_2_positions_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_2_positions_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_2_skills_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_with_2_skills_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_2_skills_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_check_ins_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_with_check_ins_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_no_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_no_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_2_positions_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_2_positions_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_2_positions_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_2_skills_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_with_2_skills_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_2_skills_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience


@pytest.mark.anyio
async def test_profile_no_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_no_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.resilience


@pytest.mark.anyio
async def test_profile_checkins_in_israel(
    person,
    editor,
    checkins_in_israel_rules,
    profile_checkins_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_in_israel,
        checkins_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel
    assert alerts.strong_affinity_with_israel.score >= 9


@pytest.mark.anyio
async def test_profile_checkins_not_in_israel(
    person,
    editor,
    checkins_in_israel_rules,
    profile_checkins_not_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_not_in_israel,
        checkins_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_without_minimum_experience_facebook(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience_facebook
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience_facebook,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 10


@pytest.mark.anyio
async def test_profile_with_minimum_experience_facebook(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience_facebook
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience_facebook,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_without_minimum_experience_internship(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience_internship
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience_internship,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 8


@pytest.mark.anyio
async def test_profile_without_minimum_experience_internship_xing(
    person,
    editor,
    min_experience_positions_rules,
    profile_without_minimum_experience_internship_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_minimum_experience_internship_xing,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation
    assert alerts.ineligible_occupation.score == 8


@pytest.mark.anyio
async def test_profile_with_minimum_experience_internship(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience_internship
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience_internship,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_minimum_experience_internship_xing(
    person,
    editor,
    min_experience_positions_rules,
    profile_with_minimum_experience_internship_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_minimum_experience_internship_xing,
        min_experience_positions_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_with_journalism_background(
    person,
    editor,
    journalism_background_rules,
    profile_with_journalism_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_journalism_background,
        journalism_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_journalism_background_xing(
    person,
    editor,
    journalism_background_rules,
    profile_with_journalism_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_journalism_background_xing,
        journalism_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_journalism_background_facebook(
    person,
    editor,
    journalism_background_rules,
    profile_with_journalism_background_facebook
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_journalism_background_facebook,
        journalism_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_government_background(
    person,
    editor,
    government_background_rules,
    profile_with_government_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background,
        government_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_government_background_xing(
    person,
    editor,
    government_background_rules,
    profile_with_government_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background_xing,
        government_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_government_background_facebook(
    person,
    editor,
    government_background_rules,
    profile_with_government_background_facebook
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background_facebook,
        government_background_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.ineligible_occupation


@pytest.mark.anyio
async def test_profile_with_international_travel_intro(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_international_travel_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_international_travel_intro,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_intro_only_emojis(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_international_travel_intro_only_emojis
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_international_travel_intro_only_emojis,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_description_bio_intro_empty(
    person,
    editor,
    international_travel_intro_rules,
    profile_with_description_bio_intro_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_description_bio_intro_empty,
        international_travel_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_checkins(
    person,
    editor,
    international_travel_checkins_rules,
    profile_with_check_ins
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins,
        international_travel_checkins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_instagram_location_name(
    person,
    editor,
    international_travel_checkins_rules,
    profile_with_instagram_location_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_instagram_location_name,
        international_travel_checkins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_with_international_travel_risky_areas_checkins(
    person,
    editor,
    travel_risky_areas_check_ins_rules,
    profile_with_check_ins
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins,
        travel_risky_areas_check_ins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage
    assert evaluation.courage.score == 10


@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
@pytest.mark.anyio
async def test_profile_with_international_travel_risky_areas_instagram_location_name(
    person,
    editor,
    travel_risky_areas_check_ins_rules,
    profile_with_instagram_location_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_instagram_location_name,
        travel_risky_areas_check_ins_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage
    assert evaluation.courage.score == 10


@pytest.mark.anyio
async def test_profile_with_profile_with_teamwork_skill_no_endorser(
    person,
    editor,
    teamwork_skill_rules,
    profile_with_teamwork_skill_one_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_one_endorser,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_profile_with_teamwork_skill_six_endorsers(
    person,
    editor,
    teamwork_skill_rules,
    profile_with_teamwork_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_six_endorsers,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_profile_without_teamwork_skill(
    person,
    editor,
    teamwork_skill_rules,
    profile_without_teamwork_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_teamwork_skill,
        teamwork_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_location_not_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_location_not_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_location_not_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert not alert


@pytest.mark.anyio
async def test_profile_with_one_location_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_one_location_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_one_location_in_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score >= 8


@pytest.mark.anyio
async def test_profile_with_two_locations_israel(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_two_locations_in_israel_no_linkedin(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel_no_linkedin
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel_no_linkedin,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_two_locations_in_israel_no_city(
    person,
    editor,
    lives_in_israel_rules,
    profile_with_two_locations_in_israel_no_city
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_two_locations_in_israel_no_city,
        lives_in_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id
    )
    assert alert.strong_affinity_with_israel
    assert alert.strong_affinity_with_israel.score == 10


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_six_endorsers(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_six_endorsers,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 10


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_no_endorsers(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_no_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_no_endorsers,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 5


@pytest.mark.anyio
async def test_profile_with_decision_making_skill_xing(
    person,
    editor,
    decision_making_skill_rules,
    profile_with_decision_making_skill_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_decision_making_skill_xing,
        decision_making_skill_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork
    assert evaluation.decision_making
    assert evaluation.decision_making.score == 5


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_teamwork_skill_six_endorsers(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_teamwork_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_skill_six_endorsers,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score == 9


@pytest.mark.anyio
async def test_profile_with_linkedin_skills_empty(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_linkedin_skills_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_skills_empty,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_teamwork_xing_skill_six_endorsers(
    person,
    editor,
    socialble_behaviour_rules,
    profile_teamwork_xing_skill_six_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing_skill_six_endorsers,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score >= 8


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_teamwork_no_interpersonal(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_teamwork_no_interpersonal
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_teamwork_no_interpersonal,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score >= 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_without_teamwork_skill(
    person,
    editor,
    socialble_behaviour_rules,
    profile_without_teamwork_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_teamwork_skill,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_interpersonal_skill(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_interpersonal_skill
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpersonal_skill,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score >= 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_interpersonal_skill_xing(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_interpersonal_skill_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpersonal_skill_xing,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills
    assert evaluation.interpersonal_skills.score >= 7


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_post_no_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_post_no_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_no_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_post_with_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_post_with_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_with_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_empty_posts(
    person,
    editor,
    socialble_behaviour_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_cover_no_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_cover_no_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_cover_no_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_profile_with_empty_xing_skills(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_empty_xing_skills
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_empty_xing_skills,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_cover_with_sociable_events(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_cover_with_sociable_events
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_cover_with_sociable_events,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_sociable_behaviour_profile_with_visuals_empty(
    person,
    editor,
    socialble_behaviour_rules,
    profile_with_visuals_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_visuals_empty,
        socialble_behaviour_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_profile_with_post_no_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_with_post_no_extreme_sports
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_post_no_extreme_sports,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_without_posts(
    person,
    editor,
    extreme_sports_rules,
    profile_without_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_posts,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


# NOTE: test run took 109.42 seconds
@pytest.mark.anyio
async def test_profile_with_posts_empty(
    person,
    editor,
    extreme_sports_rules,
    profile_with_posts_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_posts_empty,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
@pytest.mark.anyio
async def test_profile_with_posts_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_with_posts_extreme_sports
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_posts_extreme_sports,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.courage


@pytest.mark.anyio
async def test_profile_with_empty_posts_extreme_sports(
    person,
    editor,
    extreme_sports_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        extreme_sports_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_with_linkedin_high_proficiency_languages(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_high_proficiency_languages
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_high_proficiency_languages,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 10


@pytest.mark.anyio
async def test_profile_with_linkedin_2_high_proficiency_languages_1_low(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_2_high_proficiency_languages_1_low
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_2_high_proficiency_languages_1_low,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 8


@pytest.mark.anyio
async def test_profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof(
    person,
    editor,
    multiple_languages_rules,
    profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_linkedin_1_high_proficiency_language_1_low_1_no_prof,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 5


@pytest.mark.anyio
async def test_profile_with_xing_high_proficiency_languages(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_high_proficiency_languages
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_high_proficiency_languages,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 10


@pytest.mark.anyio
async def test_profile_with_xing_high_2_proficiency_languages_1_low(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_high_2_proficiency_languages_1_low
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_high_2_proficiency_languages_1_low,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 8


@pytest.mark.anyio
async def test_profile_with_xing_1_high_proficiency_language_1_low_1_no_prof(
    person,
    editor,
    multiple_languages_rules,
    profile_with_xing_1_high_proficiency_language_1_low_1_no_prof
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_xing_1_high_proficiency_language_1_low_1_no_prof,
        multiple_languages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.language_skills
    assert evaluation.language_skills.score == 5


@pytest.mark.anyio
async def test_profile_work_under_pressure_2_experiences(
    person,
    editor,
    work_under_pressure_rules,
    frequent_work_change
):
    person = await build_person_run_rules(
        person, editor,
        frequent_work_change,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 4


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_8_expected(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_8_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_5_expected_xing(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_5_expected_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_5_expected_xing,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 5


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_8_expected_no_duration(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_8_expected_no_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected_no_duration,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_work_under_pressure_score_5_expected_no_duration_xing(
    person,
    editor,
    work_under_pressure_rules,
    profile_work_under_pressure_score_5_expected_no_duration_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_5_expected_no_duration_xing,
        work_under_pressure_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 5


@pytest.mark.anyio
async def test_profile_fb_page_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_page_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7.5


@pytest.mark.anyio
async def test_profile_fb_page_no_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_page_no_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_no_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_pages_empty(
    person,
    editor,
    altruism_rules,
    profile_pages_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_pages_empty,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_interests_empty(
    person,
    editor,
    altruism_rules,
    profile_interests_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_interests_empty,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_interests_None(
    person,
    editor,
    altruism_rules,
    profile_interests_None
):
    person = await build_person_run_rules(
        person, editor,
        profile_interests_None,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_altruism_profile_fb_page_no_fb_page_name(
    person,
    editor,
    altruism_rules,
    profile_fb_page_no_fb_page_name
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_no_fb_page_name,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_no_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_post_text_no_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_no_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_altruism(
    person,
    editor,
    altruism_rules,
    profile_fb_post_text_altruism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_altruism,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 9


@pytest.mark.anyio
async def test_altruism_profile_empty_posts(
    person,
    editor,
    altruism_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        altruism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_with_skills_flexibility_1_endorse(
    person,
    editor,
    flexibility_rules,
    profile_with_skills_flexible_1_endorse
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_skills_flexible_1_endorse,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 8


@pytest.mark.anyio
async def test_profile_with_skills_flexibility_endorsed(
    person,
    editor,
    flexibility_rules,
    profile_with_skills_flexible_endorsed
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_skills_flexible_endorsed,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 9


@pytest.mark.anyio
async def test_profile_with_no_skills_flexibility(
    person,
    editor,
    flexibility_rules,
    profile_with_no_skills_flexible_1_endorse
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_skills_flexible_1_endorse,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.anyio
async def test_profile_with_no_skills_flexible_only_xing(
    person,
    editor,
    flexibility_rules,
    profile_with_no_skills_flexible_only_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_skills_flexible_only_xing,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_work_flexibility,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 9


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility_xing(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_work_flexibility_xing,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 9


@pytest.mark.skip(reason="Test skipped due to flexibility work factor being disabled")
@pytest.mark.anyio
async def test_profile_with_work_flexibility_and_skill(
    person,
    editor,
    flexibility_rules,
    profile_with_work_flexibility,
    profile_with_skills_flexible_endorsed
):
    profile_data = merge(profile_with_skills_flexible_endorsed,
                         profile_with_work_flexibility)
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        flexibility_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 10
    assert len(evaluation.flexibility.factors) == 2


@pytest.mark.anyio
async def test_profile_with_anti_israel(
    person,
    editor,
    anti_israel_rules,
    profile_with_anti_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_anti_israel,
        anti_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.anti_israel_statements
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.anti_israel_statements


@pytest.mark.anyio
async def test_profile_without_anti_israel(
    person,
    editor,
    anti_israel_rules,
    profile_without_anti_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_anti_israel,
        anti_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_with_anti_usa(
    person,
    editor,
    anti_usa_rules,
    profile_with_anti_usa
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_anti_usa,
        anti_usa_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.anti_usa_statements
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.anti_usa_statements


@pytest.mark.anyio
async def test_profile_without_anti_usa(
    person,
    editor,
    anti_usa_rules,
    profile_without_anti_usa
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_anti_usa,
        anti_usa_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_without_anti_usa_anti_israel(
    person,
    editor,
    anti_usa_rules,
    profile_with_anti_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_anti_israel,
        anti_usa_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_not_anti_israel(
    person,
    editor,
    anti_israel_rules,
    profile_not_anti_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_not_anti_israel,
        anti_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_not_anti_israel_2(
    person,
    editor,
    anti_israel_rules,
    profile_not_anti_israel_2
):
    person = await build_person_run_rules(
        person, editor,
        profile_not_anti_israel_2,
        anti_israel_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_not_anti_israel_not_anti_usa_2(
    person,
    editor,
    anti_usa_rules,
    profile_not_anti_israel_2
):
    person = await build_person_run_rules(
        person, editor,
        profile_not_anti_israel_2,
        anti_usa_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_fb_post_text_optimism(
    person,
    editor,
    optimism_rules,
    profile_fb_post_text_optimism
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_optimism,
        optimism_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience
    assert evaluation.resilience.score >= 8


@pytest.mark.anyio
async def test_profile_with_criminal_records_eumw(
    person,
    editor,
    criminal_records_rules,
    profile_with_criminal_records_eumw
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_criminal_records_eumw,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_criminal_records_interpol(
    person,
    editor,
    criminal_records_rules,
    profile_with_criminal_records_interpol
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_criminal_records_interpol,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_interpol_eumw_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_interpol_eumw_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpol_eumw_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_eumw_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_eumw_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_eumw_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_with_interpol_matched_profiles(
    person,
    editor,
    criminal_records_rules,
    profile_with_interpol_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_interpol_matched_profiles,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10


@pytest.mark.anyio
async def test_profile_without_criminal_records(
    person,
    editor,
    criminal_records_rules,
    profile_without_criminal_records
):
    person = await build_person_run_rules(
        person, editor,
        profile_without_criminal_records,
        criminal_records_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert


@pytest.mark.anyio
async def test_profile_with_criminal_records_score(
    person,
    editor,
    criminal_records_score_rules,
    profile_with_criminal_records_eumw
):
    person = await sync_build_person_run_rules(
        person, editor,
        profile_with_criminal_records_eumw,
        criminal_records_score_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alert.criminal_records
    assert alert.criminal_records.score == 10
    assert person.signaight_score == 0
    assert str(person.compatibility) == "Compatibility.disqualified"


@pytest.mark.anyio
async def test_profile_without_criminal_records_score(
    person,
    editor,
    criminal_records_score_rules,
    profile_without_criminal_records
):
    person = await sync_build_person_run_rules(
        person, editor,
        profile_without_criminal_records,
        criminal_records_score_rules)
    alert = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alert
    assert person.signaight_score == 40
    assert str(person.compatibility) != "Compatibility.disqualified"


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_user_id(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_user_id
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_user_id,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_matched_profiles(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_matched_profiles
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_matched_profiles,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo_url(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo_url
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo_url,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_goodreads_duolingo(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_goodreads_duolingo
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_goodreads_duolingo,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 8


@pytest.mark.anyio
async def test_profile_with_facebook_instagram(
    person,
    editor,
    curiosity_reading_learning_platforms_rules,
    profile_with_facebook_instagram
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_facebook_instagram,
        curiosity_reading_learning_platforms_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_fb_post_text_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6


@pytest.mark.anyio
async def test_profile_fb_post_text_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_not_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_text_not_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_page_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_page_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_not_supporting_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_not_supporting_israel,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_supporting_israel_empty_posts(
    person,
    editor,
    suporting_israel_rules,
    profile_empty_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_empty_posts,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_supporting_israel_empty_pages(
    person,
    editor,
    suporting_israel_rules,
    profile_pages_empty
):
    person = await build_person_run_rules(
        person, editor,
        profile_pages_empty,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_post_text_and_pages_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_supporting_israel,
    profile_fb_page_supporting_israel
):
    profile_data = {**profile_fb_post_text_supporting_israel,
                    **profile_fb_page_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_post_text_and_pages_not_supporting_israel(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_post_text_not_supporting_israel,
    profile_fb_page_not_supporting_israel
):
    profile_data = {**profile_fb_post_text_not_supporting_israel,
                    **profile_fb_page_not_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.moral_values


@pytest.mark.anyio
async def test_profile_fb_page_supporting_israel_posts_not(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_supporting_israel,
    profile_fb_post_text_not_supporting_israel
):
    profile_data = {**profile_fb_page_supporting_israel,
                    **profile_fb_post_text_not_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6.5


@pytest.mark.anyio
async def test_profile_fb_page_not_supporting_israel_posts_supporting(
    person,
    editor,
    suporting_israel_rules,
    profile_fb_page_not_supporting_israel,
    profile_fb_post_text_supporting_israel
):
    profile_data = {**profile_fb_page_not_supporting_israel,
                    **profile_fb_post_text_supporting_israel}
    person = await build_person_run_rules(
        person, editor,
        profile_data,
        suporting_israel_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 6


@pytest.mark.anyio
async def test_profile_teamwork_linkedin(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_linkedin
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_linkedin,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_xing(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_linkedin_duration(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_linkedin_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_linkedin_duration,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_teamwork_xing_duration(
    person,
    editor,
    teamwork_experience_rules,
    profile_teamwork_xing_duration
):
    person = await build_person_run_rules(
        person, editor,
        profile_teamwork_xing_duration,
        teamwork_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_no_endorser(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_no_endorser,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 3.5


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 5.25


@pytest.mark.anyio
async def test_profile_with_adaptability_agility_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_agility_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_agility_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 9.75


@pytest.mark.anyio
async def test_profile_with_adaptability_agility_versatility_skill_5_endorsers(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_adaptability_agility_versatility_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_agility_versatility_skill_5_endorsers,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score == 10


@pytest.mark.anyio
async def test_profile_with_not_flexible_skill_set(
    person,
    editor,
    flexibility_skill_set_rules,
    profile_with_not_flexible_skill_set
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_not_flexible_skill_set,
        flexibility_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility

@pytest.mark.skip(reason="Value of evaluation.flexibility.score is dramatically lower than required due changes in ds_app")
@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_israeli_company
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_israeli_company,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions_gov_ngo(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_government_background
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_2_industries_2_positions_gov_ngo_xing(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_with_government_background_xing
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_government_background_xing,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.flexibility
    assert evaluation.flexibility.score >= 7


@pytest.mark.anyio
async def test_profile_transition_between_industries_1_industry_1_positions(
    person,
    editor,
    flexibility_transition_industries_rules,
    profile_work_under_pressure_score_8_expected
):
    person = await build_person_run_rules(
        person, editor,
        profile_work_under_pressure_score_8_expected,
        flexibility_transition_industries_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.flexibility


@pytest.mark.anyio
async def test_profile_li_post_text_team_related_3_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_team_related_3_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_team_related_3_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score == 5


@pytest.mark.anyio
async def test_profile_li_post_text_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 8


@pytest.mark.anyio
async def test_profile_li_post_text_not_team_related(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_text_not_team_related
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_text_not_team_related,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_li_post_reaction_team_related_3_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_team_related_3_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_team_related_3_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 5


@pytest.mark.anyio
async def test_profile_li_post_reaction_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 1
    assert evaluation.teamwork.score >= 6


@pytest.mark.anyio
async def test_profile_li_post_reaction_not_team_related(
    person,
    editor,
    team_related_activities_rules,
    profile_li_post_reaction_not_team_related
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_reaction_not_team_related,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.teamwork


@pytest.mark.anyio
async def test_profile_li_posts_and_reactions_team_related_6_posts(
    person,
    editor,
    team_related_activities_rules,
    profile_li_posts_and_reactions_team_related_6_posts
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_posts_and_reactions_team_related_6_posts,
        team_related_activities_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.teamwork
    assert len(evaluation.teamwork.factors) == 2
    assert round(evaluation.teamwork.score, 2) >= 7.82

@pytest.mark.skip(reason="No data in evaluation.resilience found. ds_app dependant")
@pytest.mark.anyio
async def test_profile_with_volunteering_one_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_one_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_one_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience
    assert evaluation.resilience.score >= 8

    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7

    assert evaluation.courage
    assert evaluation.courage.score >= 6

@pytest.mark.skip(reason="No data in evaluation.resilience found. ds_app dependant")
@pytest.mark.anyio
async def test_profile_with_volunteering_two_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_two_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_two_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience
    assert evaluation.resilience.score >= 8

    assert evaluation.moral_values
    assert evaluation.moral_values.score >= 7

    assert evaluation.courage
    assert evaluation.courage.score >= 6


@pytest.mark.anyio
async def test_profile_with_volunteering_two_not_risky(
    person,
    editor,
    significant_volunteering_experience_rules,
    profile_with_volunteering_two_not_risky
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_volunteering_two_not_risky,
        significant_volunteering_experience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.resilience

    assert not evaluation.moral_values

    assert not evaluation.courage


@pytest.mark.anyio
async def test_profile_with_adaptability_skill_no_endorser_work_under_pressure(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.work_under_pressure


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 6


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_2_endorsers(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_2_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_2_endorsers,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 7


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_skill_5_endorsers(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_skill_5_endorsers
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_skill_5_endorsers,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 7


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score >= 8


@pytest.mark.anyio
async def test_profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser(
    person,
    editor,
    work_under_pressure_skill_set_rules,
    profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser,
        work_under_pressure_skill_set_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.work_under_pressure
    assert evaluation.work_under_pressure.score == 10


@pytest.mark.anyio
async def test_profile_with_foodie_intro(
    person,
    editor,
    foodie_intro_rules,
    profile_with_foodie_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_foodie_intro,
        foodie_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score == 10


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails. Review needed")
async def test_profile_with_no_foodie_intro(
    person,
    editor,
    foodie_intro_rules,
    profile_with_no_foodie_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_foodie_intro,
        foodie_intro_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
async def test_profile_fb_page_foodie(
    person,
    editor,
    foodie_pages_rules,
    profile_fb_page_foodie
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_foodie,
        foodie_pages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity
    assert evaluation.curiosity.score >= 4


@pytest.mark.anyio
async def test_profile_fb_page_not_foodie(
    person,
    editor,
    foodie_pages_rules,
    profile_fb_page_not_foodie
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_not_foodie,
        foodie_pages_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_2_positions_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_2_positions_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_2_positions_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_2_skills_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_with_2_skills_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_2_skills_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_check_ins_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_with_check_ins_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_check_ins_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.curiosity


@pytest.mark.anyio
async def test_profile_no_curiosity(
    person,
    editor,
    tuned_curiosity_rules,
    profile_no_curiosity
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_curiosity,
        tuned_curiosity_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.curiosity


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_2_positions_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_2_positions_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_2_positions_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience


@pytest.mark.anyio
@pytest.mark.xfail(reason="Sometimes test fails because of 500 response from DS app. Review needed")
async def test_profile_with_2_skills_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_with_2_skills_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_2_skills_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.resilience


@pytest.mark.anyio
async def test_profile_no_resilience(
    person,
    editor,
    tuned_resilience_rules,
    profile_no_resilience
):
    person = await build_person_run_rules(
        person, editor,
        profile_no_resilience,
        tuned_resilience_rules)
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert not evaluation.resilience


@pytest.mark.anyio
async def test_profile_checkins_in_israel(
    person,
    editor,
    checkins_in_israel_rules,
    profile_checkins_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_in_israel,
        checkins_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert alerts.strong_affinity_with_israel
    assert alerts.strong_affinity_with_israel.score >= 9


@pytest.mark.anyio
async def test_profile_checkins_not_in_israel(
    person,
    editor,
    checkins_in_israel_rules,
    profile_checkins_not_in_israel
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_not_in_israel,
        checkins_in_israel_rules)
    alerts = await AlertsModel.find_one(
        AlertsModel.person.id == person.id)
    assert not alerts


@pytest.mark.anyio
async def test_profile_location_checkins_not_in_watchlist_countries(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_checkins_not_in_watchlist_countries
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_checkins_not_in_watchlist_countries,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_location_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_in_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_in_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_location_in_watchlist_country_city(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_in_watchlist_countrY_city
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_in_watchlist_countrY_city,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_checkins_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_checkins_in_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_in_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_checkins_in_watchlist_country_city(
    person,
    editor,
    watchlist_countries_rules,
    profile_checkins_in_watchlist_country_city
):
    person = await build_person_run_rules(
        person, editor,
        profile_checkins_in_watchlist_country_city,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_person_risk_score_rules_100_expected(
    person,
    editor,
    risk_score_rules
):
    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()
    flags_dict = {
        "illegal_immigration": {
            "category": "Illegal Immigration",
            "severity": 10,
            "sub_categories": []
        }
    }
    flags_dict.setdefault("person", person.id)
    flags = FlagModel(**flags_dict)
    alerts = AlertsModel(person=person)
    evaluation = EvaluationModel(person=person)
    run_all(
        rule_list=risk_score_rules,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await flags.insert()
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags
    assert person.risk_score == 100


@pytest.mark.anyio
async def test_person_risk_score_rules_95_expected(
    person,
    editor,
    risk_score_rules
):
    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()
    flags_dict = {
        "illegal_immigration": {
            "category": "Illegal Immigration",
            "severity": 9.0,
            "sub_categories": []
        },
        "islamic_extremism": {
            "category": "Illegal Immigration",
            "severity": 8.0,
            "sub_categories": []
        },
    }
    flags_dict.setdefault("person", person.id)
    flags = FlagModel(**flags_dict)
    alerts = AlertsModel(person=person)
    evaluation = EvaluationModel(person=person)
    run_all(
        rule_list=risk_score_rules,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await flags.insert()
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags
    assert person.risk_score == 95


@pytest.mark.anyio
async def test_profile_linkedin_work_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_linkedin_work_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_linkedin_work_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_xing_work_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_xing_work_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_xing_work_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_facebook_work_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_facebook_work_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_facebook_work_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_linkedin_work_not_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_linkedin_work_not_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_linkedin_work_not_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_xing_work_not_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_xing_work_not_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_xing_work_not_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_facebook_work_not_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_facebook_work_not_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_facebook_work_not_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_location_and_facebook_work_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_and_facebook_work_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_and_facebook_work_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_profile_with_no_location_watchlist_countries(
    person,
    editor,
    watchlist_countries_rules,
    profile_with_no_location_watchlist_countries
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_location_watchlist_countries,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_with_location_watchlist_countries(
    person,
    editor,
    watchlist_countries_rules,
    profile_with_location_watchlist_countries
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_location_watchlist_countries,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries


@pytest.mark.anyio
async def test_person_teamwork_interpersonal_skills(
    person,
    editor,
    socialble_behaviour_rules
):
    person = PersonModel(**{
        **person,
        **{'last_edited_by': editor}
    })
    await person.insert()
    evaluation_dict = {
        "teamwork": {
            "factors": [
                {
                    "title": "Dries Peeters's experience shows teamwork",
                    "score": 10,
                    "weight": 3
                },
                {
                    "title": "Dries Peeters's posts show team related activities",
                    "score": 10,
                    "weight": 10
                }
            ],
            "score": 10
        },
    }
    evaluation_dict.setdefault("person", person.id)
    evaluation = EvaluationModel(**evaluation_dict)
    alerts = AlertsModel(person=person)
    flags = FlagModel(person=person)
    run_all(
        rule_list=socialble_behaviour_rules,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await evaluation.insert()
    evaluation = await EvaluationModel.find_one(
        EvaluationModel.person.id == person.id)
    assert evaluation.interpersonal_skills


@pytest.mark.anyio
async def test_profile_li_post_jihadist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_li_post_jihadist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_jihadist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    # assert flags.islamic_extremism.severity == 3


@pytest.mark.anyio
async def test_profile_li_post_salafist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_li_post_salafist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_salafist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.anyio
async def test_profile_li_post_no_extreme_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_li_post_no_extreme_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_li_post_no_extreme_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_fb_6_post_jihadist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_6_post_jihadist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_6_post_jihadist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 5


@pytest.mark.anyio
async def test_profile_fb_post_salafist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_post_salafist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_salafist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.anyio
async def test_profile_fb_post_no_extreme_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_post_no_extreme_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_no_extreme_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_instagram_post_jihadist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_post_jihadist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_post_jihadist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 3


@pytest.mark.anyio
async def test_profile_instagram_3_post_salafist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_3_post_salafist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_3_post_salafist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 2


@pytest.mark.anyio
async def test_profile_instagram_post_jihadist_text_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_post_jihadist_text_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_post_jihadist_text_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 4


@pytest.mark.anyio
async def test_profile_instagram_3_post_salafist_text_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_3_post_salafist_text_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_3_post_salafist_text_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 5


@pytest.mark.anyio
async def test_profile_instagram_post_no_extreme_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_post_no_extreme_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_post_no_extreme_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_with_jihadist_intro(
    person,
    editor,
    islamic_extremism_rules,
    profile_with_jihadist_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_jihadist_intro,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_with_salafist_intro(
    person,
    editor,
    islamic_extremism_rules,
    profile_with_salafist_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_salafist_intro,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_with_jihadist_intro_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_with_jihadist_intro_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_jihadist_intro_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_with_salafist_intro_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_with_salafist_intro_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_salafist_intro_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_with_no_foodie_intro_no_islamic_extremism(
    person,
    editor,
    islamic_extremism_rules,
    profile_with_no_foodie_intro
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_no_foodie_intro,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.xfail(reason="Test fails due to 500 response from DS app. Review needed")
@pytest.mark.anyio
async def test_profile_fb_page_jihadist(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_page_jihadist
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_jihadist,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 3


@pytest.mark.anyio
async def test_profile_fb_page_salafist(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_page_salafist
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_salafist,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 1


@pytest.mark.anyio
async def test_profile_fb_page_jihadist_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_page_jihadist_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_jihadist_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 3


@pytest.mark.anyio
async def test_profile_fb_page_salafist_non_arabic_term(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_page_salafist_non_arabic_term
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_salafist_non_arabic_term,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 4


@pytest.mark.anyio
async def test_profile_instagram_post_intagram_bio_multiple_salafist_text(
    person,
    editor,
    islamic_extremism_rules,
    profile_instagram_post_intagram_bio_multiple_salafist_text
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_post_intagram_bio_multiple_salafist_text,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 7


@pytest.mark.anyio
async def test_profile_fb_page_not_foodie_no_islamic_extremism(
    person,
    editor,
    islamic_extremism_rules,
    profile_fb_page_not_foodie
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_not_foodie,
        islamic_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert not flags


@pytest.mark.anyio
async def test_profile_fb_page_designated_group_a(
    person,
    editor,
    extremism_designated_groups_rules,
    profile_fb_page_designated_group_a
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_designated_group_a,
        extremism_designated_groups_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 4


@pytest.mark.anyio
async def test_profile_fb_page_designated_group_b(
    person,
    editor,
    extremism_designated_groups_rules,
    profile_fb_page_designated_group_b
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_designated_group_b,
        extremism_designated_groups_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 2


@pytest.mark.anyio
async def test_profile_following_fb_page_designated_group_a(
    person,
    editor,
    extremism_designated_groups_rules,
    profile_following_fb_page_designated_group_a
):
    person = await build_person_run_rules(
        person, editor,
        profile_following_fb_page_designated_group_a,
        extremism_designated_groups_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 4


@pytest.mark.anyio
async def test_profile_following_fb_page_designated_group_b(
    person,
    editor,
    extremism_designated_groups_rules,
    profile_following_fb_page_designated_group_b
):
    person = await build_person_run_rules(
        person, editor,
        profile_following_fb_page_designated_group_b,
        extremism_designated_groups_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.islamic_extremism
    assert flags.islamic_extremism.severity == 2


@pytest.mark.anyio
async def test_profile_instagram_post_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_instagram_post_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_instagram_post_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_linkedin_post_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_linkedin_post_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_linkedin_post_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_fb_post_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_fb_post_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_post_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_fb_page_weapon_profile_photo(
    person,
    editor,
    weapons_extremism_rules,
    profile_fb_page_weapon_profile_photo
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_weapon_profile_photo,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_fb_page_weapon_cover_photo(
    person,
    editor,
    weapons_extremism_rules,
    profile_fb_page_weapon_cover_photo
):
    person = await build_person_run_rules(
        person, editor,
        profile_fb_page_weapon_cover_photo,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_with_cover_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_with_cover_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_cover_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_with_profile_picture_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_with_profile_picture_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_profile_picture_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


@pytest.mark.anyio
async def test_profile_with_fb_profile_picture_weapons(
    person,
    editor,
    weapons_extremism_rules,
    profile_with_fb_profile_picture_weapons
):
    person = await build_person_run_rules(
        person, editor,
        profile_with_fb_profile_picture_weapons,
        weapons_extremism_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.weapons


async def build_person_run_rules(person, editor, profile_data, rule_list):
    person_data = {**person, **
                   profile_data}
    person = PersonModel(**{
        **person_data,
        **{'last_edited_by': editor}
    })
    await person.insert()
    alerts = AlertsModel(person=person)
    evaluation = EvaluationModel(person=person)
    flags = FlagModel(person=person)
    await async_run_all(
        rule_list=rule_list,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await evaluation.insert()
    try:
        await alerts.insert()
    except Exception:
        alerts = AlertsModel(person=person)
    try:
        await flags.insert()
    except Exception:
        flags = FlagModel(person=person)
    return person


async def sync_build_person_run_rules(person, editor, profile_data, rule_list):
    person_data = {**person, **
                   profile_data}
    person = PersonModel(**{
        **person_data,
        **{'last_edited_by': editor}
    })
    await person.insert()
    alerts = AlertsModel(person=person)
    evaluation = EvaluationModel(person=person)
    flags = FlagModel(person=person)
    run_all(
        rule_list=rule_list,
        defined_variables=PersonVariables(person, alerts, evaluation, flags),
        defined_actions=PersonActions(person, alerts, evaluation, flags))
    await person.save_changes()
    await evaluation.insert()
    try:
        await alerts.insert()
    except Exception:
        alerts = AlertsModel(person=person)
    try:
        await flags.insert()
    except Exception:
        flags = FlagModel(person=person)
    return person
