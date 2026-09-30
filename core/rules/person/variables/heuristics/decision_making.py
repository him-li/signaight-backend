from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_SELECT

from ..base import PersonBaseVariables


class DecisionMakingVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has specific background',
        params=[{
            'name': 'titles',
            'field_type': FIELD_SELECT
        }]
    )
    def person_with_specific_background(self, titles):
        try:
            positions = (self.person.biographic_details.work.linkedin_work.
                         positions)
            if not positions or not isinstance(positions, list):
                return False
        except Exception:
            return False
        for position in positions:
            for title in titles:
                if title in position.title.lower():
                    return True
        return False
