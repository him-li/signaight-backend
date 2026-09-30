# flake8: noqa
import pytest


@pytest.fixture
def education_in_israel():
    return {
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Tel Aviv University",
                        "duration": {
                            "years": 1,
                            "months": 4
                        },
                        "period": {
                            "date_from": "2021-09-01",
                            "date_to": "2022-12-25"
                        }
                    }
                ]
            },
        }
    }


@pytest.fixture
def education_in_israel_duration_only():
    return {
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Tel Aviv University",
                        "duration": {
                            "years": 1,
                            "months": 4
                        },
                    }
                ]
            },
        }
    }


@pytest.fixture
def education_in_israel_period_only():
    return {
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Tel Aviv University",
                        "period": {
                            "date_from": "2021-09-01",
                            "date_to": "2022-12-25"
                        }
                    }
                ]
            },
        }
    }


@pytest.fixture
def education_in_israel_short_period_only():
    return {
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Tel Aviv University",
                        "period": {
                            "date_from": "2021-09-01",
                            "date_to": "2021-11-25"
                        }
                    }
                ]
            },
        }
    }


@pytest.fixture
def education_not_in_israel():
    return {
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Tel Aviv University",
                        "period": {
                            "date_from": "2021-09-01",
                            "date_to": "2021-11-25"
                        }
                    }
                ]
            },
        }
    }
