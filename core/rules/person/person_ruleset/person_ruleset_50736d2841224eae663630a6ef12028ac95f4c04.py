person_ruleset = [
    {
        "label": 'Person has locations in watchlist countries',
        "conditions": {
            "any": [
                {
                    "name": "person_has_watchlist_countries_location",
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "red_countries": [
                            "Afghanistan",
                                "Syria",
                                "Yemen",
                                "Iran",
                                "Iraq",
                                "Libya",
                        ],
                        "orange_countries": [
                            "Cuba",
                            "North Korea",
                            "Iran",
                            "Syria",
                            "Pakistan",
                            "Bangladesh",
                            "Sri Lanka",
                            "Nigeria",
                            "Somalia",
                            "Democratic Republic of the Congo",
                            "Eritrea",
                        ],
                        "blue_countries": [
                            "Myanmar",
                            "Burma",
                            "Cambodia",
                            "Vietnam",
                            "Russia",
                            "Ukraine",
                            "Uzbekistan",
                            "Kazakhstan",
                            "Kyrgyzstan",
                            "China",
                            "North Korea",
                            "India",
                            "Indonesia",
                            "Malaysia",
                        ]
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_watchlist_countries",
                "params": {
                    "red_countries": [
                        "Afghanistan",
                        "Syria",
                        "Yemen",
                        "Iran",
                        "Iraq",
                        "Libya",
                    ],
                    "orange_countries": [
                        "Cuba",
                        "North Korea",
                        "Iran",
                        "Syria",
                        "Pakistan",
                        "Bangladesh",
                        "Sri Lanka",
                        "Nigeria",
                        "Somalia",
                        "Democratic Republic of the Congo",
                        "Eritrea",
                    ],
                    "blue_countries": [
                        "Myanmar",
                        "Burma",
                        "Cambodia",
                        "Vietnam",
                        "Russia",
                        "Ukraine",
                        "Uzbekistan",
                        "Kazakhstan",
                        "Kyrgyzstan",
                        "China",
                        "North Korea",
                        "India",
                        "Indonesia",
                        "Malaysia",
                    ]
                }
            },
        ],
    },
    {
        "label": 'Person has anti Israel posts',
        "conditions": {
            "any": [
                {
                    "name": ("check_person_anti_country"),
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "country": "IL"
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_anti_country",
                "params": {
                        "country": "IL"
                }
            },
        ],
    },
    {
        "label": 'Person has anti USA posts',
        "conditions": {
            "any": [
                {
                    "name": ("check_person_anti_country"),
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "country": "US"
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_anti_country",
                "params": {
                        "country": "US"
                }
            },
        ],
    },
    {
        "label": 'Person has posts showing Islamist Extremism',
        "conditions": {
            "any": [
                {
                    "name": "person_has_islamic_extremism",
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "jihadi_terms": [
                            "أنغماسي",
                            "غرباء",
                            "ك.ف.ر",
                            "تكفير",
                            "كافر",
                            "الولاء والبراء",
                            "طواغيت",
                            "طاغوت",
                            "الانغماسي",
                                "الغرباء",
                                "الكافر",
                                "الكفار",
                                "الكفر",
                                "ألولاء والبراء",
                                "الطاغوت",
                                "الطواغيت",
                                "الإنغماسي",
                                "للغرباء",
                                "كفّار",
                                "بالطاغوت",
                                "Inghimasi",
                                "Ghuraba’",
                                "Kafir",
                                "Kuffar",
                                "Kufr",
                                "Al-Wala’ wal-Bara’",
                                "Thaghut",
                                "Thaghut-Thaghut",
                                "Inghimasi",
                                "Ghuraba’",
                                "Kafir",
                                "Kuffar",
                                "Kufr",
                                "Al-Wala’ wal-Bara’",
                                "Taghut",
                                "Tawaghit",
                                "Inghimasi",
                                "Ghurabaa’",
                                "Kafir",
                                "Kuffar",
                                "Kufr",
                                "Al-Walaa’ wal-Baraa’",
                                "Taghut",
                                "Tawaghit",
                                "Ghuraba",
                                "kaafir",
                                "kuffaar",
                                "Al-Wala wal-Bara",
                                "taghoot",
                                "tawagheet",
                        ],
                        "salafi_religious_terms": [
                            "جهاد",
                            "خلافة",
                            "بدعة",
                            "أمة",
                            "توحيد",
                            "الجهاد",
                            "الخلافة",
                            "التوحيد",
                            "ألجهاد",
                            "Jihad",
                            "Khilafah",
                            "Bid’ah",
                            "Ummah",
                            "Tauhid",
                            "Jihad",
                            "Khilafah",
                            "Bid’ah",
                            "Ummah",
                            "Tauhid",
                            "Jihad",
                            "Khilafa",
                            "Bid‘a",
                            "Ummah",
                            "Tawhid",
                            "jihaad",
                            "Bidaa",
                            "Oummah",
                            "Tawheed",
                            "jehad",
                        ]
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_islamic_extremism",
                "params": {
                        "jihadi_terms": [
                            "أنغماسي",
                            "غرباء",
                            "ك.ف.ر",
                            "تكفير",
                            "كافر",
                            "الولاء والبراء",
                            "طواغيت",
                            "طاغوت",
                            "الانغماسي",
                            "الغرباء",
                            "الكافر",
                            "الكفار",
                            "الكفر",
                            "ألولاء والبراء",
                            "الطاغوت",
                            "الطواغيت",
                            "الإنغماسي",
                            "للغرباء",
                            "كفّار",
                            "بالطاغوت",
                            "Inghimasi",
                            "Ghuraba’",
                            "Kafir",
                            "Kuffar",
                            "Kufr",
                            "Al-Wala’ wal-Bara’",
                            "Thaghut",
                            "Thaghut-Thaghut",
                            "Inghimasi",
                            "Ghuraba’",
                            "Kafir",
                            "Kuffar",
                            "Kufr",
                            "Al-Wala’ wal-Bara’",
                            "Taghut",
                            "Tawaghit",
                            "Inghimasi",
                            "Ghurabaa’",
                            "Kafir",
                            "Kuffar",
                            "Kufr",
                            "Al-Walaa’ wal-Baraa’",
                            "Taghut",
                            "Tawaghit",
                            "Ghuraba",
                            "kaafir",
                            "kuffaar",
                            "Al-Wala wal-Bara",
                            "taghoot",
                            "tawagheet",
                        ],
                    "salafi_religious_terms": [
                            "جهاد",
                            "خلافة",
                            "بدعة",
                            "أمة",
                            "توحيد",
                            "الجهاد",
                            "الخلافة",
                            "التوحيد",
                            "ألجهاد",
                            "Jihad",
                            "Khilafah",
                            "Bid’ah",
                            "Ummah",
                            "Tauhid",
                            "Jihad",
                            "Khilafah",
                            "Bid’ah",
                            "Ummah",
                            "Tauhid",
                            "Jihad",
                            "Khilafa",
                            "Bid‘a",
                            "Ummah",
                            "Tawhid",
                            "jihaad",
                            "Bidaa",
                            "Oummah",
                            "Tawheed",
                            "jehad",
                            ]
                }
            },
        ],
    },
    {
        "label": 'Person follows extremist designated groups or pages',
        "conditions": {
            "any": [
                {
                    "name": "person_with_pages",
                    "operator": "is_true",
                    "value": True,
                },
                {
                    "name": "person_with_connections",
                    "operator": "is_true",
                    "value": True,
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_extremism_designated_groups",
                "params": {
                    "designated_groups_a": [
                        "100077281504626",
                        "104105132165223",
                        "100072112133015",
                        "1667314640156126",
                        "100076149076979",
                        "111604854686683",
                        "100064776814193",
                        "427975523963820",
                        "100071345002384",
                        "130124562594891",
                        "100069806612046",
                        "102472642072561",
                        "100064820076129",
                        "1485876968395912",
                        "100080397270873",
                        "107067068256111",
                        "100081145728521",
                        "108459478530870",
                        "100069657712999",
                        "102094344807871",
                        "61576771605603",
                        "699266476596763",
                        "100067926335216",
                        "832632420211648",
                        "61555007835539",
                        "223562374164930"
                    ],
                    "designated_groups_b": [
                        "100022948355060",
                        "106539387618516",
                        "doamuslims",
                        "100050389964029",
                        "2481865895172491",
                        "doamuslims2",
                        "100084520543375",
                        "100491549451484",
                        "doamuslimsbangla",
                        "100063507435709",
                        "845924955795856",
                        "doamuslimsfrance",
                        "100075461247268",
                        "144979629378025",
                        "muslimsbehindbars",
                        "100069545796341",
                        "287019441785180",
                        "brothersbehindbars.au",
                        "100069552771843",
                        "96390992174",
                        "MuslimPrisonerSupportGroup",
                        "100078690687204",
                        "738484679589324",
                        "100068937414541",
                        "326295397513168",
                        "FreeAafiaSiddiquiNow",
                        "100044361072708",
                        "181836051979249",
                        "zakirnaik"
                    ]
                }
            },
        ],
    },
    {
        "label": 'Person has images showing weapons',
        "conditions": {
            "any": [
                {
                    "name": "person_has_photos_with_weapons",
                    "operator": "is_true",
                    "value": True,
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_weapons_extremism",
            },
        ],
    },
    {
        "label": 'Calculate Person Risk Score if there are Red Flags',
        "conditions": {
            "any": [
                {
                    "name": "person_with_flags",
                    "operator": "is_true",
                    "value": True,
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_risk_score",
            },
        ],
    },

]
