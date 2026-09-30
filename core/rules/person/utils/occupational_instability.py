import pendulum

from core.logging import logger


def check_career_break_duration(positions, career_break_duration, years_prior):
    now = pendulum.now()
    covid_years = [2021, 2022]
    for position in positions:
        try:
            date_from = pendulum.parse(position.period.date_from, strict=False)
            if date_from.year in covid_years:
                continue
            if (now - date_from).in_years() < years_prior:
                if position.company_name.lower() == "career break":
                    try:
                        duration = pendulum.duration(
                            years=(int(position.duration.years) if
                                   (position.duration.years)
                                   else 0),
                            months=(int(position.duration.months) if
                                    (position.duration.months) else 0)
                        ).in_weeks()
                    except Exception:
                        duration = 0
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
                    period = (end - start).in_weeks()
                    if duration >= career_break_duration:
                        return duration
                    if period >= career_break_duration:
                        return period
        except Exception:
            pass
    try:
        initial_work_date = pendulum.parse(positions[0].period.date_from,
                                           strict=False).start_of('month')
        working_delta_end_date = pendulum.now().start_of('month')
        working_delta = (working_delta_end_date - initial_work_date).in_weeks()
        longest_work_duration_weeks = None
        for position in positions:
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
            if start.year in covid_years or end.year in covid_years:
                continue
            period = (end - start).in_weeks()
            if (not longest_work_duration_weeks or
                    period > longest_work_duration_weeks):
                longest_work_duration_weeks = period

        if longest_work_duration_weeks >= working_delta:
            return 0
    except Exception as e:
        logger.info(e)

    for i in range(len(positions) - 1):
        end_current = positions[i].period.date_to
        start_next = positions[i + 1].period.date_from

        # If there is no end date, the position is ongoing
        if not end_current or str(end_current).lower() == 'present':
            continue

        if (now - start).in_years() > years_prior:
            continue

        try:
            try:
                end_current_date = pendulum.parse(
                    end_current, strict=False)
            except Exception:
                end_current_date = now
            start_next_date = pendulum.parse(start_next, strict=False)
            if (start_next_date.year in covid_years or
                    end_current_date.year in covid_years):
                continue
            if (now - start_next_date).in_years() < years_prior:
                gap_weeks = (start_next_date - end_current_date).in_weeks()
                if gap_weeks:
                    try:
                        end_previous_date = pendulum.parse(
                            positions[i-1].period.date_to, strict=False)
                    except Exception:
                        end_previous_date = None
                    if end_previous_date:
                        if gap_weeks > career_break_duration:
                            return gap_weeks
        except Exception:
            continue
    return 0
