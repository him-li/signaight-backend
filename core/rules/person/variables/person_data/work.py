from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_TEXT

from core.rules.person.utils import (
    create_skills_model_list, create_positions_list_additive)

from ..base import PersonBaseVariables


class SkillsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has specific skill',
        params={
            "skill": FIELD_TEXT
        }
    )
    def person_has_specific_skill(self, skill):
        try:
            skills = create_skills_model_list(self.person)
            for skill_model in skills:
                if skill_model.name.lower() == skill.lower():
                    return True
            return False
        except Exception:
            return False

    @boolean_rule_variable(
        label='Person has skills in profile',
    )
    def person_has_skills_in_profile(self):
        try:
            skills = create_skills_model_list(self.person)
            if skills:
                return True
        except Exception:
            pass
        return False


class PositionsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has positions in profile'
    )
    def person_has_positions(self):
        try:
            positions = create_positions_list_additive(self.person)
            if positions:
                return True
        except Exception:
            pass
        return False


class WorkVariables(SkillsVariables, PositionsVariables):
    pass
