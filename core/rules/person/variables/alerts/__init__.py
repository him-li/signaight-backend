from .anti_country_statements import AntiCountryStatementsVariables
from .ineligible_occupation import IneligibleOccupationVariables
from .occupational_instability import OccupationalInstabilityVariables
from .strong_affinity_with_country import StrongAffinityWithCountryVariables
from .criminal_records import CriminalRecordsVariables


class AlertsVariables(AntiCountryStatementsVariables,
                      IneligibleOccupationVariables,
                      OccupationalInstabilityVariables,
                      StrongAffinityWithCountryVariables,
                      CriminalRecordsVariables):
    pass
