from business_rules.actions import rule_action
from business_rules.fields import FIELD_TEXT

from core.rules.person.utils import (
    update_evaluation_factors,
    update_evaluation_factors_weighted_average,
    calculate_skill_score,
    create_skills_model_list
)

from ..base import PersonBaseActions


class SkillsActions(PersonBaseActions):

    @rule_action(
        params={
            "skill": FIELD_TEXT
        }
    )
    def set_person_with_specific_skill(self, skill):
        skills = create_skills_model_list(self.person)
        for skill_model in skills:
            if skill_model.name.lower() == skill.lower():
                score = calculate_skill_score(skill, skill_model)

                if score:
                    factor = {
                        "title": "{} has the skill {skill} in "
                        "social media".format(
                            self.get_person_name(), skill=skill),
                        "score": score
                    }
                    if skill.lower() == 'teamwork':
                        factor['weight'] = 12
                        self.evaluation.teamwork = (
                            update_evaluation_factors_weighted_average(
                                self.evaluation.teamwork, factor))
                    elif skill.lower() == 'decision making':
                        self.evaluation.decision_making = (
                            update_evaluation_factors(
                                self.evaluation.decision_making, factor
                            ))
