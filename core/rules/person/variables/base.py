from business_rules.variables import BaseVariables

# from core.models import PersonModel, AlertsModel, EvaluationModel


class PersonBaseVariables(BaseVariables):

    def __init__(
            self,
            person,
            alerts,
            evaluation,
            flag
    ):
        self.person = person
        self.alerts = alerts
        self.evaluation = evaluation
        self.flag = flag
