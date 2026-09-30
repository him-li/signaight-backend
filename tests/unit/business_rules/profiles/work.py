# flake8: noqa
import pytest
import pendulum


@pytest.fixture
def frequent_work_change():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2024-05-01",
                                "date_to": "2024-12-01"
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
                                "date_from": "2023-01-01",
                                "date_to": "2023-11-01"
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
def frequent_work_change_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2024-05-01",
                                "date_to": "2024-12-01"
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
                                "date_from": "2023-01-01",
                                "date_to": "2023-11-01"
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
def frequent_work_change_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work":  [
                    {
                        "fb_work_title": "Associate Product Manager MNA",
                        "fb_workplace_name": "Global Blue",
                        "fb_work_period": {
                            "date_from": "2024-05-01",
                            "date_to": "2024-12-01"
                        },
                        "duration": {
                            "years": 0,
                            "months": 7
                        }
                    },
                    {
                        "fb_work_title": "Presales Analyst",
                        "fb_workplace_name": "Odoo",
                        "fb_work_period": {
                            "date_from": "2023-01-01",
                            "date_to": "2023-11-01"
                        },
                        "duration": {
                            "months": 11
                        }
                    },
                ]
            },
        }
    }


@pytest.fixture
def not_frequent_work_change():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2024-05-01",
                                "date_to": "2024-12-01"
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
                                "date_from": "2023-01-01",
                                "date_to": "2023-11-01"
                            },
                            "duration": {
                                "months": 11
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2021-01-01",
                                "date_to": "2023-01-01"
                            },
                            "duration": {
                                "years": 1,
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def not_frequent_work_change_thomas():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Solutions Engineer",
                            "employment_type": "Full-time",
                            "company_name": "Iterate Norway",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/71/a585a/b71a585a-5107-452f-a02e-2ec6406d466d.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/iterate/",
                            "period": {
                                "date_from": "2024-09-01",
                                "date_to": "2025-04-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Senior Software Developer",
                            "employment_type": "Full-time",
                            "company_name": "SynPlan (by VNNOR AS)",
                            "company_logo_url": "s3://signaight-dev/profile_photos/5/48/a24f9/548a24f9-8fb2-4475-97f7-45c101ac2e66.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/synplan-ai/",
                            "period": {
                                "date_from": "2024-04-01",
                                "date_to": "2024-07-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Data Scientist/Developer",
                            "employment_type": "Full-time",
                            "company_name": "Foocus.ai",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/1d/34ecc/71d34ecc-e8a0-4341-95a6-c5caad551f7b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/foocusai/",
                            "period": {
                                "date_from": "2022-07-01",
                                "date_to": "2024-03-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 9
                            }
                        },
                        {
                            "title": "Computer Vision Intern",
                            "employment_type": "Internship",
                            "company_name": "laiout",
                            "company_logo_url": "s3://signaight-dev/profile_photos/8/b3/96423/8b396423-9b48-4955-b160-3f3382f1fda5.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/laiout/",
                            "period": {
                                "date_from": "2021-09-01",
                                "date_to": "2022-06-01"
                            },
                            "duration": {
                                "months": 10
                            }
                        },
                        {
                            "title": "Strategic Manager & Software Lead",
                            "description": "Led software development and did some general management. Software projects included the development of the desktop interface for engine testing. I also worked on web development for the project website. \n\nThe interface was created to run on desktop, parse sensor output from the engine and remotely control the system. The development of the interface, arduino and website software involved me managing a team of 3.",
                            "company_name": "Portal Space",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/86/455a2/786455a2-9a1c-49c0-bd73-43305a61057f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/portal-space/",
                            "period": {
                                "date_from": "2020-06-01",
                                "date_to": "2021-02-01"
                            },
                            "duration": {
                                "months": 9
                            }
                        },
                        {
                            "title": "Attende",
                            "description": "Early Stage is a 6-week long experiential entrepreneurship programme for students, with a primary focus on rapid market validation of ideas, assumption testing, product/service development, growth hacking, cultivating an entrepreneurial mindset, practical application of digital tools, raising capital and so forth. \n\nThe selected participants go through the entire process of bringing a new product/service to market, and learn to use modern innovation frameworks and methods in practice, ranging from LEAN startup to design thinking, Jobs to Be Done, agile and customer development. \n\nFor more information about the programme, see www.earlystage.no .",
                            "company_name": "Early Stage",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/39/202ec/039202ec-52d3-4bce-a060-59c31d9c5b28.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/early-stage-norway/",
                            "period": {
                                "date_from": "2019-09-01",
                                "date_to": "2019-10-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Food Service Worker",
                            "employment_type": "Part-time",
                            "description": "Customer service and occasionaly training new hires.",
                            "company_name": "McDonald's",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/0b/bdb36/00bbdb36-0460-4da0-866f-89e39b93ecb1.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/mcdonald%27s-corporation/",
                            "period": {
                                "date_from": "2018-11-01",
                                "date_to": "2019-07-01"
                            },
                            "duration": {
                                "months": 9
                            }
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_israeli_company():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Primary position of nothing to do",
                            "company_name": "Bank Hapoalim,",
                            "location": "Tel Aviv",
                            "period": {
                                "date_from": "2023-04-15",
                            },
                        },
                        {
                            "title": "Primary position of something to do",
                            "company_name": "ACME Inc",
                            "period": {
                                "date_from": "2020-09-01",
                                "date_to": "2021-09-25"
                            },
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_israeli_company_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Primary position of nothing to do",
                            "company_name": "Bank Hapoalim,",
                            "location": "Tel Aviv",
                            "period": {
                                "date_from": "2023-04-15",
                            },
                        },
                        {
                            "title": "Primary position of something to do",
                            "company_name": "ACME Inc",
                            "period": {
                                "date_from": "2020-09-01",
                                "date_to": "2021-09-25"
                            },
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Primary position of something to do",
                            "company_name": "ACME Inc",
                            "start_month_year": pendulum.parse("2020-09-01",
                                                               strict=False),
                            "end_month_year": pendulum.parse("2021-09-25",
                                                             strict=False),
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering_no_duration():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Primary position of something to do",
                            "company_name": "ACME Inc",
                            "start_month_year": pendulum.parse("2020-09-01",
                                                               strict=False),
                            "end_month_year": pendulum.parse("2021-09-25",
                                                             strict=False),
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering_only_duration():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Primary position of something to do",
                            "company_name": "ACME Inc",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def career_break_position():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Career Break",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2024-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2023-01-01",
                                "date_to": "2023-05-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def career_break_position_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Career Break",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2024-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2023-01-01",
                                "date_to": "2023-05-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def career_break_position_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Associate Product Manager MNA",
                        "fb_workplace_name": "Career Break",
                        "fb_work_period": {
                            "date_from": "2023-05-01",
                            "date_to": "2024-06-01"
                        },
                        "duration": {
                            "years": 1,
                            "months": 1
                        }
                    },
                    {
                        "fb_work_title": "Presales Analyst",
                        "fb_workplace_name": "Odoo",
                        "fb_work_period": {
                            "date_from": "2023-01-01",
                            "date_to": "2023-05-01"
                        },
                        "duration": {
                            "months": 5
                        }
                    },
                ]

            },
        }
    }


@pytest.fixture
def old_career_break_position_facebook():
    return {
        "biographic_details": {
            "work": {

                "facebook_work": [
                    {
                        "fb_work_title": "Associate Product Manager MNA",
                        "fb_workplace_name": "Career Break",
                        "fb_work_period": {
                            "date_from": "2012-05-01",
                            "date_to": "2013-06-01"
                        },
                        "duration": {
                            "years": 1,
                            "months": 1
                        }
                    },
                    {
                        "fb_work_title": "Presales Analyst",
                        "fb_workplace_name": "Odoo",
                        "fb_work_period": {
                            "date_from": "2013-06-01",
                            "date_to": "2022-05-01"
                        },
                        "duration": {
                            "months": 5
                        }
                    },
                ]

            },
        }
    }


@pytest.fixture
def old_career_break_position():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Career Break",
                            "period": {
                                "date_from": "2012-05-01",
                                "date_to": "2013-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2013-06-01",
                                "date_to": "2022-05-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def long_break_between_positions():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-01-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def long_break_between_positions_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-01-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def old_long_break_between_positions():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2012-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Presales Analyst",
                            "company_name": "Odoo",
                            "period": {
                                "date_from": "2009-01-01",
                                "date_to": "2010-01-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def no_career_break_positions():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Marketing Branding Consultant",
                            "company_name": "Self Employed",
                            "period": {
                                "date_from": "2018-02-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 6,
                                "months": 6
                            }
                        },
                        {
                            "title": "Business Journalist",
                            "company_name": "Mediaworks Hungary Zrt",
                            "period": {
                                "date_from": "2021-02-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 3,
                                "months": 6
                            }
                        },
                        {
                            "title": "Managing Editor Magazine",
                            "company_name": "Infopont magazin",
                            "period": {
                                "date_from": "2018-12-01",
                                "date_to": "2019-10-01"
                            },
                            "duration": {
                                "years": 0,
                                "months": 11
                            }
                        },
                        {
                            "title": "Public Relations Communications Assistant",
                            "company_name": "SabeeApp",
                            "period": {
                                "date_from": "2016-05-01",
                                "date_to": "2018-01-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 9
                            }
                        },
                        {
                            "title": "Production Coordinator",
                            "company_name": "Pioneer Productions",
                            "period": {
                                "date_from": "2014-01-01",
                                "date_to": "2016-05-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 5
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def no_career_break_positions_ralitsa():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Senior Commercial Manager",
                            "employment_type": "Full-time",
                            "description": "• Managing the top portfolio of the company: QSRs, big chains and top accounts\n• Crafting and executing strategies for partner growth, including promotions, ads and operational metrics\n• Analysing performance metrics to deliver actionable insights and ensure sustainable success\n• Leading a team of four account managers",
                            "company_name": "Glovo",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/0f/189a7/b0f189a7-2be6-4dfc-88f4-930883444fee.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/glovo-app/",
                            "period": {
                                "date_from": "2024-11-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Brands Ads Manager",
                            "employment_type": "Full-time",
                            "description": "• Building and growing the Brands Ads strategy and partnerships with strategic clients\n• Full ownership of the Brands P&L in the country\n• Implementing strong marketing campaigns to grow the positioning of clients\n• Actively looking for new business opportunities and working towards expanding the client portfolio\n• Part of Glovo Bulgaria's Leadership team",
                            "company_name": "Glovo",
                            "company_logo_url": "s3://signaight-dev/profile_photos/9/b4/19967/9b419967-dff1-4719-9110-de006bc2fb3c.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/glovo-app/",
                            "period": {
                                "date_from": "2022-02-01",
                                "date_to": "2024-11-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 10
                            }
                        },
                        {
                            "title": "Project Manager",
                            "description": "• Completing four successful editions outlining the strongest brands on the Bulgarian market\n• Building up the client portfolio — working with 50 different brands in FMCG, retail, finance, telecom, services, and more\n• In charge of the management of the entire project: building up the sales strategy, client relations, conducting the consumer research with GFK\n• Preparing the Superbrands business publication\n• Organizing the Superbrands awarding gala ceremony",
                            "company_name": "Superbrands Bulgaria",
                            "company_logo_url": "s3://signaight-dev/profile_photos/5/f0/f637b/5f0f637b-c0b2-49e1-9d67-06c02f4a40a2.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/superbrands-bulgaria/",
                            "period": {
                                "date_from": "2014-09-01",
                                "date_to": "2022-02-01"
                            },
                            "duration": {
                                "years": 7,
                                "months": 6
                            }
                        },
                        {
                            "title": "Country Manager",
                            "description": "• Establishing the entire business from scratch on the Bulgarian market. Completed three successful editions with over 20 different FMCG brands\n• In charge of project management, building up the sales strategy, account management, managing subcontractors and the Nielsen consumer research\n• Оrganising the annual Product of the Year awarding ceremony",
                            "company_name": "Product of the Year",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/df/9ba4b/0df9ba4b-a515-4958-a572-63e984d8ce33.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/product-of-the-year-uk/",
                            "period": {
                                "date_from": "2016-04-01",
                                "date_to": "2019-07-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 4
                            }
                        },
                        {
                            "title": "Account Manager",
                            "description": "• Full set of PR and communication activities for clients in retail, cosmetics, healthcare, finance, and more\n• Creation and implementation of PR strategies.\n• Media relations, corporate communications and event management",
                            "company_name": "M3 Communications Group, Inc.",
                            "company_logo_url": "s3://signaight-dev/profile_photos/6/6c/e3e63/66ce3e63-7936-43af-ad88-b03db61d11a7.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/m3-communications-group-inc-/",
                            "period": {
                                "date_from": "2012-08-01",
                                "date_to": "2014-07-01"
                            },
                            "duration": {
                                "years": 2
                            }
                        },
                        {
                            "title": "Technology Intern",
                            "description": "• Assisting the entire team in projects for clients from the Technology industry\n• Conducting research on new trends, client presence on the market and media",
                            "company_name": "Hill+Knowlton Strategies",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/56/cf6bc/b56cf6bc-8ad0-40c4-aba8-e6a4ff12634f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/hillandknowlton/",
                            "period": {
                                "date_from": "2011-06-01",
                                "date_to": "2011-07-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Account Assistant",
                            "description": "• Providing full support for the Client services department\n• Event organization, media relations and press releases, creation and implementation of marketing, communication and public affairs strategies.",
                            "company_name": "M3 Communications Group, Inc",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/01/511fb/301511fb-0fe1-4068-bf33-dd80a29676e1.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/m3-communications-group-inc-/",
                            "period": {
                                "date_from": "2010-07-01",
                                "date_to": "2010-08-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_management_title():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Head of Product",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2022-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Product Manager",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-05-01",
                                "date_to": "2021-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_management_title_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Head of Product",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2022-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Product Manager",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-05-01",
                                "date_to": "2021-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_management_title_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Head of Product",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2022-05-01",
                            "date_to": "2023-06-01"
                        },
                        "duration": {
                            "years": 1,
                            "months": 1
                        }
                    },
                    {
                        "fb_work_title": "Product Manager",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-05-01",
                            "date_to": "2021-06-01"
                        },
                        "duration": {
                            "years": 1,
                            "months": 1
                        }
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_without_management_title():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2022-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_without_minimum_experience():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2022-05-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_without_minimum_experience_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work":  [
                    {
                        "fb_work_title": "Product Analyst",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2022-05-01",
                            "date_to": "2023-06-01"
                        },
                        "duration": {
                            "years": 1,
                            "months": 1
                        }
                    },
                ]

                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_minimum_experience_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work":  [
                    {
                        "fb_work_title": "Product Analyst",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "2023-06-01"
                        },
                    },
                ]

                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_minimum_experience():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-06-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_without_minimum_experience_internship():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "Product Intern",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2020-08-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_without_minimum_experience_internship_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "Product Intern",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2020-08-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_minimum_experience_internship():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-12-01"
                            },
                        },
                        {
                            "title": "Product Intern",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-06-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_minimum_experience_internship_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-12-01"
                            },
                        },
                        {
                            "title": "Product Intern",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-06-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_journalism_background():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Another title",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-01-01"
                            },
                        },
                        {
                            "title": "News Reporter",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "News Reporter",
                            "company_name": "Something else",
                            "period": {
                                "date_from": "2023-06-01",
                                # "date_to": "2023-06-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_journalism_background_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Another title",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2020-01-01"
                            },
                        },
                        {
                            "title": "News Reporter",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "News Reporter",
                            "company_name": "Something else",
                            "period": {
                                "date_from": "2023-06-01",
                                # "date_to": "2023-06-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_journalism_background_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Another title",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2019-01-01",
                            "date_to": "2020-01-01"
                        },
                    },
                    {
                        "fb_work_title": "News Reporter",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "2023-06-01"
                        },
                    },
                    {
                        "fb_work_title": "News Reporter",
                        "fb_workplace_name": "Something else",
                        "fb_work_period": {
                            "date_from": "2023-06-01",
                            # "date_to": "2023-06-01"
                        },
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_with_government_background():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "General",
                            "company_name": "US Army",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "Volunteer",
                            "company_name": "Salvation Army",
                            "period": {
                                "date_from": "2023-06-01",
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_government_background_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "General",
                            "company_name": "US Army",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2023-06-01"
                            },
                        },
                        {
                            "title": "Volunteer",
                            "company_name": "Salvation Army",
                            "period": {
                                "date_from": "2023-06-01",
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_government_background_facebook():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "General",
                        "fb_workplace_name": "US Army",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "2023-06-01"
                        },
                    },
                    {
                        "fb_work_title": "Volunteer",
                        "fb_workplace_name": "Salvation Army",
                        "fb_work_period": {
                            "date_from": "2023-06-01",
                        },
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_with_teamwork_skill_one_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Teamwork",
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_teamwork_skill_six_endorsers():
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
def profile_with_teamwork_no_interpersonal():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Teamwork",
                            "endorser_count": 6
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_interpersonal_skill():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Interpersonal Skills",
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_interpersonal_skill_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "skills": {
                        "soft_skills": [
                            {
                                "name": "Interpersonal Skills",
                            }
                        ]
                    }
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_teamwork_xing_skill_six_endorsers():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "skills": {
                        'soft_skills':
                        [
                            {
                                "name": "Teamwork",
                                "endorser_count": 6
                            },
                            {
                                "name": "Interpersonal Skills",
                                "endorser_count": 6
                            }
                        ]
                    }
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_without_teamwork_skill():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Other skill",
                            "endorser_count": 1
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_decision_making_skill_six_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {

                            "name": "Decision Making",
                            "endorser_count": 6
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_decision_making_skill_no_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Decision Making",
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_decision_making_skill_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "skills": {
                        "soft_skills":
                            [
                                {
                                    "name": "Decision Making",
                                }
                            ]
                    }
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_linkedin_skills_empty():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                    ]
                },
                # "facebook_work": {}
            }
        }
    }


@pytest.fixture
def profile_with_skills_flexible_1_endorse():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Flexibility",
                            "endorser_count": 1
                        },
                    ]
                },
                # "facebook_work": {}
            }
        }
    }


@pytest.fixture
def profile_with_no_skills_flexible_1_endorse():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Public Speaking",
                            "endorser_count": 1
                        },
                    ]
                },
                "xing_work": {
                    "skills": {
                        "soft_skills": [
                            {
                                "name": "Public Speaking",
                                "endorser_count": 1
                            },
                        ]
                    }
                },
                # "facebook_work": {}
            }
        }
    }


@pytest.fixture
def profile_with_no_skills_flexible_only_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "skills": {
                        "soft_skills": [
                            {
                                "name": "Public Speaking",
                                "endorser_count": 1
                            },
                        ]
                    }
                },
                # "facebook_work": {}
            }
        }
    }


@pytest.fixture
def profile_with_empty_xing_skills():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "skills": {
                    }
                },
                # "facebook_work": {}
            }
        }
    }


@pytest.fixture
def profile_with_skills_flexible_endorsed():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "Flexibility",
                            "endorser_count": 2
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_work_flexibility():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Regional Distribution Manager",
                            "company_name": "BD Media | BD Logistics",
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
            },
        }
    }


@pytest.fixture
def profile_with_work_flexibility_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Regional Distribution Manager",
                            "company_name": "BD Media | BD Logistics",
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
            },
        }
    }


@pytest.fixture
def profile_work_under_pressure_score_8_expected():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2018-05-01",
                                "date_to": "2023-12-01"
                            },
                            "duration": {
                                "years": 4,
                                "months": 1
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_work_under_pressure_score_5_expected_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2023-05-01",
                                "date_to": "2023-12-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 7
                            }
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_work_under_pressure_score_8_expected_no_duration():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2018-05-01",
                                "date_to": "2023-12-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_work_under_pressure_score_5_expected_no_duration_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Associate Product Manager MNA",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2021-05-01",
                                "date_to": "2023-12-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_teamwork_linkedin():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Team leader",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2021-05-01",
                                "date_to": "2023-12-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_teamwork_xing():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Team leader",
                            "company_name": "Global Blue",
                            "period": {
                                "date_from": "2021-05-01",
                                "date_to": "2023-12-01"
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_teamwork_linkedin_duration():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Team leader",
                            "company_name": "Global Blue",
                            "duration": {
                                "years": "8",
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_teamwork_xing_duration():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Team leader",
                            "company_name": "Global Blue",
                            "duration": {
                                "years": "7",
                            },
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_skill_no_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_skill_5_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 5
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_agility_skill_5_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 5
                        },
                        {
                            "name": "agility",
                            "endorser_count": 5
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_agility_versatility_skill_5_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 5
                        },
                        {
                            "name": "versatility",
                            "endorser_count": 5
                        },
                        {
                            "name": "agility",
                            "endorser_count": 5
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_not_flexible_skill_set():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "dancing",
                            "endorser_count": 5
                        },
                        {
                            "name": "reading",
                            "endorser_count": 5
                        },
                        {
                            "name": "singing",
                            "endorser_count": 5
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_skill_no_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                        },
                        {
                            "name": "resilience",
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_skill_2_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 2
                        },
                        {
                            "name": "resilience",
                            "endorser_count": 2
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_skill_5_endorsers():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 5
                        },
                        {
                            "name": "resilience",
                            "endorser_count": 5
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_prioritization_skill_no_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                        },
                        {
                            "name": "resilience",
                        },
                        {
                            "name": "prioritization",
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_no_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                        },
                        {
                            "name": "resilience",
                        },
                        {
                            "name": "prioritization",
                        },
                        {
                            "name": "stress tolerance",
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_adaptability_resilience_prioritization_stress_tolerance_skill_2_endorser():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "skills": [
                        {
                            "name": "adaptability",
                            "endorser_count": 2
                        },
                        {
                            "name": "resilience",
                            "endorser_count": 2
                        },
                        {
                            "name": "prioritization",
                            "endorser_count": 2
                        },
                        {
                            "name": "stress tolerance",
                            "endorser_count": 2
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering_one_risky():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Volunteer",
                            "company_name": "World Central Kitchen - WCK",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        }
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering_two_risky():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Projektingenieur",
                            "company_name": "Ingenieur:innen ohne Grenzen Austria",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                        {
                            "role": "Volunteer",
                            "company_name": "World Central Kitchen - WCK",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_with_volunteering_two_not_risky():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "volunteering_experiences": [
                        {
                            "role": "Turkish-English Translator",
                            "company_name": "Tarjimly",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                        {
                            "role": "Volunteer",
                            "company_name": "כנפיים של קרמבו",
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                    ]
                },
            },
        }
    }


@pytest.fixture
def profile_multiple_present_positions_no_career_break():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Mushroom Picker",
                            "employment_type": "Full-time",
                            "company_name": "Korona Mushroom Union",
                            "company_logo_url": "s3://signaight-dev/profile_photos/9/08/1bdd7/9081bdd7-5b9d-41bf-8e11-60bf62157134.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/korona-mushroom-union/",
                            "period": {
                                "date_from": "2023-03-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 1,
                                "months": 11
                            }
                        },
                        {
                            "title": "Data Analyst",
                            "employment_type": "Self-employed",
                            "company_name": "Self-employed",
                            "period": {
                                "date_from": "2023-03-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 1,
                                "months": 11
                            }
                        },
                        {
                            "title": "Freelance Video Editor",
                            "employment_type": "Self-employed",
                            "description": "More than 4 years of experience as a Freelance Video Editor. Proficient in Adobe Premiere and After Effects.",
                            "company_name": "Self-employed",
                            "period": {
                                "date_from": "2017-01-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 8,
                                "months": 1
                            }
                        },
                        {
                            "title": "Farm Worker",
                            "employment_type": "Full-time",
                            "description": "Main Farm Activities: Milking, Nursing, Examine animals to detect symptoms of illness or injury. feed livestock, clean and disinfect their pens, cages, yards, and hutches.",
                            "company_name": "Ha menorah Dairy Farm Ltd.",
                            "period": {
                                "date_from": "2018-10-01",
                                "date_to": "2019-09-01"
                            },
                            "duration": {
                                "years": 1
                            }
                        },
                        {
                            "title": "Farm Worker",
                            "employment_type": "Full-time",
                            "description": "Main job activities includes: different work in citrus and avocado orchards - Harvesting, pruning, girdling, netting tress, maintenance of irrigation system, packing house activities.",
                            "company_name": "Mehadrin Tnuport Export L.P.",
                            "company_logo_url": "s3://signaight-dev/profile_photos/c/f5/325a5/cf5325a5-6806-4a0d-b426-375684c2b94b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/mehadrin-tnuport-export-l-p-/",
                            "period": {
                                "date_from": "2018-10-01",
                                "date_to": "2019-09-01"
                            },
                            "duration": {
                                "years": 1
                            }
                        }
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_no_job_hopper_katrien():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Event & creative director",
                            "employment_type": "Self-employed",
                            "company_name": "SJANSAAR.",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/87/12df9/28712df9-5525-44a5-898a-56f69dc24381.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/sjansaar/",
                            "period": {
                                "date_from": "2020-02-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 5,
                                "months": 3
                            }
                        },
                        {
                            "title": "Events & communication specialist",
                            "employment_type": "Freelance",
                            "company_name": "Equans BeLux",
                            "company_logo_url": "s3://signaight-dev/profile_photos/f/9c/b7b94/f9cb7b94-d84f-448a-8508-e009bcd6c7ee.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/equans-belux/",
                            "period": {
                                "date_from": "2023-06-01",
                                "date_to": "2023-10-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Corporate/Organizational Communication & Event manager",
                            "employment_type": "Freelance",
                            "company_name": "Stanley/Stella",
                            "company_logo_url": "s3://signaight-dev/profile_photos/6/84/bd496/684bd496-d025-497c-95cb-4569e3ff2cce.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/stanley-&-stella-sa/",
                            "period": {
                                "date_from": "2023-01-01",
                                "date_to": "2023-06-01"
                            },
                            "duration": {
                                "months": 6
                            }
                        },
                        {
                            "title": "Marketingexpert",
                            "employment_type": "Freelance",
                            "description": "Marketing expert NL & DE",
                            "company_name": "Xandres",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/c8/49c04/0c849c04-6e95-40a6-8b77-4602a4d8ebd7.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/xandres/",
                            "period": {
                                "date_from": "2022-04-01",
                                "date_to": "2022-09-01"
                            },
                            "duration": {
                                "months": 6
                            }
                        },
                        {
                            "title": "Marketing manager ad interim",
                            "employment_type": "Freelance",
                            "company_name": "Xandres",
                            "company_logo_url": "s3://signaight-dev/profile_photos/8/a3/42424/8a342424-b21c-410b-b8f8-7f5a8907ce95.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/xandres/",
                            "period": {
                                "date_from": "2021-12-01",
                                "date_to": "2022-04-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Freelance Marketing, Event & Communication Specialist",
                            "employment_type": "Freelance",
                            "description": "Freelance Marketing, Event & Communication Specialist for different smaller companies in cosmetics, entertainment & pharmacy.\nSocial Media Marketing Management\nRoll out the communication plan \nWork out the event structure\nOptimizing & daily management of Social Media channels",
                            "company_name": "2BRAIN",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/bc/c92c2/0bcc92c2-02b0-4e1a-8e36-32bafb40aab0.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/2brain2/",
                            "period": {
                                "date_from": "2019-10-01",
                                "date_to": "2022-02-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 5
                            }
                        },
                        {
                            "title": "Marketing Project Coordinator FOOD",
                            "employment_type": "Freelance",
                            "description": "Rolling out new communication/marketing campaign.\nCoordination of briefings (strategy, concept & design, fotoshoots,...)\nDetermine the right project approach & project team.\nOperational coordination & evaluation.",
                            "company_name": "Colruyt Group",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/15/d4317/715d4317-137f-41a9-b49f-30440f4eca72.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/colruytgroup/",
                            "period": {
                                "date_from": "2021-09-01",
                                "date_to": "2021-10-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Brand Manager Sikkens",
                            "employment_type": "Freelance",
                            "description": "Rolling out new communication campaign.\nRolling out launch new REZISTO products.\nResponsible for roadshows, webinars, media campaigns, fotoshoot,...\nCoordination of the communication agency.",
                            "company_name": "AkzoNobel",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/49/76036/24976036-263f-4140-89f0-c837bd7e8b80.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/akzonobel/",
                            "period": {
                                "date_from": "2021-05-01",
                                "date_to": "2021-08-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Freelance Account coordinator",
                            "employment_type": "Freelance",
                            "company_name": "BBC, a B2B creative agency.",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/d8/1d351/3d81d351-3da9-4467-bb7f-12424f2257d3.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/bbc-creativity/",
                            "period": {
                                "date_from": "2021-03-01",
                                "date_to": "2021-05-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Marketing Communication Consultant",
                            "employment_type": "Freelance",
                            "description": "Collaboration with the Project Manager of Difference Day (Press Freedom Day), MARCOM VUB & Caroline Pauwels (Rector VUB).\nSet up the communication plan + roll-out\nSet up the advertising campaign in collaboration with an advertisement agency\nSocial Media Management & hosting DD website\nOrganization & coordination of the LIVE & VIRTUAL event\nLogistical follow-up of the event",
                            "company_name": "Vrije Universiteit Brussel",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/4a/c4735/74ac4735-3655-4d32-9263-922b93b3d4e4.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/school/vrije-universiteit-brussel/",
                            "period": {
                                "date_from": "2020-11-01",
                                "date_to": "2021-05-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Communication & PR",
                            "employment_type": "Full-time",
                            "description": "Responsible for the communication of the vaccination center Pacheco, roll-out re-branding, variable communication & PR projects within the Clinic.",
                            "company_name": "Kliniek Sint-Jan / Clinique Saint-Jean",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/c3/c68d8/3c3c68d8-3d39-4ce6-a639-76f8fdf44917.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/kliniek-sint-jan-clinique-saint-jean/",
                            "period": {
                                "date_from": "2021-01-01",
                                "date_to": "2021-02-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Project Manager Beauty-Massage-Wellness-Expo 6 & 7 March 2021 @ Waregem Expo",
                            "employment_type": "Freelance",
                            "description": "Set up the communication plan & social media channels \nSourcing exhibitors, speakers and negotiating conditions\nWork out the set up & catering\nPhotography & video montage\n\n",
                            "company_name": "Sonar Media & PR",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/e6/20543/ee620543-4549-4519-aaaa-44249514172c.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/beautybizz/",
                            "period": {
                                "date_from": "2020-05-01",
                                "date_to": "2020-11-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Sales Manager @ Nuquest Nautical Events",
                            "employment_type": "Freelance",
                            "description": "Presenting Nuquest Nautical Events (Sail & Boot Incentives & Teambuilding)",
                            "company_name": "Nuquest events - exclusive and ecological Sailing Incentives & Teambuilding",
                            "company_logo_url": "s3://signaight-dev/profile_photos/9/fd/881b3/9fd881b3-3403-4281-bcac-1a73b5d47941.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/nuquest-sail-&-boat-incentives-&-teambuilding/",
                            "period": {
                                "date_from": "2019-10-01",
                                "date_to": "2020-06-01"
                            },
                            "duration": {
                                "months": 9
                            }
                        },
                        {
                            "title": "Event & Incentive Consultant",
                            "employment_type": "Freelance",
                            "company_name": "Triple Tree Event Agency",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/5a/cf5ee/25acf5ee-8407-4284-b62f-eb8047d4220b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/triple-tree-events-agency/",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "2020-03-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Employer Branding Consultant",
                            "employment_type": "Freelance",
                            "description": "Supporting the HR-department in marketing activities. My mission is to translate the employer branding of Carrefour into concrete actions (online and offline) and to develop a better candidate experience throughout the entire recruitment process. I will form the bridge between the recruiters and the Communication, Marketing and Digital department.",
                            "company_name": "Carrefour Belgium",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/e8/dba0b/ee8dba0b-d876-46dc-a1cf-b54ebd2651e2.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/carrefourbelgium/",
                            "period": {
                                "date_from": "2019-10-01",
                                "date_to": "2019-12-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Commercial Operations Coordinator , Sales & Marketing Oncology",
                            "employment_type": "Freelance",
                            "description": "Practical organisation and follow-up of congresses & seminars & Masterclasses\nThe chain between the CBM & PM Oncology\nAnalysing Sales and support to the commercial director\nCollaboration with specialist working groups to develop sales tools, slidekits, trainings & campaigns.",
                            "company_name": "Astellas Pharma",
                            "company_logo_url": "s3://signaight-dev/profile_photos/a/d9/bbfbd/ad9bbfbd-67f6-4f98-8dd9-e0ef49dccad3.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/astellaspharmainc/",
                            "period": {
                                "date_from": "2018-11-01",
                                "date_to": "2019-09-01"
                            },
                            "duration": {
                                "months": 11
                            }
                        },
                        {
                            "title": "Project Manager",
                            "employment_type": "Freelance",
                            "description": "Coordination of the Sensobus project.\nAnalyzing needs of the target groups & suppliers\nNegotiation new partners/suppliers\nFollow-up of the project administration",
                            "company_name": "Puratos",
                            "company_logo_url": "s3://signaight-dev/profile_photos/c/ce/d575f/cced575f-cd1e-4ce8-8c6e-ae47a97d188f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/puratos/",
                            "period": {
                                "date_from": "2018-05-01",
                                "date_to": "2018-12-01"
                            },
                            "duration": {
                                "months": 8
                            }
                        },
                        {
                            "title": "Event Manager",
                            "employment_type": "Full-time",
                            "description": "Negotiation suppliers & clients\nProspecting new events/collaborations\nResponsible POS-material\nAttending trade fairs\nResponsible for the visibility @ events/fairs,....\nFull project administration",
                            "company_name": "Royal Swinkels Family Brewers",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/2c/f1d8d/02cf1d8d-36e4-4c92-878a-3e10a17ae026.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/royalswinkels/",
                            "period": {
                                "date_from": "2017-07-01",
                                "date_to": "2018-09-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                        {
                            "title": "Marketing & Event Management Assistant",
                            "employment_type": "Contract",
                            "description": "Responsible for the marketing of the export-department (brochures, website, newsletters, trade fairs)\nPlanning business trips\nResponsible for trainings in Belgium and Europe for export-clients\nFull secretarial support to the KAM’s",
                            "company_name": "Eternit Belgium",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/17/4ea76/e174ea76-6af1-437b-b677-f7815f3987ca.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/cedralsidingsbenelux/",
                            "period": {
                                "date_from": "2006-03-01",
                                "date_to": "2016-03-01"
                            },
                            "duration": {
                                "years": 10,
                                "months": 1
                            }
                        },
                        {
                            "title": "Transport & Supply chain assistant/BLS SAP",
                            "description": "Full transport planning BE+FR+NL+UK+LUX+DE\nSourcing and negotiation of new suppliers\nSAP Basic Line Support\nCoordinator of SAP-trainings in logistics\nRight-hand of the Supply Chain Manager",
                            "company_name": "Eternit Belgium",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/1d/4f219/b1d4f219-2142-49e1-9504-ecc0e5996288.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/cedralsidingsbenelux/",
                            "period": {
                                "date_from": "2001-01-01",
                                "date_to": "2006-03-01"
                            },
                            "duration": {
                                "years": 5,
                                "months": 3
                            }
                        },
                        {
                            "title": "Sales & Marketing Assistant",
                            "employment_type": "Contract",
                            "description": "Full administrational + commercial support of the Marketing department.",
                            "company_name": "Puratos",
                            "company_logo_url": "s3://signaight-dev/profile_photos/4/e7/416ca/4e7416ca-f77b-4ff4-ab55-554e0692e79f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/puratos/",
                            "period": {
                                "date_from": "2000-09-01",
                                "date_to": "2001-01-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_no_job_hopper_viara():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Change Management Consultant. Organisational Psychologist",
                            "employment_type": "Full-time",
                            "description": "- Develop and execute change management strategies and plans to support the implementation of organizational changes.\n- Conduct impact assessments and stakeholder analyses to identify potential risks and resistance to change.\n- Create and deliver effective communication materials to keep stakeholders informed and engaged throughout the change process.\n- Design and deliver training programs to equip employees with the necessary skills and knowledge to adapt to change.\n- Provide coaching and support to leaders and managers to facilitate their role in driving and sustaining change.\n- Monitor and measure change progress, identifying areas for improvement and implementing corrective actions as needed.\n- Collaborate with cross-functional teams to ensure alignment and coordination of change activities.",
                            "company_name": "DSK Bank",
                            "company_logo_url": "s3://signaight-dev/profile_photos/f/5a/02a80/f5a02a80-16cd-494c-94a3-a86ee20509f3.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/dsk-bank/",
                            "period": {
                                "date_from": "2024-10-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Managing Partner and Performance Coach",
                            "employment_type": "Self-employed",
                            "description": "About the company: Thistle & Lime Consulting Ltd. is a company for brave and ambitious personal, professional and business growth. Our experts will provoke and equip each individual, group or organization with lots of inventive, sharp, bittersweet ideas and meaning on the way to enhance their performance and cooperation for achieving better results every day. If you are looking for something challenging and enlightening to help you reach your full potential and even more, as an individual or as an organization, contact us and we will walk you through a special and meaningful, individualised process. Our approach does not shy away from the “deeply theoretical” in favour of the “simple and practical” or vice versa, since neither theory nor practice exist independently of each other and we are prepared to demonstrate why.\n\nAbout me: My interests range from leadership and key roles performance coaching and constructive culture development to attracting talent and supporting any individuals and groups to discover, understand and implement great ideas into their personal and professional life. I am inspired by philosophical ideas, great readings, creative technology, music, arts, and travel, meaning and beauty in general, and I do my best to bring this to my work.",
                            "company_name": "Thistle&Lime Consulting",
                            "company_logo_url": "s3://signaight-dev/profile_photos/a/6a/4707b/a6a4707b-dbc3-47f9-9030-b0f623910163.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/thistle-lime-consulting/",
                            "period": {
                                "date_from": "2020-01-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 5,
                                "months": 2
                            }
                        },
                        {
                            "title": "Senior Human Resources Business Partner",
                            "employment_type": "Full-time",
                            "description": "• Manages a regular interaction with employees and managers to ensure understanding of business and people needs\n• Provides day-to-day performance management guidance to line management\n• Managing staff wellness initiatives\n• Improving and monitoring employee productivity\n• Acts as a liaison between management and employees to improve work relationships, build morale, and increase productivity and retention",
                            "company_name": "Delasport",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/c7/63c30/2c763c30-bb02-47c0-9733-d634f64eea9c.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/delasport/",
                            "period": {
                                "date_from": "2024-03-01",
                                "date_to": "2024-07-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Managing Director and Executive L&D Consultant",
                            "description": "Leading and manage a team of HR Service Consultants in the three main business areas – Recruitment, Learning and Development and HR Consultancy as well as all business processes of the company, contacts with clients and partners. Act as Learning & Development and Performance Coach for priority Clients as part of projects with high level of importance.\n",
                            "company_name": "UpSkill Ltd.",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/f3/66010/ef366010-6ff5-454d-99a2-bcdbca2e516f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/upskill-bulgaria-ltd-/",
                            "period": {
                                "date_from": "2016-03-01",
                                "date_to": "2019-09-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 7
                            }
                        },
                        {
                            "title": "Senior HR Consultant ",
                            "description": "Behaviour Skills - Trainings and Coaching\nInterpersonal and Corporative Communications \nOrganizational Culture Development\nPerformance and Processes Improvement",
                            "company_name": "Stone  Computers AD",
                            "company_logo_url": "s3://signaight-dev/profile_photos/6/0a/a3832/60aa3832-ddb4-4c12-83f9-073a14a93e94.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/stone-computers-ad/",
                            "period": {
                                "date_from": "2014-09-01",
                                "date_to": "2016-03-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 7
                            }
                        },
                        {
                            "title": "Learning & Development Lead",
                            "description": "Deed is a challenge-based platform empowering HR specialists to carry out employee activities resulting in motivated and better performing teams. Deed reduces the HR budget while improving the efficiency and visibility of human capital initiatives.\nSome of Deed’s HR applications include:\n* Making training and sharing of knowledge regular and employee-driven;\n* Building your team via regular and cost-efficient activities;\n* Creating engaging volunteer campaigns;\n* Creating reliable and rewarding internal recruitment processes;",
                            "company_name": "Deed",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/a3/6a290/ba36a290-aac0-48c6-a4b2-c908e720eb8e.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/deed/",
                            "period": {
                                "date_from": "2014-09-01",
                                "date_to": "2016-01-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 5
                            }
                        },
                        {
                            "title": "Continuous Improvement Lead",
                            "description": "Monitor and manage people performance and processes implementation. Recommend changes and improvements. Develop and implement training programs and courses. Observe and analyze corporate culture. Develop instruments and processes for sustaining constructive culture and productivity. Represent 60K on business events connected with people development and learning processes. Support the recruitment and the talent management processes. Assist CEO and the project managers in business expansion activities.\n\n",
                            "company_name": "Sixty K Ltd (60K)",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/1e/c528d/31ec528d-6ded-4cb5-8a71-0c3c21357ae3.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/resultscxbulgaria/",
                            "period": {
                                "date_from": "2011-01-01",
                                "date_to": "2014-09-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 9
                            }
                        },
                        {
                            "title": "Business Develoment and Training Consultant",
                            "description": "Create and conduct tailor made training for developing behavior skills (soft skills) such as sales, customer care, management and leadership, effective communication, negotiations and more, introduces and sustains processes for building constructive corporate culture in business field.\n\n",
                            "company_name": "Free-Lance Consultant and Trainer",
                            "period": {
                                "date_from": "2009-01-01",
                                "date_to": "2011-01-01"
                            },
                            "duration": {
                                "years": 2
                            }
                        },
                        {
                            "title": "Business Development and Training Manager",
                            "description": "Responsible for researching, analyzing and acting upon the business development and training needs of businesses, companies and individuals who have ambitious goals of improving their personal, group or corporate results, strengthen their capacity and reach-out higher horizons in their professions and life.",
                            "company_name": "Horizons Bulgaria",
                            "company_logo_url": "s3://signaight-dev/profile_photos/f/86/72c13/f8672c13-1185-4bed-9722-3dcbace3946b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/horizons-bulgaria/",
                            "period": {
                                "date_from": "2008-08-01",
                                "date_to": "2009-07-01"
                            },
                            "duration": {
                                "years": 1
                            }
                        },
                        {
                            "title": "Executive Director",
                            "description": "About: The Association works to improve Family School Relations and to help Teachers, School Directors, Regional Inspectorates of Education and all other Education Institutions to involve parents and students in working together for improving education quality and modernizing the education system in Bulgaria.\nMy role: Manage and develop a Network of 33 local community development experts and trainers; 65 School Boards of Trustees and 12 Public Councils of Education within 12 Administrative Regions all over Bulgaria.",
                            "company_name": "ASSOCIATION FOR PARENTAL ACTIVISM",
                            "period": {
                                "date_from": "2005-01-01",
                                "date_to": "2008-05-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 5
                            }
                        },
                        {
                            "title": "Learning & Development and Partnership Building Manager EMEA Region",
                            "employment_type": "Full-time",
                            "description": "Design training programs for capacity building of partners of the CRS/Bulgaria. Provide consultation and assistance to CRS/Bulgaria for the organizational development of any appropriate components of the education program. Assist in the development of a concept on the role of TOT group and perspectives for its development. Design, Implement, Monitor, Evaluation projects, including Budget and Staff management.\n\n",
                            "company_name": "Catholic Relief Services",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/4d/652f7/04d652f7-461c-4487-a86e-329f63c3ea9d.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/catholic-relief-services/",
                            "period": {
                                "date_from": "1998-01-01",
                                "date_to": "2005-01-01"
                            },
                            "duration": {
                                "years": 7
                            }
                        },
                        {
                            "title": "Sales and Marketing Assistant",
                            "description": "Assist the Sales Manager in planning and monitoring the work of 15 distribution regions all over the country. Summarize the information for the sales. Provide regular information to the regions-sales and stock reports, tables and charts. Coordinate communication between supervisor merchandisers and distributors within the division",
                            "company_name": "Wrigley",
                            "company_logo_url": "s3://signaight-dev/profile_photos/c/cd/cd5ed/ccdcd5ed-2d02-4fb2-a28b-2424fc21dc28.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/wrigley/",
                            "period": {
                                "date_from": "1996-01-01",
                                "date_to": "1998-01-01"
                            },
                            "duration": {
                                "years": 2
                            }
                        },
                        {
                            "title": "Manager of Center For Information and Culture",
                            "description": "Organize conferences, logistics and coordination of events. Monitor the information services such as local radio emissions, newsletter and the cultural activities. Develop a plan for cultural activities for the staff and the patients, like for example moves, sport activities, exhibitions, concerts, theater, events, ext.\n\n",
                            "company_name": "Military Medical Academy",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/ea/a3356/beaa3356-11e0-40be-9209-b143fbd17f98.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/militarymedicalacademy/",
                            "period": {
                                "date_from": "1991-05-01",
                                "date_to": "1995-09-01"
                            },
                            "duration": {
                                "years": 4,
                                "months": 5
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_no_job_hopper_tina():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "DE&I | EY Belgium | bEYou Co-Lead",
                            "company_name": "EY",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/6c/eb910/76ceb910-8097-4acd-9f70-3cf3d9569653.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/ernstandyoung/",
                            "period": {
                                "date_from": "2025-01-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Senior Consultant | FSO | Business Transformation ",
                            "employment_type": "Full-time",
                            "company_name": "EY",
                            "company_logo_url": "s3://signaight-dev/profile_photos/9/f9/b5df9/9f9b5df9-58cb-4e0f-bf91-69abb0e754af.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/ernstandyoung/",
                            "period": {
                                "date_from": "2024-04-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Management Consulting Analyst | Financial Services",
                            "employment_type": "Full-time",
                            "description": "Senior Business Analyst:\nClearstream, National Bank of Belgium",
                            "company_name": "Accenture",
                            "company_logo_url": "s3://signaight-dev/profile_photos/4/80/c5194/480c5194-64dc-4867-add0-b7cf9f9f1a60.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/accenture/",
                            "period": {
                                "date_from": "2022-07-01",
                                "date_to": "2023-11-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 5
                            }
                        },
                        {
                            "title": "Technology Consulting Analyst | Financial Services",
                            "employment_type": "Full-time",
                            "description": "Functional Analyst/ Change management:\nING, Degroof Petercam",
                            "company_name": "Accenture",
                            "company_logo_url": "s3://signaight-dev/profile_photos/8/79/a1944/879a1944-333d-4136-8b56-f1c720f236e9.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/accenture/",
                            "period": {
                                "date_from": "2021-01-01",
                                "date_to": "2022-07-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 7
                            }
                        },
                        {
                            "title": "Consultant | Financial services ",
                            "description": "Test Analyst/Business Analyst/ PMO:\nBNP Paribas Fortis, Etnic",
                            "company_name": "Capgemini",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/81/9ce08/0819ce08-cbcf-47c6-8607-819beea2ae82.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/capgemini/",
                            "period": {
                                "date_from": "2019-01-01",
                                "date_to": "2021-01-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 1
                            }
                        },
                        {
                            "title": "Sales Assistant |While studying|",
                            "employment_type": "Full-time",
                            "description": "Greeting and engaging visitors in an effort to establish relationships to determine customer needs and preferences. Providing timely and consistent follow through with \r\ncustomers from initial contact through closing and post-closing activities.",
                            "company_name": "Living Development",
                            "company_logo_url": "s3://signaight-dev/profile_photos/6/18/bcb8f/618bcb8f-42ab-4f31-8859-937ad518610f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/living-capital/",
                            "period": {
                                "date_from": "2017-04-01",
                                "date_to": "2018-06-01"
                            },
                            "duration": {
                                "years": 1,
                                "months": 3
                            }
                        },
                        {
                            "title": "Office Manager |While studying|",
                            "employment_type": "Contract",
                            "description": "Maintaining office operations by receiving and distributing communications; maintaining supplies and equipment; picking-up and delivering items; serving customers; supporting the organisation of meeting & Events.",
                            "company_name": "Ergon Capital",
                            "company_logo_url": "s3://signaight-dev/profile_photos/a/ac/87ba7/aac87ba7-6453-4f39-b24f-ccb3d2feaade.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/apheon/",
                            "period": {
                                "date_from": "2016-09-01",
                                "date_to": "2017-03-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Sales Executive",
                            "employment_type": "Full-time",
                            "description": "As a sales consultant, I had to understand the needs of prospective members/ companies and help them find the best way to use our clubs. I performed a series of sales duties – from call prospection to contract negotiation using Microsoft Dynamics – in order to maximize membership sales numbers in order to surpass personal and team targets.",
                            "company_name": "Aspria",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/7f/6b626/27f6b626-e4e0-46d9-8fea-b9357861bfec.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/aspria/",
                            "period": {
                                "date_from": "2015-09-01",
                                "date_to": "2016-06-01"
                            },
                            "duration": {
                                "months": 10
                            }
                        },
                        {
                            "title": "Promogirl/ Hostess |While studying|",
                            "employment_type": "Contract",
                            "description": "As a Promogirl I am basically hired as a brand ambassador by companies like Coca-Cola, Jupiler, Hoegaarden, Proximus, Mercedes, Douwe Egberts, Magnum, Ricola etc to spread the word about their products and/or services all over the country. I had various duties, Depending on the needs of the company, but each lead back to selling and promoting.",
                            "company_name": "Demonstr8",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/97/7a51d/e977a51d-9efc-40cc-939d-7a46f55cbf06.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/demonstrate/",
                            "period": {
                                "date_from": "2012-01-01",
                                "date_to": "2015-09-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 9
                            }
                        },
                        {
                            "title": "Meeting & Events Coordinator |While studying|",
                            "employment_type": "Internship",
                            "description": "As a Hotel Planner I was in charge of the Co-ordination of Meetings and Events, preparing proposals to satisfy clients' needs and maximize profit, Drawing up and \r\ndispatching of contracts for business using the Opera Software, negotiating with the clients in all aspects of the booking. I arranged the meeting space and supported services. Whether it was a business meeting/ convention, a banquet or a conference call, I ensured that the purpose is achieved efficiently and seamlessly. I coordinated every detail of events, from beginning to end.",
                            "company_name": "Thon Hotels",
                            "company_logo_url": "s3://signaight-dev/profile_photos/6/54/a4d9f/654a4d9f-0d7d-4e0b-accd-74b03822db0a.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/thon-hotels/",
                            "period": {
                                "date_from": "2014-09-01",
                                "date_to": "2015-02-01"
                            },
                            "duration": {
                                "months": 6
                            }
                        },
                        {
                            "title": "Receptionist Sales |While studying|",
                            "employment_type": "Internship",
                            "description": "As a receptionist, I was the first point of contact for the Hotel and provided administrative support across the organization. I was handling the flow of people (telephone/email/ walk in inquiries) and ensured that all responsibilities are completed accurately and delivered with high quality and in a timely manner in line with the hotel’s vision and values on customer satisfaction. (Yes I Can! training)",
                            "company_name": "Park Inn by Radisson",
                            "company_logo_url": "s3://signaight-dev/profile_photos/d/53/bcf65/d53bcf65-762e-4934-94cd-0a853cd65c4b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/parkinnbyradisson/",
                            "period": {
                                "date_from": "2014-01-01",
                                "date_to": "2014-04-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_job_hopper_primoz_6_expected():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Regional Sales",
                            "employment_type": "Full-time",
                            "company_name": "Harmonic",
                            "company_logo_url": "s3://signaight-dev/profile_photos/8/7d/b0499/87db0499-5991-4949-816c-b331317c3bd4.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/harmonic/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=5).to_date_string(),
                                "date_to": pendulum.now().subtract(months=1).to_date_string()
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Chief Executive Officer",
                            "employment_type": "Part-time",
                            "description": "Based on 30 years of experience, Delta Networks is expanding into regional  waters of system integration in the broadcast media, security and telecom areas. Looking forward to meeting you at IBC!",
                            "company_name": "Delta Networks",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/a0/2e546/ea02e546-ca1c-4767-a4a3-96e98ea47138.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/deltanetworks-europe/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=12).to_date_string(),
                                "date_to": pendulum.now().subtract(months=5).to_date_string()
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Regional Sales Director",
                            "employment_type": "Full-time",
                            "description": "Responsible for on going business and business development in the region. Evangelising cloud and new workflows adoption in broadcast media. Working both directly and with system integrators based on Devops for perpetual improvement of partner experiences. Working with different levels of contacts and project sizes, both private in publi sectors, adjusting to local best business practices. Constantly striving for Learning, Innovation and Growth.",
                            "company_name": "TVU Networks",
                            "company_logo_url": "s3://signaight-dev/profile_photos/1/6a/4455f/16a4455f-a3ab-4380-a68f-b3af953cdd64.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/tvu-networks/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=7, years=6).to_date_string(),
                                "date_to": pendulum.now().subtract(months=9).to_date_string()
                            },
                            "duration": {
                                "years": 5,
                                "months": 11
                            }
                        },
                        {
                            "title": "President",
                            "company_name": "Otium Delfin",
                            "period": {
                                "date_from": pendulum.now().subtract(months=2, years=25).to_date_string(),
                                "date_to": pendulum.now().subtract(months=9).to_date_string()
                            },
                            "duration": {
                                "years": 25,
                                "months": 5
                            }
                        },
                        {
                            "title": "Regional Sales Director",
                            "company_name": "Net Insight",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/57/2b707/b572b707-a4af-427b-beeb-65d1e33ed596.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/net-insight/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=4, years=11).to_date_string(),
                                "date_to": pendulum.now().subtract(months=7, years=6).to_date_string()
                            },
                            "duration": {
                                "years": 4,
                                "months": 11
                            }
                        },
                        {
                            "title": "Sales Manager",
                            "description": "Key Customer facing sales executive for following markets in Europe: Hungary, Slovenia, Croatia, Bosnia and Herzegovina, Kosovo, Macedonia, Albania. Defending dominant position in some of them and increasing market share in others. Closely working with R&D and presales in order to generate sustainable competitive advantage for the company. Working with all biggest mobile and fixed Telecom operators, including all vertical markets in the region.",
                            "company_name": "Ceragon Networks",
                            "company_logo_url": "s3://signaight-dev/profile_photos/f/21/12a8d/f2112a8d-7934-476e-94d7-bc9077b3ff7d.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/ceragon-networks/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=6, years=14).to_date_string(),
                                "date_to": pendulum.now().subtract(months=4, years=11).to_date_string()
                            },
                            "duration": {
                                "years": 3,
                                "months": 2
                            }
                        },
                        {
                            "title": "Sales Manager",
                            "description": "Bring in the numbers!",
                            "company_name": "Nera Networks AS",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/27/60f24/72760f24-abf2-4e2d-8af2-a0a1f1ce388b.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/nera-networks-as/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=0, years=15).to_date_string(),
                                "date_to": pendulum.now().subtract(months=4, years=11).to_date_string()
                            },
                            "duration": {
                                "years": 3,
                                "months": 10
                            }
                        },
                        {
                            "title": "Sales  Manager",
                            "description": "Telecommunications: Upgrading Iskra global network of partners and sales revenues each year. Building global network &amp; expanding team of collegues and business partners worldwide, centred around unique skills and solutions.",
                            "company_name": "Iskra Sistemi",
                            "period": {
                                "date_from": pendulum.now().subtract(months=4, years=22).to_date_string(),
                                "date_to": pendulum.now().subtract(months=0, years=15).to_date_string()
                            },
                            "duration": {
                                "years": 7,
                                "months": 5
                            }
                        },
                        {
                            "title": "Key Account manager",
                            "description": "Develop network and bring in the $$$",
                            "company_name": "Iskra Transmission d.d.",
                            "period": {
                                "date_from": pendulum.now().subtract(months=4, years=22).to_date_string(),
                                "date_to": pendulum.now().subtract(months=6, years=19).to_date_string()
                            },
                            "duration": {
                                "years": 3
                            }
                        },
                        {
                            "title": "Director Professional Services and Delivery",
                            "description": "Managed group of extremely talented Management Consultants",
                            "company_name": "Be Solutions",
                            "company_logo_url": "s3://signaight-dev/profile_photos/5/1b/1989d/51b1989d-7a35-4ac6-bd7b-037753e27bfb.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/be-solutions/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=7, years=24).to_date_string(),
                                "date_to": pendulum.now().subtract(months=4, years=22).to_date_string()
                            },
                            "duration": {
                                "years": 1,
                                "months": 4
                            }
                        },
                        {
                            "title": "Programme Director",
                            "description": "Merger of third biggest and fourth biggest national insurance companies",
                            "company_name": "Slovenica",
                            "period": {
                                "date_from": pendulum.now().subtract(months=1, years=27).to_date_string(),
                                "date_to": pendulum.now().subtract(months=3, years=23).to_date_string()
                            },
                            "duration": {
                                "years": 3,
                                "months": 11
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_job_hopper_brane_6_expected():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions":  [
                        {
                            "title": "Managing Director",
                            "employment_type": "Full-time",
                            "description": "Undertaking and managing the most difficult projects in the field of HR. Supplying customers with scarce candidates, but advising companies on how to obtain their employees by building a secure and diverse environment.",
                            "company_name": "Talents Pro",
                            "period": {
                                "date_from":  pendulum.now().subtract(months=13).to_date_string(),
                                "date_to": pendulum.now().subtract(months=1).to_date_string()
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Advisor to the Board",
                            "employment_type": "Full-time",
                            "company_name": "Kariera Slovenija",
                            "company_logo_url": "s3://signaight-dev/profile_photos/b/40/182a3/b40182a3-1086-4dd2-a394-241d9ac226b4.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/kariera-slovenija/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=21).to_date_string(),
                                "date_to": pendulum.now().subtract(months=13).to_date_string()
                            },
                            "duration": {
                                "months": 8
                            }
                        },
                        {
                            "title": "General Manager",
                            "description": "Its an honor to lead a company like Naton. It's a constant process where standards are high and being able to live up to the tasks is overwhelming.  My responsibilities in Naton is primarily employee satisfaction. When this is achieved, success in any and all forms just simply follow.",
                            "company_name": "Naton HR",
                            "period": {
                                "date_from": pendulum.now().subtract(months=10, years=10).to_date_string(),
                                "date_to": pendulum.now().subtract(months=21).to_date_string()
                            },
                            "duration": {
                                "years": 9,
                                "months": 1
                            }
                        },
                        {
                            "title": "General Manager",
                            "employment_type": "Full-time",
                            "company_name": "Prohuman Slovenia",
                            "period": {
                                "date_from": pendulum.now().subtract(months=10, years=10).to_date_string(),
                                "date_to": pendulum.now().subtract(months=9, years=1).to_date_string()
                            },
                            "duration": {
                                "years": 9,
                                "months": 1
                            }
                        },
                        {
                            "title": "Advisor",
                            "description": "As an advisor to the content of the 4th Pillar platform. Offering a new tool  for recruiters, human resource dept's and to all who's common goal is to make a step forward in HR.",
                            "company_name": "4th Pillar",
                            "period": {
                                "date_from": pendulum.now().subtract(months=5, years=7).to_date_string(),
                                "date_to": pendulum.now().subtract(months=10, years=7).to_date_string()
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Sales and Marketing Manager",
                            "description": "Sales and Marketing Manager",
                            "company_name": "PROMLES d.o.o.",
                            "period": {
                                "date_from": pendulum.now().subtract(months=7, years=13).to_date_string(),
                                "date_to": pendulum.now().subtract(months=6, years=12).to_date_string()
                            },
                            "duration": {
                                "years": 1,
                                "months": 11
                            }
                        },
                        {
                            "title": "Senior Account Manager",
                            "description": "Increased sales with existing accounts and made a break through in new fields of business.",
                            "company_name": "Printec S.I.",
                            "period": {
                                "date_from": pendulum.now().subtract(months=2, years=16).to_date_string(),
                                "date_to": pendulum.now().subtract(months=6, years=14).to_date_string()
                            },
                            "duration": {
                                "years": 2,
                                "months": 4
                            }
                        },
                        {
                            "title": "Head of Retail Banking",
                            "description": "Responsible for all individual accounts. Managing more than 100 personell throughout the country. With out of the box mindset, succeeded in increasing opening accounts and gaining new customers.",
                            "company_name": "Sparkasse",
                            "period": {
                                "date_from": pendulum.now().subtract(months=1, years=17).to_date_string(),
                                "date_to": pendulum.now().subtract(months=2, years=16).to_date_string()
                            },
                            "duration": {
                                "years": 1,
                                "months": 1
                            }
                        },
                        {
                            "title": "Senior Project Manager in Strategic Marketing",
                            "description": "Repositioning and rebranding the entire fleet of electronic banking products. Sales, Marrketing and profitability wise.  Also in charge of larger bank projects such as co-brand, pay now card partnership. Rebranding and repositioning of all ATM's within the bank.",
                            "company_name": "SKB banka Societe Generale Group",
                            "period": {
                                "date_from": pendulum.now().subtract(years=23).to_date_string(),
                                "date_to": pendulum.now().subtract(months=9, years=16).to_date_string()
                            },
                            "duration": {
                                "years": 6,
                                "months": 4
                            }
                        },
                        {
                            "title": "Account Director",
                            "description": "In charge of larger accounts such as NLB bank, Peugeot Slovenia, Adria Airways, Večer etc.",
                            "company_name": "Futura DDB",
                            "company_logo_url": "s3://signaight-dev/profile_photos/0/a0/04980/0a004980-1d50-4364-b611-73057a22051a.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/futura-ddb/",
                            "period": {
                                "date_from": pendulum.now().subtract(months=8, years=25).to_date_string(),
                                "date_to": pendulum.now().subtract(months=1, years=23).to_date_string()
                            },
                            "duration": {
                                "years": 2,
                                "months": 8
                            }
                        },
                        {
                            "title": "Senior Marketing Manager",
                            "description": "In charge of e-banking and renewal of the banks website.",
                            "company_name": "Abanka Vipa d.d.",
                            "period": {
                                "date_from": pendulum.now().subtract(months=4, years=31).to_date_string(),
                                "date_to": pendulum.now().subtract(months=9, years=25).to_date_string()
                            },
                            "duration": {
                                "years": 5,
                                "months": 8
                            }
                        }
                    ],
                    "projects": [],
                    "honors": [],
                    "publications": [
                        {
                            "description": "What is happening in the field of recruitment in Slovenia and how headhunting is slowly, but persistantly on the move with the latest worldwide trends.",
                            "name": "Recruitment and Headhunting in SLovenia"
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_career_break_student_position():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Graduate",
                            "employment_type": "Full-time",
                            "company_name": "Atea Danmark",
                            "company_logo_url": "s3://signaight-dev/profile_photos/d/fc/03555/dfc03555-525e-4ef0-a799-937451724b1d.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/atea-danmark/",
                            "period": {
                                "date_from": "2025-02-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Project Assistant",
                            "employment_type": "Part-time",
                            "company_name": "Copenhagen Capacity",
                            "company_logo_url": "s3://signaight-dev/profile_photos/5/7c/497b4/57c497b4-979c-44e7-ae8b-e0d5a7d99bd1.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/copenhagen-capacity/",
                            "period": {
                                "date_from": "2022-09-01",
                                "date_to": "2024-08-01"
                            },
                            "duration": {
                                "years": 2
                            }
                        },
                        {
                            "title": "Marketing and communications assistant ",
                            "employment_type": "Part-time",
                            "description": "Changing positions to Marketing assistant, I gained insight into workflows and communication through CRM systems with the purpose of attracting and nurturing prospect candidates. Furthermore, I worked with several marketing initiatives and content creation.",
                            "company_name": "Copenhagen Business School",
                            "company_logo_url": "s3://signaight-dev/profile_photos/3/45/657ef/345657ef-f82a-4687-9799-f21a6ab0a3d0.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/school/copenhagen-business-school/",
                            "period": {
                                "date_from": "2022-02-01",
                                "date_to": "2022-10-01"
                            },
                            "duration": {
                                "months": 9
                            }
                        },
                        {
                            "title": "Admissions Assistant",
                            "employment_type": "Part-time",
                            "description": "As an admissions assistant, my main responsibility was communication with prospect candidates, assessment of eligibility for the programme, and assistance of visas and other practical matters to admitted students. Furthermore, I assisted the other MBA departments when necessary.",
                            "company_name": "Copenhagen Business School",
                            "company_logo_url": "s3://signaight-dev/profile_photos/9/8f/58671/98f58671-5201-43cc-9de5-3e2214135dcb.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/school/copenhagen-business-school/",
                            "period": {
                                "date_from": "2021-05-01",
                                "date_to": "2022-01-01"
                            },
                            "duration": {
                                "months": 9
                            }
                        },
                        {
                            "title": "Middle Manager",
                            "employment_type": "Part-time",
                            "description": "Working as a middle manager, I had responsibility of the daily operations when I was at work. I opened the bakery in the morning, baked and arranged the goods, recevied deliveries and managed the sellers who were working.",
                            "company_name": "Holms Bager",
                            "period": {
                                "date_from": "2018-10-01",
                                "date_to": "2021-10-01"
                            },
                            "duration": {
                                "years": 3,
                                "months": 1
                            }
                        },
                        {
                            "title": "Front of House Concierge",
                            "description": "I worked in a Centrica office as front of house concierge for four months. Here I dealed with a lot of different tasks. I welcomed guests coming in for meetings with directors and traders and helped the employee at the office with bookings of meeting rooms and did my best to meet their needs. I prepared catering for meetings and helped with facilities matters.",
                            "company_name": "Carillion",
                            "company_logo_url": "s3://signaight-dev/profile_photos/c/11/517b0/c11517b0-a8b3-440d-a87b-2a32cb2b5eb4.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/carillion/",
                            "period": {
                                "date_from": "2017-02-01",
                                "date_to": "2017-05-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Waitress",
                            "description": "I helped opening the English grill restaurant Temple and Sons. As waitress I learned all knowledge about our product to provide top quality to our customers. Mainly, I served the dining people and did my best to give them a memorable evening. I also prepared the restaurant for opening as well as closing it down after service.",
                            "company_name": "Temple and Sons",
                            "period": {
                                "date_from": "2016-11-01",
                                "date_to": "2017-02-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Sales Advisor",
                            "description": "I was working as a Sales advisor for several CrossEyes Central London stores. \nI provided customer service on the shop floor and have also done a number of administrative tasks such as making newsletters and mail merges.\nFurthermore, I was identifying a number of suppliers of marketing materials, and have helped the company choosing the right supplier and product.",
                            "company_name": "CrossEyes UK Ltd",
                            "period": {
                                "date_from": "2016-08-01",
                                "date_to": "2016-10-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Servicemedarbejder",
                            "description": "I mainly worked with customer service at the counter but was also granted administrative responsibility such as receiving incoming deliveries and arranging them on the shelves. Furthermore, I set up campaigns in the store during special promotions.",
                            "company_name": "The SPAR Group Ltd",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/fd/4b840/efd4b840-3368-4ed8-b469-bc443f5f11d3.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/sparsouthafrica/",
                            "period": {
                                "date_from": "2012-03-01",
                                "date_to": "2016-08-01"
                            },
                            "duration": {
                                "years": 4,
                                "months": 6
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_career_break_covid():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Work Planner",
                            "employment_type": "Full-time",
                            "description": "I now continue at VR FleetCare in a more defined role as Work Planner. My focus is on organizing planned maintenance and inspections, emphasizing preventive over reactive maintenance. I oversee equipment calibrations and lead development efforts within the Spotilla system, collaborating closely with subcontractors to ensure technical support and continuous improvement. This role has brought more responsibility, allowing me to further develop processes within the Factory Services unit.",
                            "company_name": "VR FleetCare",
                            "company_logo_url": "s3://signaight-dev/profile_photos/7/b6/28db6/7b628db6-f7e4-4425-8bf9-10e245cea77f.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/vrfleetcare/",
                            "period": {
                                "date_from": "2024-10-01",
                                "date_to": "Present"
                            },
                            "duration": {
                                "months": 8
                            }
                        },
                        {
                            "title": "Development Specialist",
                            "employment_type": "Full-time",
                            "description": "I focused on improving and streamlining our digital maintenance system, enhancing maintenance plans, and working with subcontractors to ensure smooth operations. While still overseeing a team of independent mechanics and an electrician, I provided the support they needed to succeed.\n\nDuring this time, I also completed my thesis with excellent marks, reflecting my commitment to both my professional and academic growth.",
                            "company_name": "VR FleetCare",
                            "company_logo_url": "s3://signaight-dev/profile_photos/a/fe/855c5/afe855c5-6385-4470-8502-4f51724bcc49.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/vrfleetcare/",
                            "period": {
                                "date_from": "2024-04-01",
                                "date_to": "2024-10-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Technical Specialist",
                            "employment_type": "Contract",
                            "description": "I continued my duties as a Technical Specialist through my own company, Valens Technologies. I ensured the seamless functionality of the digital maintenance system, keeping it up to date and addressing issues. After a successful summer in Helsinki, I've expanded my impact, assisting colleagues across Finland.",
                            "company_name": "VR FleetCare",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/39/2a7e2/e392a7e2-ce9f-4121-93be-7292bc8b69b9.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/vrfleetcare/",
                            "period": {
                                "date_from": "2023-09-01",
                                "date_to": "2024-04-01"
                            },
                            "duration": {
                                "months": 8
                            }
                        },
                        {
                            "title": "Technical Specialist",
                            "employment_type": "Full-time",
                            "description": "As a Technical Specialist, combining my engineer and mechanic's skillset, I was part of ensuring the optimal functionality of all equipment and tools within the Ilmala depot in Helsinki. My responsibilities extended to utilizing and managing the maintenance program, guaranteeing the seamless operation of critical assets. Beyond the workshop, I collaborated extensively with various departments, offering support and expertise whenever required.\n\nTaking on additional responsibilities, I stepped into project roles during colleagues' absences, showcasing my versatility and commitment to project success. Above all, as our department consisted of mechanics and electricians, I prioritized ensuring they had all necessary resources, information, and assistance to do their job, fostering a collaborative and efficient work environment.\n\nMy time as a Technical Specialist was characterized by a proactive approach to maintenance, meticulous project execution, and effective collaboration across departments.",
                            "company_name": "VR FleetCare",
                            "company_logo_url": "s3://signaight-dev/profile_photos/e/a3/965ae/ea3965ae-5fd0-4da2-a485-270dbcf5ff19.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/vrfleetcare/",
                            "period": {
                                "date_from": "2023-04-01",
                                "date_to": "2023-08-01"
                            },
                            "duration": {
                                "months": 5
                            }
                        },
                        {
                            "title": "Aircraft Mechanic Trainee",
                            "employment_type": "Internship",
                            "description": "During my internship at Finnair, I served as an Aircraft Mechanic Trainee, actively contributing to the maintenance operations of A330 and A350 aircrafts. Immersed in a dynamic aviation environment, I honed my skills in mechanics, enjoyed working in a team, and gained valuable insights into the aircraft mechanical systems and importance of safety. My responsibilities included ensuring flight safety standards and actively participating in maintenance and repair activities.",
                            "company_name": "Finnair",
                            "company_logo_url": "s3://signaight-dev/profile_photos/5/c8/a0b85/5c8a0b85-41dd-46ed-bfbd-6155dbd4b3d0.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/finnair/",
                            "period": {
                                "date_from": "2023-01-01",
                                "date_to": "2023-03-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Project Manager",
                            "employment_type": "Full-time",
                            "description": "In my second summer as a Project Manager at Rototec, I elevated my expertise, undertaking more challenging geothermal drilling projects and worked more independently. While embracing increased autonomy, I valued the strong safety net and expertise of co-workers and subcontractors. Building on my previous experience, I continued to excel in project management with an expanded scope.",
                            "company_name": "Rototec",
                            "company_logo_url": "s3://signaight-dev/profile_photos/8/ea/bec75/8eabec75-0a24-4b70-9fe6-9249258542a8.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/rototec-/",
                            "period": {
                                "date_from": "2021-06-01",
                                "date_to": "2021-07-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Project Manager",
                            "employment_type": "Full-time",
                            "description": "As the Project Manager at Rototec, my responsibility was to manage comprehensively geothermal drilling projects. Duties involved site inspections, site meetings, time schedule planning, stakeholder communication, material logistics, cost management, reporting and overseeing subcontractors.\n\nThis dynamic position demanded constant collaboration with diverse professionals, subcontractors, clients, and residents. My role involved not only meeting project objectives but also ensuring that all stakeholders were informed and engaged throughout the process. Additionally, I rigorously ensured project compliance with national and local laws and regulations.\n\nThe complexity of the projects often required adept problem-solving in the face of challenges or technical issues. While the majority of my projects were centered in the Southern part of Finland, my commitment to project success occasionally required travel to locations further.\n\n\"In her work, Elina has shown initiative and the courage to handle things independently. She has quickly adopted a broad work picture and managed it responsibly.\"",
                            "company_name": "Rototec",
                            "company_logo_url": "s3://signaight-dev/profile_photos/d/1e/49269/d1e49269-7eae-49af-aada-92012875a6db.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/rototec-/",
                            "period": {
                                "date_from": "2020-05-01",
                                "date_to": "2020-08-01"
                            },
                            "duration": {
                                "months": 4
                            }
                        },
                        {
                            "title": "Project Engineer Trainee",
                            "description": "Assisting in circular economy projects that took place in Hiedanranta, Tampere.",
                            "company_name": "Tampere University of Applied Sciences",
                            "company_logo_url": "s3://signaight-dev/profile_photos/2/fb/3ee5e/2fb3ee5e-ec70-4dbe-84b9-e9ded8149469.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/school/tamk/",
                            "period": {
                                "date_from": "2019-05-01",
                                "date_to": "2019-10-01"
                            },
                            "duration": {
                                "months": 6
                            }
                        },
                        {
                            "title": "Shift Manager",
                            "company_name": "Lapinjärven Mehiläispesä Oy",
                            "period": {
                                "date_from": "2018-06-01",
                                "date_to": "2018-08-01"
                            },
                            "duration": {
                                "months": 3
                            }
                        },
                        {
                            "title": "Summer Assistant",
                            "employment_type": "Full-time",
                            "company_name": "TAKLAB Tampereen asbesti- ja kuitulaboratorio Oy",
                            "company_logo_url": "s3://signaight-dev/profile_photos/f/b0/a529a/fb0a529a-14b4-42a1-aca7-79ff2e0dbe66.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/taklab/",
                            "period": {
                                "date_from": "2018-05-01",
                                "date_to": "2018-06-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        },
                        {
                            "title": "Summer Trainee",
                            "company_name": "Valmet",
                            "company_logo_url": "s3://signaight-dev/profile_photos/4/7d/35a2b/47d35a2b-2293-428c-af27-1179be635fbd.jpg",
                            "linkedin_company_url": "https://www.linkedin.com/company/valmet/",
                            "period": {
                                "date_from": "2017-06-01",
                                "date_to": "2017-12-01"
                            },
                            "duration": {
                                "months": 7
                            }
                        },
                        {
                            "title": "Employee",
                            "company_name": "VMP Group",
                            "period": {
                                "date_from": "2014-09-01",
                                "date_to": "2016-10-01"
                            },
                            "duration": {
                                "years": 2,
                                "months": 2
                            }
                        },
                        {
                            "title": "Substitute Teacher",
                            "description": "Taught English, Swedish and handcrafts",
                            "company_name": "Kevätkummun koulu",
                            "period": {
                                "date_from": "2015-10-01",
                                "date_to": "2015-11-01"
                            },
                            "duration": {
                                "months": 2
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def profile_linkedin_work_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "Present"
                            },
                            "location": "Tehran"
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_xing_work_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "Present"
                            },
                            "location": "Tehran"
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_facebook_work_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Product Analyst",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "Present"
                        },
                        "fb_workplace_location": "Tehran"
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_linkedin_work_not_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "linkedin_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "Present"
                            },
                            "location": "New York"
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_xing_work_not_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "xing_work": {
                    "positions": [
                        {
                            "title": "Product Analyst",
                            "company_name": "Something",
                            "period": {
                                "date_from": "2020-08-01",
                                "date_to": "Present"
                            },
                            "location": "New York"
                        },
                    ]
                },
                # "facebook_work": {}
            },
        }
    }


@pytest.fixture
def profile_facebook_work_not_watchlist_country():
    return {
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Product Analyst",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "Present"
                        },
                        "fb_workplace_location": "New York"
                    },
                ]
            },
        }
    }


@pytest.fixture
def profile_location_and_facebook_work_watchlist_country():
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
        },
        "biographic_details": {
            "work": {
                "facebook_work": [
                    {
                        "fb_work_title": "Product Analyst",
                        "fb_workplace_name": "Something",
                        "fb_work_period": {
                            "date_from": "2020-01-01",
                            "date_to": "Present"
                        },
                        "fb_workplace_location": "Tehran"
                    },
                ]
            },
        }
    }
