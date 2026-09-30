from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class MoralValuesVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label=("Person has volunteering experience"),
    )
    def person_with_linkedin_volunteering_experience(self):
        try:
            volunteering_experiences = (self.person.biographic_details.work.
                                        linkedin_work.volunteering_experiences)
            if not volunteering_experiences or not isinstance(
                    volunteering_experiences,
                    list):
                return False
            else:
                return True
        except Exception:
            return False
