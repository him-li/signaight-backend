# flake8: noqa
import pytest


@pytest.fixture
def profile_with_check_ins():
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
def profile_with_instagram_location_name():
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
                "hometown": {
                    "fb_hometown": "Sopron"
                },
            }
        },
        "posts": [
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIyMDY3OTE4NjM1MjQ3OA==",
                "title": "Elafonisi Beach",
                "subtitle": "Yialós, Khania, Greece\nVisited on June 29, 2019",
                "url": "https://www.facebook.com/pages/Elafonisi-Beach/1513535772033282",
                "instagram_post_location": {
                    "instagram_location_name": "Elafonisi Beach",
                },
                "date": "2019-06-29"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNjM3NzE0OTY4NDI1MA==",
                "title": "Stuhleck",
                "subtitle": "Spital Am Semmering, Steiermark, Austria\nVisited on February 16, 2018",
                "url": "https://facebook.com/stuhleck",
                "instagram_post_location": {
                    "instagram_location_name": "Stuhleck"},
                "date": "2018-02-16"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNDgzNTc4OTAzMTE5Nw==",
                "title": "Vienna, Austria",
                "subtitle": "Vienna\nVisited on August 30, 2017",
                "url": "https://www.facebook.com/pages/Vienna-Austria/111165112241092",
                "instagram_post_location": {
                    "instagram_location_name": "Vienna, Austria"},
                "date": "2017-08-30"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNzkwOTAxMzc4NjE0NQ==",
                "title": "Puertito de Güimar",
                "subtitle": "Spain\nVisited on August 16, 2015",
                "url": "https://www.facebook.com/pages/Puertito-de-G%C3%BCimar/191570397564890",
                "instagram_post_location": {
                    "instagram_location_name": "Puertito de Güimar"},
                "date": "2015-08-16"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNjQ5ODU5NTI0NjU2Mw==",
                "title": "Gino Sopron",
                "subtitle": "Sopron\nVisited on February 21, 2015",
                "url": "https://facebook.com/ginosopron",
                "instagram_post_location": {
                    "instagram_location_name": "Gino Sopron"},
                "date": "2015-02-21"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNjQ5MDU5NjIwNjU5Mg==",
                "title": "Nyárliget",
                "subtitle": "Sarród, Gyor-Moson-Sopron, Hungary\nVisited on February 20, 2015",
                "url": "https://www.facebook.com/pages/Ny%C3%A1rliget/470954942917542",
                "instagram_post_location": {
                    "instagram_location_name": "Nyárliget"},
                "date": "2015-02-20"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNTIyMTUwOTQ4MDIxNw==",
                "title": "Dragrace Fertőszentmiklós",
                "subtitle": "Fertoszentmiklos\nVisited on September 28, 2014",
                "url": "https://facebook.com/gyorsulas",
                "instagram_post_location": {
                    "instagram_location_name": "Dragrace Fertőszentmiklós"},
                "date": "2014-09-28"
            },
            {
                "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIwNDU3NzM2ODg5NzEwNQ==",
                "title": "VOLT Fesztivál Official",
                "subtitle": "Sopron\nVisited on July 6, 2014",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "VOLT Fesztivál Official"},
                "date": "2014-07-06"
            },
            {
                "id": "Iguazu==",
                "title": "Iguazu National Park",
                "subtitle": "Parana\nVisited on July 6, 2013",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "Iguazu National Park"},
                "date": "2013-07-06"
            },
            {
                "id": "Rocky Mountain National Park ==",
                "title": "Rocky Mountain National Park",
                "subtitle": "Colorado\nVisited on July 6, 2013",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "Rocky Mountain National Park"},
                "date": "2012-07-06"
            },
            {
                "id": "Rocky Mountain National Park ==",
                "title": "Rocky Mountain National Park",
                "subtitle": "Colorado\nVisited on July 6, 2013",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "Rocky Mountain National Park"},
                "date": "2012-07-06"
            },
            {
                "id": "Bromo Tengger Semeru National Park ==",
                "title": "Bromo Tengger Semeru National Park",
                "subtitle": "Indonesia\nVisited on July 6, 2013",
                "country": "Indonesia",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "Bromo Tengger Semeru National Park"},
                "date": "2012-07-06"
            },
            {
                "id": "Picos de Europa National Park ==",
                "title": "Picos de Europa National Park",
                "subtitle": "Spain\nVisited on July 6, 2013",
                "country": "Spain",
                "url": "https://facebook.com/VOLTFesztival",
                "instagram_post_location": {
                    "instagram_location_name": "Picos de Europa National Park"},
                "date": "2012-07-06"
            },
        ]
    }


@pytest.fixture
def profile_with_location_not_israel():
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
            }
        }
    }


@pytest.fixture
def profile_with_one_location_in_israel():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Ramat Gan",
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
            }
        }
    }


@pytest.fixture
def profile_with_two_locations_in_israel():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Ramat Gan",
                "current_city_region_country": {
                    "linkedin_location": "Tel Aviv"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
            }
        }
    }


@pytest.fixture
def profile_with_two_locations_in_israel_no_linkedin():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Ramat Gan",
                "current_city": {
                    "fb_current_city": "Tel Aviv"
                },
                'current_lat_long': {
                    "fb_lives_in_lat": "Tel Aviv"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
            }
        }
    }


@pytest.fixture
def profile_with_two_locations_in_israel_no_city():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Israel",
                "current_city": {
                    "fb_current_city": "Haderah"
                },
                'current_lat_long': {
                    "fb_lives_in_lat": "Israel"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
            }
        }
    }


@pytest.fixture
def profile_checkins_in_israel():
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
                            "title": "Haf HaKarmel Beach",
                            "subtitle": "Haifa, Israel\nVisited on June 29, 2019",
                            "url": "https://www.facebook.com/pages/Elafonisi-Beach/1513535772033282",
                            "region": "Haifa, Israel",
                            "date": "2019-06-29"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNjM3NzE0OTY4NDI1MA==",
                            "title": "Tel Aviv University",
                            "subtitle": "Tel Aviv, Israel\nVisited on February 16, 2018",
                            "url": "https://facebook.com/stuhleck",
                            "region": "Tel Aviv, Israel",
                            "date": "2018-02-16"
                        },
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIxNDgzNTc4OTAzMTE5Nw==",
                            "title": "Knesset",
                            "subtitle": "Jerusalem\nVisited on August 30, 2017",
                            "url": "https://www.facebook.com/pages/Vienna-Austria/111165112241092",
                            "region": "Jerusalem",
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
                    ]
                },
                "hometown": {
                    "fb_hometown": "Sopron"
                }
            }
        }
    }


@pytest.fixture
def profile_checkins_not_in_israel():
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
def profile_location_checkins_not_in_watchlist_countries():
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
def profile_location_in_watchlist_country():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Iran",
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
                "hometown": {
                    "fb_hometown": "Sopron"
                }
            }
        }
    }


@pytest.fixture
def profile_location_in_watchlist_countrY_city():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "twitter_location": "Tehran",
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },
                "hometown": {
                    "fb_hometown": "Sopron"
                }
            }
        }
    }


@pytest.fixture
def profile_checkins_in_watchlist_country():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIyMDY3OTE4NjM1MjQ3OA==",
                            "title": "Elafonisi Beach",
                            "subtitle": "Tehran, Iran\nVisited on June 29, 2019",
                            "url": "https://www.facebook.com/pages/Elafonisi-Beach/1513535772033282",
                            "region": "Tehran, Iran",
                            "date": "2019-06-29"
                        },
                    ]
                },

            }
        }
    }


@pytest.fixture
def profile_checkins_in_watchlist_country_city():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "id": "YXBwX2l0ZW06MTMyMDUzMzQ0NzozMDIzMjQ0MjU3OTA6MTAzOjoxMDIyMDY3OTE4NjM1MjQ3OA==",
                            "title": "Elafonisi Beach",
                            "subtitle": "Tehran\nVisited on June 29, 2019",
                            "url": "https://www.facebook.com/pages/Elafonisi-Beach/1513535772033282",
                            "region": "Tehran",
                            "date": "2019-06-29"
                        },
                    ]
                },

            }
        }
    }


@pytest.fixture
def profile_with_google_reviews():
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
                    "google_reviews": [
                        {
                            "address": "Eliezer Kaplan St 4, Tel Aviv-Yafo, Israel",
                            "comment": "",
                            "date": "11/01/2022 13:11:46 (UTC)",
                            "id": "ChZDSUhNMG9nS0VJQ0FnSUNteDRhQ0pREAE",
                            "name": "Beit Sokolov",
                            "lat": 32.0732281,
                            "long": 34.7825482
                        },
                        {
                            "comment": "Rating: 5/5\nFrazer has been looking after our lawn for the last 5 months and it has never looked so good. The results have been far better than with anyone else we've had looking after it in the past. He has also got our unruly hedges under control and dealt with the weeds on our gravel drive. His communication is excellent and he always turns up when he says he will and works hard. Highly recommended.",
                            "date": "28/10/2024 09:51:44 (UTC)",
                            "id": "",
                            "name": "Frazer garden services",
                            "lat": 50.839959199999996,
                            "long": -4.3008842
                        },
                        {
                            "address": "unit 2, Newport Industrial Estate, Launceston PL15 8EX, United Kingdom",
                            "comment": "Rating: 5/5\nExcellent service - fast and invisible repair.",
                            "date": "01/12/2022 22:12:48 (UTC)",
                            "id": "",
                            "name": "Blue Chip Body Repair",
                            "lat": 50.6407624,
                            "long": -4.358811
                        }

                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_with_no_location_watchlist_countries():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "linkedin_country_code": "us",
                "current_city_region_country": {
                    "linkedin_location": "Indianapolis, Indianapolis, United States"
                },
                "current_country": {
                    "linkedin_location_country": "United States"
                },
                "check_ins": {
                    "google_reviews": [
                        {
                            "address": "3443 Dickerson Pike # 430, Nashville, TN 37207",
                            "comment": "Rating: 5/5\nDr. Connelly is an excellent physician. After having heart problems for 25 years, I have found him to be the very best in every way. His bedside manner, professionalism and diagnostics place him at the very top!",
                            "date": "31/10/2022 19:44:31 (UTC)",
                            "id": "ChZDSUhNMG9nS0VJQ0FnSUQwcFlMaVNBEAE",
                            "name": "Tennessee Heart and Vascular - Skyline",
                            "lat": 36.245133599999996,
                            "long": -86.7495311
                        },
                        {
                            "address": "141 Gallatin Pike N, Madison, TN 37115",
                            "comment": "Rating: 5/5\nI went for the first time. Excellent food and service. Highly recommend this restaurant. The shrimp is great!!!",
                            "date": "20/02/2022 00:45:28 (UTC)",
                            "id": "ChZDSUhNMG9nS0VJQ0FnSUNXcklTM1hREAE",
                            "name": "Juicy Seafood & Hibachi Grill",
                            "lat": 36.2648286,
                            "long": -86.7121401
                        },
                        {
                            "address": "1114 Gallatin Pike N, Madison, TN 37115",
                            "comment": "Rating: 1/5\nI made an appointment for December 29 a few weeks ago. I received a call asking call if I wanted an earlier appointment if there was a cancellation. I kept my 29th appointment. I received a text message and confirmed my appointment.\nUpon arriving at 1:00 for my 1:30 appointment, I was told my appointment was canceled because I didn’t confirm it. Apparently confirming twice is not sufficient.\nHowever I suffered a stroke and was in Skyline Hospital. Maybe I failed to answer my phone while I’m there.\nThe cancellation of my appointment without notification is not acceptable. I wanted to use my dental insurance this year. Due to incompetence of this office, I lost at least several hundred dollars.\nRediculous!!!",
                            "date": "29/12/2021 20:12:27 (UTC)",
                            "id": "ChdDSUhNMG9nS0VJQ0FnSUNtM3NlLXdnRRAB",
                            "name": "Thomasson Dental",
                            "lat": 36.279144599999995,
                            "long": -86.70841209999999
                        },
                        {
                            "address": "106 Madison St, Madison, TN 37115",
                            "comment": "Rating: 5/5\nI had excellent food and service. Great job Dos Sisters!",
                            "date": "27/08/2021 17:04:21 (UTC)",
                            "id": "ChdDSUhNMG9nS0VJQ0FnSUM2b0lXVF9nRRAB",
                            "name": "Dos Sisters Restaurant",
                            "lat": 36.2587744,
                            "long": -86.7144316
                        },
                        {
                            "address": "3443 Dickerson Pike SUITE 400, Nashville, TN 37207",
                            "comment": "Rating: 5/5\n",
                            "date": "03/06/2020 20:38:48 (UTC)",
                            "id": "ChZDSUhNMG9nS0VJQ0FnSUQwOVl1Y2VREAE",
                            "name": "CFP Weight Loss, Nashville's #1 Non Surgical Weight Loss Success Clinic",
                            "lat": 36.245244899999996,
                            "long": -86.7501699
                        }
                    ]
                }
            }
        },
        "biographic_details": {
            "education": {
                "linkedin_schools": [
                    {
                        "school_name": "Purdue University",
                        "degree_name": "Education Specialist, Administration",
                        "period": {
                            "date_to": "Present"
                        },
                        "duration": {},
                        "school_logo_url": "s3://signaight-dev/profile_photos/f/9d/ab7e6/f9dab7e6-7004-4706-bb36-34b40517273d.jpg",
                        "school_url": "https://www.linkedin.com/school/purdue-university/"
                    }
                ]
            },
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Adjunct Professor",
                            "description": "Specialty in teaching adullts returning to advance their opportunities.Taught over twenty differenct subjects to strengthen the general education background of students.",
                            "company_name": "Medtech College",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/70/92306/37092306-a05d-48aa-a720-c779852a17f0.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/school/medtech-college/",
                            "period": {
                                "date_from": "2010-03-01",
                                "date_to": "2016-09-01"
                            },
                            "duration": {
                                "years": 6,
                                "months": 7
                            }
                        },
                        {
                            "title": "Director of Education",
                            "description": "Developed curriculum and educationsal programs for juvenile inmates.  Solved conflicts among inmates and staff.  Served on release committee and parole board.",
                            "company_name": "Indiana Department of Correction",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/60/98abc/36098abc-ed8e-46e2-9ad4-dc9aa42e3b12.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/indiana-department-of-correction/",
                            "period": {
                                "date_from": "2000-01-01",
                                "date_to": "2008-12-01"
                            },
                            "duration": {
                                "years": 9
                            }
                        }
                    ],
                }
            }
        }

    }


@pytest.fixture
def profile_with_location_watchlist_countries():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "current_city": {
                    "fb_current_city": "Lawrenceville, Georgia"
                },
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "id": "YXBwX2l0ZW06MTAwMDQ0NjI2ODMwMTIzOjMwMjMyNDQyNTc5MDoxMDM6OjIwNDAyMTA0Nzc2MjEyMg==",
                            "title": "Lalmatia D Block",
                            "subtitle": "Dhaka, Bangladesh\nVisited on November 17, 2020",
                            "url": "https://www.facebook.com/pages/Lalmatia-D-Block/304315349641769",
                            "event_image": "s3://signaight-dev/profile_photos/b/1c/df483/b1cdf483-dbfb-4c16-a06c-aefdcdb59a84.png",
                            "region": "Dhaka, Bangladesh",
                            "date": "2020-11-17"
                        },

                    ]
                },
                "hometown": {
                    "fb_hometown": "Dhaka, Bangladesh"
                }
            }
        }
    }


@pytest.fixture
def geo_trace_grouping():
    return {
        "geo_trace": {
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": "dXJuOm1ieHBsYzpBbjFzYXc",
                        "place_name": "D Block, East of Kailash, New Delhi, South Delhi, Delhi, India",
                        "location_type": "check_ins",
                        "date": "2020-11-17",
                    },
                    "geometry": {"coordinates": [77.24527, 28.557344], "type": "Point"},
                    "id": "neighborhood.41774187",
                },
                {
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": "dXJuOm1ieHBsYzpFRWdV",
                        "wikidata": "Q1354",
                        "place_name": "Dhaka, Dhaka, Bangladesh",
                        "location_type": "residence",
                    },
                    "geometry": {"coordinates": [90.38896, 23.764288], "type": "Point"},
                    "id": "place.1067028",
                },
                {
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": "dXJuOm1ieHBsYzpJaFU",
                        "wikidata": "Q31",
                        "short_code": None,
                        "place_name": "Belgium",
                        "location_type": "entities",
                        "date": None,
                    },
                    "geometry": {"coordinates": [4.633575, 50.438696], "type": "Point"},
                    "id": "country.8725",
                },
            ],
            "type": "FeatureCollection",
        },
    }


@pytest.fixture
def profile_location_in_watchlist_country_without_twitter():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "current_city": {"fb_current_city": "Lawrenceville, Georgia"},
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "id": "YXBwX2l0ZW06MTAwMDQ0NjI2ODMwMTIzOjMwMjMyNDQyNTc5MDoxMDM6OjIwNDAyMTA0Nzc2MjEyMg==",
                            "title": "Lalmatia D Block",
                            "subtitle": "Dhaka, Bangladesh\nVisited on November 17, 2020",
                            "url": "https://www.facebook.com/pages/Lalmatia-D-Block/304315349641769",
                            "event_image": "s3://signaight-dev/profile_photos/4/24/f6856/424f6856-a6b3-4119-aeef-fa401b2dd442.png",
                            "region": "Dhaka, Bangladesh",
                            "date": "2020-11-17",
                        },
                    ]
                },
                "hometown": {"fb_hometown": "Dhaka, Bangladesh"},
            },
        },
        "geo_trace": {
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": "dXJuOm1ieHBsYzpBbjFzYXc",
                        "place_name": "D Block, East of Kailash, New Delhi, South Delhi, Delhi, India",
                        "location_type": "check_ins",
                        "date": "2020-11-17",
                    },
                    "geometry": {"coordinates": [77.24527, 28.557344], "type": "Point"},
                    "id": "neighborhood.41774187",
                },
                {
                    "type": "Feature",
                    "properties": {
                        "mapbox_id": "dXJuOm1ieHBsYzpFRWdV",
                        "wikidata": "Q1354",
                        "place_name": "Dhaka, Dhaka, Bangladesh",
                        "location_type": "residence",
                    },
                    "geometry": {"coordinates": [90.38896, 23.764288], "type": "Point"},
                    "id": "place.1067028",
                },
            ],
            "type": "FeatureCollection",
        },
    }


@pytest.fixture
def profile_with_hometown_current_city_equal():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "hometown": {
                    "fb_hometown_city": "Sopron"
                },
                "current_city": {
                    "fb_current_city": "Sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },

            }
        }
    }


@pytest.fixture
def profile_with_hometown_current_city_equal_different_casing():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "current_city_region_country": {
                    "linkedin_location": "Austria"
                },
                "hometown": {
                    "fb_hometown_city": "Sopron"
                },
                "current_city": {
                    "fb_current_city": "sopron"
                },
                "current_country": {
                    "linkedin_location_country": "Austria"
                },

            }
        }
    }


@pytest.fixture
def profile_with_hometown_current_city_equal_different_writing():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "current_city_region_country": {
                    "linkedin_location": "Vienna, Austria"
                },
                "hometown": {
                    "fb_hometown_city": "Sopron"
                },
                "current_city": {
                    "fb_current_city": "Sopron, Hungary"
                },
                "current_country": {
                    "linkedin_location_country": "Wien"
                },

            }
        }
    }


@pytest.fixture
def profile_with_checkins_not_shown_in_geotrace():
    return {
        "personal_details": {
            "name": {
                "first_name": {"f_name": "John"},
                "last_name": {"l_name": "Doe"},
                "full_name": {"full_name": "John Doe"},
            },
            "location": {
                "truecaller_country_code": "XK",
                "current_city_region_country": {
                    "linkedin_search_location": "Kosovo"
                },
                "check_ins": {
                    "fb_check_ins": [
                        {
                            "title": "Çka Ka Qëllu",
                            "subtitle": "The Bronx\nVisited on December 19, 2021",
                            "url": "https://facebook.com/ckakaqellubx",
                            "event_image": "s3://signaight-dev/profile_photos/0/f5/87d22/0f587d22-2421-4e88-93e6-3557bb2503b7.jpg",
                            "region": "The Bronx",
                            "date": "2021-12-19"
                        },
                        {
                            "title": "Gatsby's Cocktail Lounge",
                            "subtitle": "Las Vegas, Nevada\nVisited on December 17, 2021",
                            "url": "https://facebook.com/GatsbysVegas",
                            "event_image": "s3://signaight-dev/profile_photos/6/70/18048/67018048-d154-457e-9b2f-27b96d5135d0.jpg",
                            "region": "Las Vegas, Nevada",
                            "date": "2021-12-17"
                        },
                        {
                            "title": "Eight Lounge",
                            "subtitle": "Las Vegas, Nevada\nVisited on December 13, 2021",
                            "url": "https://facebook.com/eightloungelv",
                            "event_image": "s3://signaight-dev/profile_photos/1/ec/e047e/1ece047e-86f9-4d44-bcaf-9890a3431b59.jpg",
                            "region": "Las Vegas, Nevada",
                            "date": "2021-12-13"
                        }
                    ]
                },
                "places_lived": {}
            }
        }
    }
