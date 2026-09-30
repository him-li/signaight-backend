import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT

from core.rules.person.utils import (update_evaluation_factors,
                                     create_position_model_list_additive
                                     )

from ..base import PersonBaseActions


class DecisionMakingActions(PersonBaseActions):

    @rule_action(params={
        "management_titles": FIELD_SELECT
    })
    def set_person_with_management_positions(self, management_titles):

        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return
        except Exception:
            return
        factor = {
            "title": "{} has management positions".format(
                self.get_person_name()),
            "score": 0
        }
        manager_period = 0
        manager_positions = 0
        titles_period = 0
        titles_positions = 0
        for position in positions:
            for title in management_titles:
                if title in position.title.lower():
                    try:
                        if duration := position.duration:
                            years = duration.years
                            period = duration.months if duration.months else 0
                            if years:
                                period = years * 12 + period
                        elif position.period:
                            start_date = position.period.date_from
                            end_date = (position.period.date_to if
                                        position.period.date_to and
                                        position.period.date_to !=
                                        "Present" else
                                        pendulum.now().to_date_string())
                            period = (pendulum.parse(end_date) -
                                      pendulum.parse(start_date)).in_months()
                        titles_period += period
                        titles_positions += 1
                        break
                    except Exception:
                        pass

                elif "manager" in position.title.lower():
                    try:
                        if duration := position.duration:
                            years = duration.years
                            period = duration.months if duration.months else 0
                            if years:
                                period = years * 12 + period
                        elif position.period:
                            start_date = position.period.date_from
                            try:
                                end_date = (position.period.date_to if
                                            position.period.date_to and
                                            position.period.date_to !=
                                            "Present" else
                                            pendulum.now().to_date_string())
                            except Exception:
                                end_date = pendulum.now().to_date_string()
                            try:
                                period = (pendulum.parse(end_date) -
                                          pendulum.parse(start_date)
                                          ).in_months()
                            except Exception:
                                pass
                        manager_period += period
                        manager_positions += 1
                        break
                    except Exception:
                        pass

        period_score = ((manager_period/12) * 1.5) + ((titles_period/12) * 3.5)
        positions_score = (0.8 * titles_positions) + (0.4 * manager_positions)
        factor['score'] = period_score + positions_score

        if factor['score'] > 10:
            factor['score'] = 10

        if factor['score']:
            factor['score'] = round(factor['score'], 0)
            self.evaluation.decision_making = update_evaluation_factors(
                self.evaluation.decision_making, factor)
