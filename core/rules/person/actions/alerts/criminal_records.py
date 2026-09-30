from business_rules.actions import rule_action


from core.rules.person.utils import update_heuristics_score
from ..base import PersonBaseActions


class CriminalRecordsActions(PersonBaseActions):

    @rule_action()
    def set_has_criminal_records(self):
        p_d = self.person.personal_details
        n_s = self.person.network_signature
        criminal_records = 0
        try:
            if p_d.additional_details.eumw_details:
                criminal_records += 1
        except Exception:
            pass
        try:
            if profiles := n_s.matched_profiles:
                if profiles.interpol and profiles.interpol.primary_candidate:
                    criminal_records += 1
                if profiles.eumw and profiles.eumw.primary_candidate:
                    criminal_records += 1
        except Exception:
            pass
        try:
            if p_d.additional_details.interpol_details:
                criminal_records += 1
        except Exception:
            pass

        try:
            if criminal_records:

                heuristic = {
                    "title": ("Criminal Records"),
                    "description": ("{} has criminal records").format(
                        self.get_person_name()),
                    "score": 10
                }

                self.alerts.criminal_records = update_heuristics_score(
                    self.alerts.criminal_records, heuristic)

        except Exception:
            pass
