import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_NUMERIC

from core.rules.person.utils import (update_heuristics_score,
                                     check_career_break_duration,
                                     create_position_model_list_unique)

from ..base import PersonBaseActions


class OccupationalInstabilityActions(PersonBaseActions):

    @rule_action()
    def set_occupational_instability_job_hopper(self):

        heuristic = {
            "title": "Job Hopper",
            "description": ("{} frequent job changes are interpreted"
                            " as an indication for instability.").format(
                                self.get_person_name()),
            "score": 0
        }
        try:
            positions = create_position_model_list_unique(self.person)
            if (not positions or len(positions) < 2 or
                    not isinstance(positions, list)):
                return
            positions.sort(key=lambda position: position.period.date_from)
            positions.reverse()
        except Exception:
            return

        # Calculate the duration of each workplace and check the last two
        last_two_durations_short = True
        workplaces_within_24_months = 0
        companies_last_24_months = []
        current_date = pendulum.now().start_of('month')
        two_years_ago = current_date.subtract(months=24)
        company_durations = {}

        for position in positions:
            start = pendulum.parse(position.period.date_from,
                                   strict=False).start_of('month')
            try:
                end = (pendulum.parse(
                    position.period.date_to,
                    strict=False).start_of('month') if
                    position.period.date_to else current_date)
            except Exception:
                end = pendulum.now().start_of("month")
            duration = end.diff(start).in_months()

            # Check if the position is within the last 24 months
            if start > two_years_ago or (start <= two_years_ago and
                                         end > two_years_ago):
                workplaces_within_24_months += 1
                companies_last_24_months.append(
                    getattr(position, 'company_name', 'Unknown'))

            # Check the last two positions for short duration
            if positions.index(position) < 2:
                if duration >= 24:
                    last_two_durations_short = False

            company_name = getattr(position, 'company_name', 'Unknown')
            if company_name not in company_durations:
                company_durations[company_name] = 0
            company_durations[company_name] += duration

        stable_company = False

        # Check if either of the last two positions was at a
        # company with total >= 14 months
        for position_index, position in enumerate(positions):
            if position_index < 2:
                company = getattr(position, 'company_name', 'Unknown')
                if company_durations.get(company, 0) >= 14:
                    stable_company = True
                    break

        # Did any company contribute >= 24 months *within the last 24 months*
            start = pendulum.parse(
                position.period.date_from, strict=False).start_of('month')
            try:
                end = (pendulum.parse(
                    position.period.date_to, strict=False).start_of('month')
                    if position.period.date_to else current_date)
            except Exception:
                end = pendulum.now().start_of('month')

            # Intersect with last 24 months
            if end <= two_years_ago:
                continue
            effective_start = max(start, two_years_ago)
            effective_end = min(end, current_date)
            duration_within_window = effective_end.diff(
                effective_start).in_months()
            position_duration = end.diff(start).in_months()

            if duration_within_window >= 24:
                stable_company = True
                break
            elif position_duration >= 24:
                workplaces_within_24_months -= 1

        if last_two_durations_short and not stable_company:
            if workplaces_within_24_months == 2:
                heuristic['score'] = 6
            elif workplaces_within_24_months == 3:
                heuristic['score'] = 8
            elif workplaces_within_24_months >= 4:
                heuristic['score'] = 10

            self.alerts.occupational_instability = update_heuristics_score(
                self.alerts.occupational_instability, heuristic)

    @rule_action(params={
        "career_break_duration": FIELD_NUMERIC,
        "years_prior": FIELD_NUMERIC
    })
    def set_person_career_break(self, career_break_duration, years_prior):
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return
            positions.sort(key=lambda position: position.period.date_to)
        except Exception:
            return
        carrer_break_date_to = check_career_break_duration(
            positions,
            career_break_duration,
            years_prior)
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return
            positions.sort(key=lambda position: position.period.date_from)
        except Exception:
            return
        carrer_break_date_from = check_career_break_duration(
            positions,
            career_break_duration,
            years_prior)
        positions.reverse()

        if carrer_break_date_to and carrer_break_date_from:
            if carrer_break_date_from >= career_break_duration:
                heuristic = {
                    "title": "Career break",
                    "description": "{} with career break".format(
                        self.get_person_name()),
                    "score": 3
                }
                if (carrer_break_date_from >= 52 and
                        carrer_break_date_from < 61):
                    heuristic['score'] = round(3 * 1.2, 0)
                if (carrer_break_date_from >= 61 and
                        carrer_break_date_from < 78):
                    heuristic['score'] = round(3 * 1.4, 0)
                if (carrer_break_date_from >= 78 and
                        carrer_break_date_from < 104):
                    heuristic['score'] = round(4 * 1.6, 0)
                if (carrer_break_date_from >= 104 and
                        carrer_break_date_from < 130):
                    heuristic['score'] = round(4 * 1.7, 0)
                if (carrer_break_date_from >= 130 and
                        carrer_break_date_from < 156):
                    heuristic['score'] = round(5 * 1.8, 0)
                if carrer_break_date_from >= 156:
                    heuristic['score'] = round(5 * 2, 0)

                self.alerts.occupational_instability = update_heuristics_score(
                    self.alerts.occupational_instability, heuristic)
