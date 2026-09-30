from business_rules.actions import BaseActions

class PersonBaseActions(BaseActions):

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

    def get_person_name(self):
        return self.person.personal_details.name.full_name.full_name
