from .alerts import AlertsActions
from .heuristics import HeuristicsActions
from .score_compatibility import ScoreCompatibilityActions
from .flags import FlagsActions


class PersonActions(AlertsActions,
                    HeuristicsActions,
                    ScoreCompatibilityActions,
                    FlagsActions
                    ):
    pass
