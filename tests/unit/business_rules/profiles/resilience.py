import pytest


@pytest.fixture
def profile_2_positions_resilience():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2023-12-01"
                            },
                            "duration": {
                                "years": 0,
                                "months": 7
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2022-01-01",
                                "date_to": "2022-11-01"
                            },
                            "duration": {
                                "months": 11
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_2_skills_resilience():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Teamwork",
                            "endorser_count": 6
                        },
                        {
                            "name": "Interpersonal Skills",
                            "endorser_count": 6
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_no_resilience():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                }
            }
        }
    }
