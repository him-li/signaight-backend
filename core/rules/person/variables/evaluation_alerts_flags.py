from business_rules.variables import boolean_rule_variable

from .base import PersonBaseVariables


class EvaluationAlertsFlagsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has evaluation or alerts'
    )
    def person_with_evaluation_alerts(self):
        alerts = True if self.alerts else False
        evaluation = True if self.evaluation else False

        if alerts or evaluation:
            return True
        else:
            return False

    @boolean_rule_variable(
        label='Person has flags'
    )
    def person_with_flags(self):
        if _ := self.flag:
            return True
        else:
            return False
