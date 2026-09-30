from copy import deepcopy
import pendulum


def check_min_experience(positions):
    filtered_positions = [
        position for position in deepcopy(positions)
        if all(keyword not in position.title.lower() for keyword in
               ['internship', 'intern', 'summer job'])]
    try:
        start_date = pendulum.parse(
            filtered_positions[len(filtered_positions)-1].period.date_from,
            strict=False)
    except Exception:
        return 0
    try:
        end_date = pendulum.parse(filtered_positions[0].period.date_to,
                                  strict=False)
    except Exception:
        end_date = pendulum.now()
    experience_months = (end_date - start_date).in_months()

    return experience_months
