# flake8: noqa
import pytest


@pytest.fixture
def profile_2_positions_curiosity():
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
def profile_with_2_skills_curiosity():
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
def profile_with_check_ins_curiosity():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Budapest",
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIyMDY3OTE4NjM1MjQ3OA==",
                            "title": "Elafonisi Beach",
                            "subtitle": "Yialós, Khania, Greece\nVisited on June 29, 2019",
                            "url": "https://www.facebook.com/pages/Elafonisi-Beach/1513535772033282",
                            "region": "Yialós, Khania, Greece",
                            "date": "2019-06-29"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNjM3NzE0OTY4NDI1MA==",
                            "title": "Stuhleck",
                            "subtitle": "Spital Am Semmering, Steiermark, Austria\nVisited on February 16, 2018",
                            "url": "https://facebook.com/stuhleck",
                            "region": "Spital Am Semmering, Steiermark, Austria",
                            "date": "2018-02-16"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNDgzNTc4OTAzMTE5Nw==",
                            "title": "Vienna, Austria",
                            "subtitle": "Vienna\nVisited on August 30, 2017",
                            "url": "https://www.facebook.com/pages/Vienna-Austria/111165112241092",
                            "region": "Vienna",
                            "date": "2017-08-30"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNzkwOTAxMzc4NjE0NQ==",
                            "title": "Puertito de Güimar",
                            "subtitle": "Spain\nVisited on August 16, 2015",
                            "url": "https://www.facebook.com/pages/Puertito-de-G%C3%BCimar/191570397564890",
                            "region": "Spain",
                            "date": "2015-08-16"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNjQ5ODU5NTI0NjU2Mw==",
                            "title": "Gino Sopron",
                            "subtitle": "Sopron\nVisited on February 21, 2015",
                            "url": "https://facebook.com/ginosopron",
                            "region": "Sopron",
                            "date": "2015-02-21"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNjQ5MDU5NjIwNjU5Mg==",
                            "title": "Nyárliget",
                            "subtitle": "Sarród, Gyor-Moson-Sopron, Hungary\nVisited on February 20, 2015",
                            "url": "https://www.facebook.com/pages/Ny%C3%A1rliget/470954942917542",
                            "region": "Sarród, Gyor-Moson-Sopron, Hungary",
                            "date": "2015-02-20"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNTIyMTUwOTQ4MDIxNw==",
                            "title": "Dragrace Fertőszentmiklós",
                            "subtitle": "Fertoszentmiklos\nVisited on September 28, 2014",
                            "url": "https://facebook.com/gyorsulas",
                            "region": "Fertoszentmiklos",
                            "date": "2014-09-28"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNDU3NzM2ODg5NzEwNQ==",
                            "title": "VOLT Fesztivál Official",
                            "subtitle": "Sopron\nVisited on July 6, 2014",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Sopron",
                            "date": "2014-07-06"
                        },
                        {
                            "id": "Iguazu==",
                            "title": "Iguazu National Park",
                            "subtitle": "Parana\nVisited on July 6, 2013",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Parana",
                            "date": "2013-07-06"
                        },
                        {
                            "id": "Rocky Mountain National Park ==",
                            "title": "Rocky Mountain National Park",
                            "subtitle": "Colorado\nVisited on July 6, 2013",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Colorado",
                            "date": "2012-07-06"
                        },
                        {
                            "id": "Rocky Mountain National Park ==",
                            "title": "Rocky Mountain National Park",
                            "subtitle": "Colorado\nVisited on July 6, 2013",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Colorado",
                            "date": "2012-07-06"
                        },
                        {
                            "id": "Bromo Tengger Semeru National Park ==",
                            "title": "Bromo Tengger Semeru National Park",
                            "subtitle": "Indonesia\nVisited on July 6, 2013",
                            "country": "Indonesia",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Asia",
                            "date": "2012-07-06"
                        },
                        {
                            "id": "Picos de Europa National Park ==",
                            "title": "Picos de Europa National Park",
                            "subtitle": "Spain\nVisited on July 6, 2013",
                            "country": "Spain",
                            "url": "https://facebook.com/VOLTFesztival",
                            "region": "Europe",
                            "date": "2012-07-06"
                        },
                    ]
                },
                "hometown": {
                    "fb_hometown": "Sopron"
                }
            }
        }
    }


@pytest.fixture
def profile_no_curiosity():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                }
            }
        }
    }
