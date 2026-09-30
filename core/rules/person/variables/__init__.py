from .alerts import AlertsVariables
from .heuristics import HeuristicsVariables
from .person_data import PersonDataVariables
from .evaluation_alerts_flags import EvaluationAlertsFlagsVariables
from .flags import FlagsVariables


class PersonVariables(AlertsVariables,
                      HeuristicsVariables,
                      PersonDataVariables,
                      EvaluationAlertsFlagsVariables,
                      FlagsVariables
                      ):
    pass
