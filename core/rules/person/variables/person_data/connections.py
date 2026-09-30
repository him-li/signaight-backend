from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class ConnectionsVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_with_connections(self):
        try:
            if self.person.connections:
                return True
        except Exception:
            pass
        return False
