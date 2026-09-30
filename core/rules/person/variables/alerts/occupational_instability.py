import pendulum
from business_rules.variables import (
    boolean_rule_variable,
    numeric_rule_variable)
from business_rules.fields import FIELD_NUMERIC

from core.rules.person.utils import (
    check_career_break_duration, create_position_model_list_unique)

from ..base import PersonBaseVariables


class OccupationalInstabilityVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label=('Frequent job changes are interpreted'
               ' as an indication for instability.'),
        params=[
            {
                'field_type': FIELD_NUMERIC,
                'name': 'last_positions_qty',
                'label': 'Last positions qty'
            },
            {
                'field_type': FIELD_NUMERIC,
                'name': 'period',
                'label': 'Period in months'
            }
        ]
    )
    def linkedin_work_change_frequency_for_period(self,
                                                  last_positions_qty,
                                                  period):
        period = pendulum.duration(months=period)
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return False
            # NOTE: potentially unstable cause position.period is optional
            # TODO: more tests coverage needed and maybe check for values presence # noqa
            positions.sort(key=lambda position: position.period.date_to)
            positions.reverse()
        except Exception:
            return False
        position_change_count_date_to = 0
        for i, position in enumerate(positions):
            if i < last_positions_qty:
                if position.duration:
                    duration = pendulum.duration(
                        years=(int(position.duration.years)
                               if position.duration.years else 0),
                        months=(int(position.duration.months)
                                if position.duration.months else 0)
                    )
                else:
                    duration = pendulum.duration(seconds=0)
                try:
                    start = pendulum.parse(position.period.date_from,
                                           strict=False).start_of('month')
                except Exception:
                    start = pendulum.now().start_of('month')
                try:
                    end = pendulum.parse(
                        position.period.date_to,
                        strict=False).start_of('month')
                except Exception:
                    end = pendulum.now().start_of('month')
                position_period = (end - start)
                if (duration.in_days() <= period.in_days()
                        or position_period.in_days() <= period.in_days()):
                    position_change_count_date_to += 1
                else:
                    break
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return False
            # NOTE: potentially unstable cause position.period is optional
            # TODO: more tests coverage needed and maybe check for values presence # noqa
            positions.sort(key=lambda position: position.period.date_from)
            positions.reverse()
        except Exception:
            return False
        position_change_count_date_from = 0
        for i, position in enumerate(positions):
            if i < last_positions_qty:
                if position.duration:
                    duration = pendulum.duration(
                        years=(int(position.duration.years)
                               if position.duration.years else 0),
                        months=(int(position.duration.months)
                                if position.duration.months else 0)
                    )
                else:
                    duration = pendulum.duration(seconds=0)
                try:
                    start = pendulum.parse(position.period.date_from,
                                           strict=False).start_of('month')
                except Exception:
                    start = pendulum.now().start_of('month')
                try:
                    end = pendulum.parse(
                        position.period.date_to,
                        strict=False).start_of('month')
                except Exception:
                    end = pendulum.now().start_of('month')
                position_period = (end - start)
                if (duration.in_days() <= period.in_days()
                        or position_period.in_days() <= period.in_days()):
                    position_change_count_date_from += 1
                else:
                    break
        return True if (
            position_change_count_date_to >= last_positions_qty and
            position_change_count_date_from >= last_positions_qty) else False

    @numeric_rule_variable(
        label=("Person has career break periods"),
        params=[
            {
                'field_type': FIELD_NUMERIC,
                'name': 'career_break_duration',
                'label': 'Min duration of career break'
            },
            {
                'field_type': FIELD_NUMERIC,
                'name': 'years_prior',
                'label': 'Number of years prior to check'
            }
        ]
    )
    def linkedin_career_break(self, career_break_duration, years_prior):
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return 0
            positions.sort(key=lambda position: position.period.date_from)
        except Exception:
            return 0
        carrer_break = check_career_break_duration(positions,
                                                   career_break_duration,
                                                   years_prior)
        positions.reverse()
        return carrer_break
