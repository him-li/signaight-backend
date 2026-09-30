from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class ResilienceVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_has_data_for_tuned_resilience_score(self):
        person = self.person
        try:
            try:
                work = person.biographic_details.work
                try:
                    if work.linkedin_work.positions:
                        return True
                except Exception:
                    pass
                try:
                    if work.linkedin_work.skills:
                        return True
                except Exception:
                    pass
            except Exception:
                pass

        except Exception:
            pass
        return False
