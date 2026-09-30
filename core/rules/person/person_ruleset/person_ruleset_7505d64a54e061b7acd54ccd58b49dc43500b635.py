from core.rules.helpers.education_institutions import EducationInstitutions
from core.rules.helpers.person import PersonHelper

person_ruleset = [
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
                    "value": (EducationInstitutions.
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
        "label": ('A candidate who\'s work period in the last two work places '
                  'is shorter than 1 year and two months'),
        "conditions": {
            "all": [
                {
                    "name": "linkedin_work_change_frequency_for_period",
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
    },
    {
        "label": "Person with work experience in specific country",
        "conditions": {
            "all": [
                {
                    "name": "linkedin_work_experience_in_chosen_country",
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "country": "IL"
                    }
                }
            ]
        },
        "actions": [
            {
                "name": "set_company_affiliated_with_country",
                "params": {"country": "IL"}
            }
        ]
    },
    {
        "label": "Person with work experience in specific country",
        "conditions": {
            "all": [
                {
                    "name": "linkedin_work_experience_in_chosen_country",
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "country": "US"
                    }
                }
            ]
        },
        "actions": [
            {
                "name": "set_company_affiliated_with_country",
                "params": {"country": "US"}
            }
        ]
    },
    {
        "label": "Person has volunteering experience",
        "conditions": {
            "any": [
                {
                    "name": "person_with_linkedin_volunteering_experience",
                    "operator": "is_true",
                    "value": True,
                }
            ]
        },
        "actions": [
            {
                "name": "set_volunteering_experience",
            }
        ]
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
    {
        "label": 'Career Break',
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
    },
    {
        "label": 'Management Positions',
        "conditions": {
            "any": [
                {
                    "name": "person_with_specific_background",
                    "operator": "is_true",
                    "value": True,
                    "params": {'titles': [
                        *PersonHelper.management_titles,
                        "manager"]}
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
    },
    {
        "label": 'Minimum Experience',
        "conditions": {
            "any": [
                {
                    "name": "person_without_minimum_experience",
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "min_months": 36
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_without_minimun_experience",
                "params": {
                    "min_months": 36,
                    "min_intermidate_months": 33,
                }
            },
        ],
    },
    {
        "label": 'Journalism background',
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
    },
    {
        "label": 'Government background',
        "conditions": {
            "any": [
                {
                    "name": ("person_with_background_"
                             "in_specific_company_areas"),
                    "operator": "is_true",
                    "value": True,
                    "params": {
                        "fields": ['government']
                    }
                },
            ]
        },
        "actions": [
            {
                "name": "set_person_with_government_background",
            },
        ],
    },
    {
        "label": 'International Travel in Social Media Intro',
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
                    "indicative_terms": PersonHelper.traveler_indicative_terms
                }
            },
        ],
    },
    {
        "label": 'International Travel Checkins',
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
    },
    {
        "label": 'Risky Areas Checkins',
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
    },
    {
        "label": "Person has Teamwork as skill",
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
    },
    {

        "label": ('Person lives in Israel'),
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
    },
    {
        "label": "Person has Decision Making as skill",
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
                            "skill": "Decision Making"
                        }
            }
        ]
    },
    {
        "label": 'Person shows sociable behaviour',
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
    },
    {
        "label": 'Person has extreme sports pictures',
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
    },
    {
        "label": 'Person has Flexibility',
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
    },
    {
        "label": 'Person has work under pressure',
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
        "label": 'Person with Altruism',
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
    },
    {
        "label": 'Person with criminal records',
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
        "label": 'Person supports Israel',
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
    },
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
                    "test_skills": {
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
                "name": "set_person_with_significant_volunteering_experience",
            },
        ],
    },
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
    },
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
    },
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
    },
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
    },
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
    },
    # Always keep these as the last rules
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
                        "anti_israel_statements": 5,
                        "anti_usa_statements": 5,
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
