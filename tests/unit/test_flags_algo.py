import pytest
import pandas
import pendulum
from datetime import datetime
from rich import print
from stringmatch import Match

from core.rules.helpers.education_institutions import EducationInstitutions


@pytest.fixture()
def person_with_il_educational(person):
    person['education'] = {
        'linkedin_schools': [
            {
                'school_name': "Sami Shamoon College of Engineering",
                'degree_name': 'Bachelor of Science',
                'education_field': 'Computer Architecture',
                'linkedin_school_location': 'Beersheba and Ashdod',
                'period': {
                    'date_from': '2014-10',
                    'date_to': '2017-04'
                },
            },
            {
                'school_name': "Princeton University",
                'degree_name': 'Master of Science',
                'education_field': 'Computer Architecture',
                'linkedin_school_location': 'Princeton',
                'period': {
                    'date_from': '2017-09',
                    'date_to': '2021-06'
                },
            }
        ],
        'facebook_schools': [
            {
                'fb_school_name': "Sami Shamoon College",
                'fb_education_field': 'Computer Architecture',
                'fb_school_location': 'Beersheba',
                'period': {
                    'date_from': '2014-10',
                    'date_to': '2017-04'
                },
            }
        ]
    }
    return person


def create_timeline(events):
    now = datetime.now()
    timeline = []
    for event in events:
        if not event:
            timeline.append(None)
            continue
        period = event.get('period', {})
        start = pendulum.parse(
            period.get('date_from', now), strict=False)
        end = pendulum.parse(
            period.get('date_to', now), strict=False)
        timeline.append(pandas.Interval(
            left=pandas.Timestamp(start),
            right=pandas.Timestamp(end),
            closed='both'
        ))
    return pandas.arrays.IntervalArray(timeline)


def find_overlaps(education_linkedin, education_facebook):
    now = datetime.now()
    li_timeline = create_timeline(education_linkedin)
    fb_timeline = create_timeline(education_facebook)

    overlaps = []
    for i, event in enumerate(li_timeline):
        _overlaps = fb_timeline.overlaps(event)
        # skip iteration without overlap
        if not any(_overlaps):
            continue
        # turn overlap index into entities
        for j, overlap in enumerate(_overlaps):
            if not overlap:
                continue
            overlaps.append({
                'origin': education_linkedin[i],
                'check': education_facebook[j]
            })
    match = Match()

    factors = {
        'location': ['linkedin_school_location', 'fb_school_location',],
        'organization': ['school_name', 'fb_school_name'],
    }
    def find_factor_value_by_fields(origin, fields):
        for field in fields:
            if result := origin.get(field):
                return result
        return None

    for overlap in overlaps:
        overlap['result'] = {}
        origin = overlap.get('origin', {})
        check = overlap.get('check', {})
        # use timedelta factor
        o_start = pendulum.parse(
            origin.get('period', {}).get('date_from', now), strict=False)
        o_end = pendulum.parse(origin.get('period', {}).get('date_to', now), strict=False)
        c_start = pendulum.parse(
            check.get('period', {}).get('date_from', now), strict=False)
        c_end = pendulum.parse(check.get('period', {}).get('date_to', now), strict=False)
        overlap['result']['period_delta'] = abs(
            o_start.diff(c_start).in_seconds()
            + o_end.diff(c_end).in_seconds())
        # apply comparison of 3 education factors
        factors_result = []
        for factor, fields in factors.items():
            origin_factor_value = find_factor_value_by_fields(origin, fields)
            check_factor_value = find_factor_value_by_fields(check, fields)
            result = {
                'field': factor,
                'origin': origin_factor_value,
                'check': check_factor_value,
            }
            success, ratio = match.match_with_ratio(
                origin_factor_value,
                check_factor_value
            )
            factors_result.append({
                **result,
                **{'success': success, 'accuracy_ratio': ratio}
            })
    return overlaps


@pytest.mark.anyio
@pytest.mark.skip(reason="No more in game. Maybe later will transformed into another one")
async def test_person_with_il_educations_compare(person_with_il_educational):
    education_linkedin = person_with_il_educational.get('education', {}).get('linkedin_schools', [])
    education_facebook = person_with_il_educational.get('education', {}).get('facebook_schools', [])
    overlaps = find_overlaps(education_linkedin, education_facebook)
    print(overlaps)
    total_time_delta = 0
    total_rating = 0
    for overlap in overlaps:
        total_time_delta += overlap.get('result', {}).get('period_delta', 0)
        total_rating += overlap.get('result', {}).get('ratio', 0)
    total_rating = round(total_rating/len(overlaps))
    print(f"Total timedelta with periods: {total_time_delta} seconds")
    print(f"Total rating: {total_rating}")
    '''
    institutions = EducationInstitutions.get_institution_by_country('IL')
    for school in education_linkedin:
        # affinity with israel
        institution_accuracy = []
        for institrution in institutions:
        factor = 'israel_affinity'
        factor_result
        overlap['result']['factors'] = factors_result
    '''

