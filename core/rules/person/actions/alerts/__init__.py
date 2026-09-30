from .anti_country_statements import AntiCountiStatementsActions
from .ineligible_occupation import IneligibleOccupationActions
from .occupational_instability import OccupationalInstabilityActions
from .strong_affinity_with_country import StrongAffinityWithCountryActions
from .criminal_records import CriminalRecordsActions


class AlertsActions(AntiCountiStatementsActions,
                    IneligibleOccupationActions,
                    OccupationalInstabilityActions,
                    StrongAffinityWithCountryActions,
                    CriminalRecordsActions):
    pass
