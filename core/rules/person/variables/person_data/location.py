from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class LocationVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has checkins'
    )
    def person_has_checkins(self):
        try:
            if self.person.personal_details.location.check_ins:
                return True
        except Exception:
            pass
        return False
