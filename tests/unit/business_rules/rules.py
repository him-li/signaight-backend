import pytest

from core.rules.helpers.education_institutions import EducationInstitutions
from core.rules.helpers.person import PersonHelper


@pytest.fixture
def education_in_israel_rules():
    return [
        {
            "label": ('Person spent a semester of more in Israel as part '
                      'of an academic program'),
            "conditions": {
                "all": [
                    {
                        "name": ("linkedin_education_institutes_"
                                 "more_than_defined_semsesters"),
                        # exact school name match
                        "operator": "shares_at_least_one_element_with",
                        "value": (
                            EducationInstitutions.
                            get_institution_name_by_country('IL')),
                        "params": {"semesters": 1},
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_long_stay_in_country_by_educational_history",
                    "params": {"country": "IL"}
                },
            ],
        }
    ]


@pytest.fixture
def work_change_frequency_rules():
    return [
        {
            "label": (
                'A candidate who\'s work period in the last two work places '
                'is shorter than 1 year and two months'),
            "conditions": {
                "all": [
                    {
                        "name": "linkedin_work_change_frequency_for_period",
                        # exact school name match
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "last_positions_qty": 2,
                            "period": 14
                        },
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_occupational_instability_job_hopper",
                },
            ],
        }
    ]


@pytest.fixture
def hebrew_lang_native_speaker_rules():
    return [
        {
            "label": ('Fluency in Hebrew is an evidence for strong affinity'
                      ' with Israel or Israelis (e.g. Israeli origin,'
                      ' connections with Israelis, long stay in Israel)'),
            "conditions": {
                "any": [
                    {
                        "name": "chosen_language_speaker_from_social_networks",
                        # exact school name match
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "target_language": "he"
                        },
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_lang_native_seaker",
                    "params": {"language": "he"}
                },
            ],
        }
    ]


@pytest.fixture
def work_experience_in_israel_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "linkedin_work_experience_in_chosen_country",
                        "operator": "is_true",
                        "value": True,
                        "params": {"country": "IL"},
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_company_affiliated_with_country",
                    "params": {"country": "IL"}
                },
            ],
        }
    ]


@pytest.fixture
def volunteering_experience_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "person_with_linkedin_volunteering_experience",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_volunteering_experience",
                },
            ],
        }
    ]


@pytest.fixture
def person_score_rules():
    return [
        {
            "label": ('Fluency in Hebrew is an evidence for strong affinity'
                      ' with Israel or Israelis (e.g. Israeli origin,'
                      ' connections with Israelis, long stay in Israel)'),
            "conditions": {
                "any": [
                    {
                        "name": "chosen_language_speaker_from_social_networks",
                        # exact school name match
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "target_language": "he"
                        },
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_lang_native_seaker",
                    "params": {"language": "he"}
                },
            ],
        },
        {
            "label": "Person speaks multiple languages",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_multiple_languages",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_lang_proficiency"
                }
            ]
        },
        {
            "label": "Calculate person signaight_score",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_score",
                    "params": {
                        "evaluation_weights": {
                            "resilience": 5,
                            "flexibility": 5,
                            "work_under_pressure": 5,
                            "curiosity": 5,
                            "decision_making": 5,
                            "courage": 5,
                            "teamwork": 5,
                            "moral_values": 5,
                            "language_skills": 5,
                            "interpersonal_skills": 5,
                        },
                        "alerts_weights": {
                            "strong_affinity_with_israel": 5,
                            "strong_affinity_with_usa": 5,
                            "occupational_instability": 5,
                            "ineligible_occupation": 5,
                        },
                        "unweighted_alerts": [
                            "criminal_records"
                        ]
                    }
                }
            ]
        },
        {
            "label": "Calculate person compatibility",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_compatibility",
                    "params": {
                        "disqualifying_alerts": [
                            "strong_affinity_with_israel",
                            "strong_affinity_with_usa",
                            "occupational_instability",
                            "ineligible_occupation",
                            "anti_israel_statements",
                            "anti_usa_statements",
                            "criminal_records"
                        ],
                        "disqualifying_threshold": 8
                    }
                }
            ]
        }
    ]


@pytest.fixture
def person_only_score_compatibility_rules():
    return [
        {
            "label": "Calculate person signaight_score",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_score",
                    "params": {
                        "evaluation_weights": {
                            "resilience": 5,
                            "flexibility": 5,
                            "work_under_pressure": 5,
                            "curiosity": 5,
                            "decision_making": 5,
                            "courage": 5,
                            "teamwork": 5,
                            "moral_values": 5,
                            "language_skills": 5,
                            "interpersonal_skills": 5,
                        },
                        "alerts_weights": {
                            "strong_affinity_with_israel": 5,
                            "strong_affinity_with_usa": 5,
                            "occupational_instability": 5,
                            "ineligible_occupation": 5,
                        },
                        "unweighted_alerts": [
                            "criminal_records"
                        ]
                    }
                }
            ]
        },
        {
            "label": "Calculate person compatibility",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_compatibility",
                    "params": {
                        "disqualifying_alerts": [
                            "strong_affinity_with_israel",
                            "strong_affinity_with_usa",
                            "occupational_instability",
                            "ineligible_occupation",
                            "anti_israel_statements",
                            "anti_usa_statements",
                            "criminal_records"
                        ],
                        "disqualifying_threshold": 8
                    }
                }
            ]
        }
    ]


@pytest.fixture
def person_israel_affinity_rules():
    return [
        {
            "label": ('Person spent a semester of more in Israel as part '
                      'of an academic program'),
            "conditions": {
                "all": [
                    {
                        "name": ("linkedin_education_institutes_"
                                 "more_than_defined_semsesters"),
                        # exact school name match
                        "operator": "shares_at_least_one_element_with",
                        "value": (
                            EducationInstitutions.
                            get_institution_name_by_country('IL')),
                        "params": {"semesters": 1},
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_long_stay_in_country_by_educational_history",
                    "params": {"country": "IL"}
                },
            ],
        },
        {
            "label": ('Fluency in Hebrew is an evidence for strong affinity'
                      ' with Israel or Israelis (e.g. Israeli origin,'
                      ' connections with Israelis, long stay in Israel)'),
            "conditions": {
                "any": [
                    {
                        "name": "chosen_language_speaker_from_social_networks",
                        # exact school name match
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "target_language": "he"
                        },
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_lang_native_seaker",
                    "params": {"language": "he"}
                },
            ],
        },
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "linkedin_work_experience_in_chosen_country",
                        "operator": "is_true",
                        "value": True,
                        "params": {"country": "IL"},
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_company_affiliated_with_country",
                    "params": {"country": "IL"}
                },
            ],
        },
    ]


@pytest.fixture
def career_break_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "linkedin_career_break",
                        "operator": "greater_than",
                        "value": 52,
                        "params": {
                            "career_break_duration": 52,
                            "years_prior": 5
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_career_break",
                    "params": {
                        "career_break_duration": 52,
                        "years_prior": 5
                    }
                },
            ],
        }
    ]


@pytest.fixture
def management_positions_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "person_with_specific_background",
                        "operator": "is_true",
                        "value": True,
                        "params": {'titles': [*PersonHelper.management_titles,
                                              'manager']}
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_with_management_positions",
                    "params": {
                        "management_titles": PersonHelper.management_titles
                    }
                },
            ],
        }
    ]


@pytest.fixture
def min_experience_positions_rules():

    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "person_without_minimum_experience",
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "min_months": 36,
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_without_minimun_experience",
                    "params": {
                        "min_months": 36,
                        'min_intermidate_months': 33
                    }
                },
            ],
        }
    ]


@pytest.fixture
def journalism_background_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": "person_with_specific_background",
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "titles": PersonHelper.journalism_titles
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_with_journalism_background",
                    "params": {
                        "titles": PersonHelper.journalism_titles
                    }
                },
            ],
        }
    ]


@pytest.fixture
def government_background_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_with_background_"
                                 "in_specific_company_areas"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "fields": ["government"]
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_with_government_background",
                },
            ],
        }
    ]


@pytest.fixture
def international_travel_intro_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_international_travel_intro"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "emoticons": PersonHelper.traveler_emoticons_list,
                            "indicative_terms": (PersonHelper.
                                                 traveler_indicative_terms)
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_international_travel_intro",
                    "params": {
                        "emoticons": PersonHelper.traveler_emoticons_list,
                        "indicative_terms": (PersonHelper.
                                             traveler_indicative_terms)
                    }
                },
            ],
        }
    ]


@pytest.fixture
def international_travel_checkins_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_has_checkins"),
                        "operator": "is_true",
                        "value": True,
                    },
                    {
                        "name": ("person_with_posts"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_international_travel_checkins",
                },
            ],
        }
    ]


@pytest.fixture
def travel_risky_areas_check_ins_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_has_checkins"),
                        "operator": "is_true",
                        "value": True,
                    },
                    {
                        "name": ("person_with_posts"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_travel_risky_areas_check_ins",
                },
            ],
        }
    ]


@pytest.fixture
def teamwork_skill_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_has_specific_skill"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "skill": "Teamwork"
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_with_specific_skill",
                    "params": {
                        "skill": "Teamwork"
                    }
                },
            ],
        }
    ]


@pytest.fixture
def decision_making_skill_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_has_specific_skill"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "skill": "Decision Making"
                        }
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_with_specific_skill",
                    "params": {
                        "skill": "Decision Making"}
                }
            ]

        }
    ]


@pytest.fixture
def lives_in_israel_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_lives_in_country"),
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

                    "name": "set_person_lives_in_country",
                    "params": {
                        "country": "IL"
                    }
                },
            ],
        }
    ]


@pytest.fixture
def multiple_languages_rules():
    return [
        {
            "label": "Person speaks multiple languages",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_multiple_languages",
                                "operator": "is_true",
                                "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_lang_proficiency"
                }
            ]
        },
    ]


@pytest.fixture
def socialble_behaviour_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_is_sociable"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "social_photos": ["friends",
                                              "family",
                                              "relationship"]
                        }
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_is_sociable",
                    "params": {
                            "social_photos": ["friends",
                                              "family",
                                              "relationship"]
                    }
                },
            ],
        }
    ]


@pytest.fixture
def extreme_sports_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_with_posts"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_extreme_sports",
                },
            ],
        }
    ]


@pytest.fixture
def work_under_pressure_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_work_under_pressure"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {

                    "name": "set_person_work_under_pressure",
                },
            ],
        }
    ]


@pytest.fixture
def flexibility_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("person_with_evaluation_alerts"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_flexibility_score",
                },
            ],
        }
    ]


@pytest.fixture
def anti_israel_rules():
    return [
        {
            "label": (''),
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
        }
    ]


@pytest.fixture
def altruism_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {"name": ("person_with_posts"),
                     "operator": "is_true",
                     "value": True,
                     },
                    {
                        "name": ("person_with_pages"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_altruism",
                },
            ],
        }
    ]


@pytest.fixture
def anti_usa_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("check_person_anti_country"),
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            "country": "US"
                        }},
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
        }
    ]


@pytest.fixture
def criminal_records_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("has_criminal_records"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_has_criminal_records",
                },
            ],
        }
    ]


@pytest.fixture
def criminal_records_score_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {
                        "name": ("has_criminal_records"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_has_criminal_records",
                },
            ],
        },
        {
            "label": "Calculate person signaight_score",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_score",
                    "params": {
                        "evaluation_weights": {
                            "resilience": 5,
                            "flexibility": 5,
                            "work_under_pressure": 5,
                            "curiosity": 5,
                            "decision_making": 5,
                            "courage": 5,
                            "teamwork": 5,
                            "moral_values": 5,
                            "language_skills": 5,
                            "interpersonal_skills": 5,
                        },
                        "alerts_weights": {
                            "strong_affinity_with_israel": 5,
                            "strong_affinity_with_usa": 5,
                            "occupational_instability": 5,
                            "ineligible_occupation": 5,
                        },
                        "unweighted_alerts": [
                            "criminal_records"
                        ]
                    }
                }
            ]
        },
        {
            "label": "Calculate person compatibility",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_evaluation_alerts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_compatibility",
                    "params": {
                        "disqualifying_alerts": [
                            "strong_affinity_with_israel",
                            "strong_affinity_with_usa",
                            "occupational_instability",
                            "ineligible_occupation",
                            "anti_israel_statements",
                            "anti_usa_statements",
                            "criminal_records"
                        ],
                        "disqualifying_threshold": 8
                    }
                }
            ]
        }
    ]


@pytest.fixture
def optimism_rules():
    return [
        {
            "label": "Person has posts",
            "conditions": {
                "all": [
                    {
                        "name": "person_with_posts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_optimism"
                }
            ]
        },
    ]


@pytest.fixture
def suporting_israel_rules():
    return [
        {
            "label": (''),
            "conditions": {
                "any": [
                    {"name": ("person_with_posts"),
                     "operator": "is_true",
                     "value": True,
                     },
                    {
                        "name": ("person_with_pages"),
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_supporting_country",
                    "params": {
                        "country": "IL"
                    }
                },
            ],
        }
    ]


@pytest.fixture
def curiosity_reading_learning_platforms_rules():
    return [
        {
            "label": "Person has reading platforms",
            "conditions": {
                "all": [
                    {
                        "name": "person_has_reading_learning_platforms",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_has_reading_learning_platforms"
                }
            ]
        },
    ]


@pytest.fixture
def teamwork_experience_rules():
    return [
        {
            "label": "Person has teamwork experience",
            "conditions": {
                "all": [
                    {
                        "name": "person_has_teamwork",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_has_teamwork_experience"
                }
            ]
        },
    ]


@pytest.fixture
def flexibility_transition_industries_rules():
    return [
        {
            "label": ("Person shows flexibility by transitioning "
                      "between industries"),
            "conditions": {
                "all": [
                    {
                        "name": "person_has_positions",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_flexibility_transition_industries"
                }
            ]
        },
    ]


@pytest.fixture
def flexibility_skill_set_rules():
    return [
        {
            "label": "Person's skills show flexibility",
            "conditions": {
                "all": [
                    {
                        "name": "person_has_skills_in_profile",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_flexibility_skill_set",
                    "params": {
                        "test_skills":  {
                            "adaptability": 3.5,
                            "agility": 3,
                            "versatility": 2.5,
                            "resilience": 2,
                            "open-mindness": 1.5,
                            "multitasking": 1.5,
                            "problem-solving": 2.5,
                            "change management": 3,
                            "time management": 2,
                            "collaboration": 1.5,
                            "leadership": 1,
                            "critical thinking": 1
                        }
                    }
                }
            ]
        },
    ]


@pytest.fixture
def team_related_activities_rules():
    return [
        {
            "label": ("Person shows teamwork from posts and post reactions"),
            "conditions": {
                "all": [
                    {
                        "name": "person_with_posts",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_teamwork_team_related_activities_posts"
                },
                {
                    "name": "set_teamwork_team_related_activities_reactions"
                },
            ]
        },
    ]


@pytest.fixture
def work_under_pressure_skill_set_rules():
    return [
        {
            "label": "Person's skills show work under pressure capabilities",
            "conditions": {
                "all": [
                    {
                        "name": "person_has_skills_in_profile",
                        "operator": "is_true",
                        "value": True
                    }
                ]
            },
            "actions": [
                {
                    "name": "set_person_work_under_pressure_skill_set",
                    "params": {
                        "test_skills":  [
                            "resilience",
                            "stress tolerance",
                            "emotional stability",
                            "crisis management",
                            "decision-making under pressure",
                            "prioritization",
                            "critical thinking",
                            "adaptability",
                            "time management",
                            "problem solving"
                        ]
                    }
                }
            ]
        },
    ]


@pytest.fixture
def significant_volunteering_experience_rules():
    return [
        {
            "label": 'Person has significant volunteering experience',
            "conditions": {
                "any": [
                    {
                        "name": "person_with_linkedin_volunteering_experience",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": (
                        "set_person_with_significant_volunteering_experience"),
                },
            ],
        }
    ]


@pytest.fixture
def foodie_pages_rules():
    return [
        {
            "label": 'Person has foodie pages',
            "conditions": {
                "any": [
                    {
                        "name": "person_with_pages",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_foodie_pages",
                },
            ],
        }
    ]


@pytest.fixture
def foodie_intro_rules():
    return [
        {
            "label": 'Person has foodie intro data',
            "conditions": {
                "any": [
                    {
                        "name": "person_with_intro",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_foodie_intro",
                },
            ],
        }
    ]


@pytest.fixture
def tuned_curiosity_rules():
    return [
        {
            "label": 'Person has data to score curiosity',
            "conditions": {
                "any": [
                    {
                        "name": "person_has_data_for_tuned_curiosity_score",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_tuned_curiosity_score",
                },
            ],
        }
    ]


@pytest.fixture
def tuned_resilience_rules():
    return [
        {
            "label": 'Person has data to score resilience',
            "conditions": {
                "any": [
                    {
                        "name": "person_has_data_for_tuned_resilience_score",
                        "operator": "is_true",
                        "value": True,
                    },
                ]
            },
            "actions": [
                {
                    "name": "set_person_tuned_resilience_score",
                },
            ],
        }
    ]


@pytest.fixture
def checkins_in_israel_rules():
    return [
        {
            "label": 'Person has checkins in Israel',
            "conditions": {
                "any": [
                    {
                        "name": "has_checkins_in_country",
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
                    "name": "set_person_has_checkins_in_country",
                    "params": {
                            "country": "IL"
                    }
                },
            ],
        }
    ]


@pytest.fixture
def watchlist_countries_rules():
    return [
        {
            "label": 'Person has locations in watchlist countries',
            "conditions": {
                "any": [
                    {
                        "name": "person_has_watchlist_countries_location",
                        "operator": "is_true",
                        "value": True,
                        "params": {
                            # TODO: list of params should be changed to country codes (alpha 2)
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
        }
    ]


@pytest.fixture
def risk_score_rules():
    return [
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
        }
    ]


@pytest.fixture
def islamic_extremism_rules():
    return [
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
        }
    ]


@pytest.fixture
def extremism_designated_groups_rules():
    return [
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
    ]


@pytest.fixture
def weapons_extremism_rules():
    return [
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
        }
    ]
