import pandas
import pendulum
from datetime import datetime
from rich import print
from stringmatch import Match


def create_timeline(events):
    now = datetime.now()
    timeline = []
    for event in events:
        if not event:
            timeline.append(None)
            continue
        start = pendulum.parse(
            event.get('start_month_year', now), strict=False)
        end = pendulum.parse(event.get('end_month_year', now), strict=False)
        timeline.append(pandas.Interval(
            left=pandas.Timestamp(start),
            right=pandas.Timestamp(end),
            closed='both'
        ))
    return pandas.arrays.IntervalArray(timeline)


def timeline_rating(origin, check):
    now = datetime.now()
    origin_timeline = create_timeline(origin)
    check_timeline = create_timeline(check)

    '''
    # Unable to apply Dataframe diff cause:
    # IntervalArray has no 'diff' method. Convert to a suitable dtype prior to calling 'diff'.
    df = pandas.DataFrame({'li': li_timeline,
                   'fb': fb_timeline})
    df.diff()
    '''

    overlaps = []
    for i, event in enumerate(origin_timeline):
        _overlaps = check_timeline.overlaps(event)
        # skip iteration without overlap
        if not any(_overlaps):
            continue
        # turn overlap index into entities
        for j, overlap in enumerate(_overlaps):
            if not overlap:
                continue
            overlaps.append({
                'origin': origin[i],
                'check': check[j]
            })
    match = Match()
    factors = [
        'degree_name', 'fields_of_study_name',
        'organization', 'school_name',
    ]

    for overlap in overlaps:
        overlap['result'] = {}
        origin = overlap.get('origin', {})
        check = overlap.get('check', {})
        # use timedelta factor
        o_start = pendulum.parse(
            origin.get('start_month_year', now), strict=False)
        o_end = pendulum.parse(
            origin.get('end_month_year', now), strict=False)
        c_start = pendulum.parse(
            check.get('start_month_year', now), strict=False)
        c_end = pendulum.parse(check.get('end_month_year', now), strict=False)
        overlap['result']['period_delta'] = abs(
            o_start.diff(c_start).in_seconds()
            + o_end.diff(c_end).in_seconds())
        # apply comparison of 3 education factors
        factors_result = []
        total = 0
        for factor in factors:
            origin_factor = origin.get(factor, '')
            check_factor = check.get(factor, '')
            result = {
                'field': factor,
                'origin': origin_factor,
                'check': check_factor,
            }
            success, ratio = match.match_with_ratio(
                origin_factor,
                check_factor
            )
            factors_result.append({
                **result,
                **{'success': success, 'ratio': ratio}
            })
            total += ratio
        overlap['result']['factors'] = factors_result
        overlap['result']['ratio'] = round(total / len(factors))

    print(overlaps)

    total_time_delta = 0
    total_rating = 0
    for overlap in overlaps:
        total_time_delta += overlap.get('result', {}).get('period_delta', 0)
        total_rating += overlap.get('result', {}).get('ratio', 0)
    total_rating = round(total_rating/len(overlaps))
    print(f"Total timedelta with periods: {total_time_delta} seconds")
    print(f"Total rating: {total_rating}")
