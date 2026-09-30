from business_rules.actions import rule_action
from business_rules.fields import FIELD_NUMERIC, FIELD_SELECT
from core.models.person import Compatibility

from .base import PersonBaseActions


class ScoreCompatibilityActions(PersonBaseActions):

    @rule_action(params={
        "evaluation_weights": FIELD_SELECT,
        "alerts_weights": FIELD_SELECT,
        "unweighted_alerts": FIELD_SELECT
    })
    def set_person_score(self,
                         evaluation_weights,
                         alerts_weights,
                         unweighted_alerts):
        alerts = self.alerts.model_dump()
        evaluation = self.evaluation.model_dump()

        # Score based on evaluation and alerts qty and avg
        alerts_len = sum(1 for key, value in alerts.items() if key != 'person'
                         and key != 'id' and key not in unweighted_alerts
                         and value is not None)
        evaluation_len_greater_8 = sum(
            1 for key, value in evaluation.items() if
            key != 'person' and key != 'id' and
            value is not None and isinstance(
                value, dict) and 'score' in value
            and value.get("score") >= 8)
        evaluation_len = sum(1 for key, value in evaluation.items() if
                             key != 'person' and key != 'id' and
                             value is not None)
        evaluation_sum = sum(value['score'] * evaluation_weights[key] for
                             key, value in evaluation.items() if
                             key != 'person' and key != 'id' and
                             isinstance(value, dict))
        alert_sum = sum(value['score'] * alerts_weights[key] for
                        key, value in alerts.items() if
                        key != 'person' and key != 'id' and
                        alerts_weights.get(key) and isinstance(value, dict)
                        and 'score' in value)
        evaluation_weight_sum = sum(
            value for key, value in evaluation_weights.items() if
            evaluation[key])
        alerts_weight_sum = sum(
            value for key, value in alerts_weights.items() if alerts[key])

        # Weighted scores
        weighted_evaluation = (evaluation_sum /
                               evaluation_weight_sum if
                               evaluation_len else
                               evaluation_sum / 1) * 3
        evaluation_len_score = evaluation_len_greater_8 * 5
        weighted_alert = (alert_sum / (alerts_len * alerts_weight_sum) if
                          alerts_len and alerts_weight_sum else
                          alert_sum / 1) * 3
        alerts_len_score = alerts_len * 5

        score_increment = weighted_evaluation + evaluation_len_score
        score_decrement = weighted_alert + alerts_len_score
        if alerts.get("criminal_records"):
            score_decrement += 50

        # Final score and min and max checks
        score = 40 + score_increment - score_decrement
        if score < 0:
            score = 0
        if score > 100:
            score = 100

        self.person.signaight_score = int(round(score, 0))

    @rule_action(params={
        "disqualifying_alerts": FIELD_SELECT,
        "disqualifying_threshold": FIELD_NUMERIC
    })
    def set_person_compatibility(self, disqualifying_alerts,
                                 disqualifying_threshold):
        person = self.person.model_dump()
        alerts = self.alerts.model_dump()

        score = person.get("signaight_score", None)

        def switch_score(score):
            match score:
                case _ if 0 <= score <= 25:
                    return "Disqualified"
                case _ if 25 < score <= 50:
                    return "Low Compatibility"
                case _ if 50 < score <= 75:
                    return "Medium Compatibility"
                case _ if 75 < score:
                    return "High Compatibility"

        if score is not None:
            compatibility = switch_score(score)
            for disqualifying_alert in disqualifying_alerts:
                if (disqualifying_alert in alerts.keys() and
                        alerts.get(disqualifying_alert)):
                    score = alerts.get(disqualifying_alert, {}).get('score')
                    if score >= disqualifying_threshold:
                        compatibility = 'Disqualified'

            self.person.compatibility = Compatibility(compatibility)

    @rule_action()
    def set_person_risk_score(self):
        flags = self.flag.model_dump()
        score = 0
        flag_severities = [flag.get("severity") for key, flag in flags.items(
        ) if flag is not None and key not in ['id', 'revision_id', 'person']]
        try:
            score = (max(flag_severities)*10) + ((len(flag_severities) - 1)*5)
        except Exception:
            pass

        if score:
            self.person.risk_score = int(round(score, 0))
