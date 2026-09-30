from business_rules.variables import boolean_rule_variable

from ..base import PersonBaseVariables


class CriminalRecordsVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def has_criminal_records(self):
        p_d = self.person.personal_details
        n_s = self.person.network_signature
        try:
            if p_d.additional_details.eumw_details:
                return True
        except Exception:
            pass
        try:
            if profiles := n_s.matched_profiles:
                if profiles.interpol and profiles.interpol.primary_candidate:
                    return True
                if profiles.eumw and profiles.eumw.primary_candidate:
                    return True
        except Exception:
            pass
        try:
            if p_d.additional_details.interpol_details:
                return True
        except Exception:
            pass
        return False
